"""pytest plugin for collecting polarion test cases data"""

import json
import os
import re

import pytest

from polarion_docstrings import parser as docparser
from polarion_docstrings import utils as doc_utils

DUPLICATES = "duplicates.log"
TESTS_DATA = "tests_data.json"

STEP_NUMBERING = re.compile(r"[0-9]+[.)]? ?")
TEST_PARAMS = re.compile(r"\[.*\]")


# pylint: disable=protected-access
def _set_cache(session):
    # cache of parsed docstrings (can be used by other plugins as well)
    if not hasattr(session, "_docstrings_cache"):
        session._docstrings_cache = {}
    if "_parsed_files" not in session._docstrings_cache:
        session._docstrings_cache["_parsed_files"] = set()

    # cache of dirs with Polarion tests, cache of dirs with non-Polarion tests
    if not hasattr(session, "_test_dirs_cache"):
        session._test_dirs_cache = set(), set()


def pytest_addoption(parser):
    """Adds command line options."""
    group = parser.getgroup("Polarion: options related to test cases data collection")
    group.addoption(
        "--generate-json",
        action="store_true",
        default=False,
        help="generate JSON file with tests data",
    )
    group.addoption(
        "--meta-filter",
        type=json.loads,
        help="only run tests with the given meta (JSON) matches in polarion metadata",
    )


def get_marker(item, marker):
    """Gets the marker in a way that's supported by the pytest version."""
    try:
        return item.get_marker(marker)
    except AttributeError:
        return item.get_closest_marker(marker)


def extract_fixtures_values(item):
    """Extracts names and values of all the fixtures that the test has.

    Args:
        item: py.test test item
    Returns:
        :py:class:`dict` with fixtures and their values.
    """
    try:
        return item.callspec.params.copy()  # protect against accidential manipulation of the spec
    except AttributeError:
        # Some of the test items do not have callspec, so fall back
        # This can cause some problems if the fixtures are used in the guards in this case, but
        # that will tell use where is the problem and we can then find it out properly.
        return {}


def get_unicode_str(obj):
    """Makes sure obj is a unicode string."""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="ignore")
    return str(obj)


def get_nodeid_full_path(item):
    """Assembles nodeid with full file path."""
    return "{}::{}".format(str(item.fspath), item.location[2].replace(".", "::"))


def get_raw_docstring(item):
    """Gets unprocessed docstring of test function."""
    docstring = ""
    try:
        docstring = get_unicode_str(item.function.__doc__)
    except (AttributeError, UnicodeDecodeError):
        pass

    return docstring


def get_parsed_docstring(item, docstrings_cache):
    """Gets parsed docstring from cache."""
    nodeid = TEST_PARAMS.sub("", get_nodeid_full_path(item))

    if str(item.fspath) not in docstrings_cache["_parsed_files"]:
        docstrings = docparser.get_docstrings_in_file(str(item.fspath))
        merged_docstrings = docparser.merge_docstrings(docstrings)
        docstrings_cache.update(merged_docstrings)
        docstrings_cache["_parsed_files"].add(str(item.fspath))

    # handle situations when the node was created dynamically
    if nodeid not in docstrings_cache:
        raw_docstring = get_raw_docstring(item)
        record = docparser.parse_docstring(raw_docstring)
        docstrings_cache[nodeid] = docparser.merge_record(record, docstrings_cache, nodeid)

    return docstrings_cache[nodeid]


def _get_caselevel(item, parsed_docstring):
    caselevel = parsed_docstring.get("caselevel")
    if caselevel:
        return caselevel

    try:
        tier = int(get_marker(item, "tier").args[0])
    except (ValueError, AttributeError):
        tier = 0

    return tier


def _get_caseautomation(item, parsed_docstring):
    caseautomation = parsed_docstring.get("caseautomation")
    if caseautomation:
        return caseautomation

    # a bare marker results in 'notautomated', a marker with an arg results in 'manualonly'
    marker = get_marker(item, "manual")
    if marker is not None:
        # ignore the arg value itself
        return "manualonly" if getattr(marker, "args", False) else "notautomated"

    return "automated"


def _get_automation_script(item):
    return "{}#L{}".format(item.location[0], item.function.__code__.co_firstlineno)


def _get_description(item):
    raw_docstring = get_raw_docstring(item)
    try:
        description = docparser.strip_polarion_data(raw_docstring)
    except ValueError as err:
        print("Cannot parse the description of {}: {}".format(item.location[2], err))
        description = ""

    return description


def _get_steps_and_results(parsed_docstring):
    steps = parsed_docstring.get("testSteps")
    if not steps:
        return None

    test_steps = []
    expected_results = []

    results = parsed_docstring.get("expectedResults") or ()
    try:
        steps = [STEP_NUMBERING.sub("", s) for s in steps]
        results = [STEP_NUMBERING.sub("", r) for r in results]
    # pylint: disable=broad-except
    except Exception:
        # misconfigured steps or results, ignoring
        return test_steps, expected_results

    for index, step in enumerate(steps):
        test_steps.append(step)

        try:
            result = results[index]
        except IndexError:
            result = ""
        expected_results.append(result)

    return test_steps, expected_results


def _get_requirements_names(item):
    """Gets names of all linked requirements in a way that's supported by the pytest version."""
    if hasattr(item, "iter_markers"):
        try:
            return [r.args[0] for r in item.iter_markers("requirement")]
        except (AttributeError, IndexError):
            pass
    else:
        try:
            return list(item.get_marker("requirement").args)
        except AttributeError:
            pass

    return None


def _get_linked_items(parsed_docstring):
    linked_items = parsed_docstring.get("linkedWorkItems")
    return [item.strip('" ') for item in linked_items.split(",")] if linked_items else None


def get_testcase_data(item, docstrings_cache):
    """Gets data for single test case entry."""
    if hasattr(item, "_testcase_data"):
        # pylint: disable=protected-access
        return item._testcase_data

    parsed_docstring = get_parsed_docstring(item, docstrings_cache)
    test_name = item.location[2]
    testcase_data = {}

    testcase_data["caseautomation"] = _get_caseautomation(item, parsed_docstring)

    if testcase_data["caseautomation"] == "automated":
        testcase_data["automation_script"] = _get_automation_script(item)

    test_steps = _get_steps_and_results(parsed_docstring)
    if test_steps:
        testcase_data["testSteps"], testcase_data["expectedResults"] = test_steps

    testcase_data["title"] = parsed_docstring.get("title") or test_name
    testcase_data["id"] = parsed_docstring.get("id") or test_name
    testcase_data["assignee-id"] = parsed_docstring.get("assignee") or None
    testcase_data["caselevel"] = _get_caselevel(item, parsed_docstring)
    testcase_data["description"] = _get_description(item)
    testcase_data["initial-estimate"] = parsed_docstring.get("initialEstimate")
    testcase_data["linked-items"] = _get_requirements_names(item) or _get_linked_items(
        parsed_docstring
    )
    testcase_data["params"] = list(extract_fixtures_values(item).keys()) or None
    testcase_data["nodeid"] = item.nodeid.replace("::()", "")

    # save the rest of the fields as it is
    for field, record in parsed_docstring.items():
        if field not in testcase_data:
            testcase_data[field] = record

    item._testcase_data = testcase_data
    return testcase_data


def _get_name(obj):
    if hasattr(obj, "_param_name"):
        # pylint: disable=protected-access
        return str(obj._param_name)
    if hasattr(obj, "name"):
        return str(obj.name)
    return str(obj)


def process_testresult(item, docstrings_cache):
    """Gets data for single test result entry."""
    testcase_data = get_testcase_data(item, docstrings_cache)
    if not testcase_data:
        return {}

    testresult_data = {
        "title": testcase_data["title"],
        "verdict": "waiting",
        "id": testcase_data["id"],
    }

    try:
        params = item.callspec.params
    except AttributeError:
        params = {}

    parameters = {p: _get_name(v) for p, v in params.items()}
    if parameters:
        testresult_data["params"] = parameters

    return testresult_data


def gen_duplicates_log(items):
    """Generates log file containing non-unique test cases names."""
    names = {}
    duplicates = set()

    for item in items:
        name = TEST_PARAMS.sub("", item.location[2])
        path = item.location[0]

        name_record = names.get(name)
        if name_record:
            name_record.add(path)
        else:
            names[name] = {path}

    for name, paths in names.items():
        if len(paths) > 1:
            duplicates.add(name)

    with open(DUPLICATES, "w") as outfile:
        for test in sorted(duplicates):
            outfile.write("{}\n".format(test))


def write_json(data_dict, out_file):
    """Outputs data to file in JSON format."""
    with open(out_file, "w") as out:
        json.dump(data_dict, out, indent=4)
        out.write("\n")


def is_test_dir(abs_filename, test_dirs_cache):
    """Checks if the test is in directory with Polarion tests and updates cache."""
    white, black = test_dirs_cache

    for tdir in white:
        if abs_filename.startswith(tdir):
            return True
    for tdir in black:
        if abs_filename.startswith(tdir):
            return False

    test_dir = os.path.dirname(abs_filename)
    test_top_dir = doc_utils.find_tests_marker(test_dir)
    if test_top_dir:
        white.add(test_top_dir)
    else:
        black.add(test_dir)
    return bool(test_top_dir)


def meta_matches(session, item, metafilters):
    """Apply meta filters (key/value pairs) to the item metadata.

    Returns:
        bool: True if all the meta filters match the item's metadata
    """
    testcase_data = get_testcase_data(item, session._docstrings_cache)
    try:
        full_match = all(
            [
                testcase_data.get(filter_key) == filter_value
                for filter_key, filter_value in metafilters.items()
            ]
        )
    except KeyError:
        print("Failed meta-filter match lookup for test {}".format(item.nodeid))
        full_match = False
    return full_match


def _process_json_data(session, items):
    """Generates JSON files for testcase and testresult data using collected items.

    Writes a duplicates log file.
    """
    gen_duplicates_log(items)

    processed = set()
    testcases = []
    testsuites = []

    for item in items:
        if not is_test_dir(str(item.fspath), session._test_dirs_cache):
            continue

        test_name = item.location[2]
        if test_name in processed:
            continue
        processed.add(test_name)
        testcases.append(get_testcase_data(item, session._docstrings_cache))
        testsuites.append(process_testresult(item, session._docstrings_cache))

    tests_data = {"testcases": testcases, "results": testsuites}
    write_json(tests_data, TESTS_DATA)


@pytest.mark.trylast
def pytest_collection_modifyitems(session, config, items):
    """Generate testcase JSON file in collection only mode, or modify nodes based on meta filter."""
    # prevent on slave nodes (xdist)
    if hasattr(config, "slaveinput"):
        return

    gen_json = config.getoption("generate_json")
    collect = config.getoption("collectonly")
    metafilters = config.getoption("meta_filter")

    _set_cache(session)

    if metafilters:
        keep, discard = [], []
        # Apply any meta filters and discard cases
        # Not a great pattern, pytest issues #1372 and #1373
        for item in items:
            if not is_test_dir(str(item.fspath), session._test_dirs_cache):
                continue
            if not meta_matches(session, item, metafilters):
                # filter did not match item meta, discard the item
                discard.append(item)
                continue
            keep.append(item)

        # modify items list with kept functions
        items[:] = keep
        config.hook.pytest_deselected(items=discard)
        # make the number of tests uncollected by the filter available
        session._uncollected_meta_filter = len(discard)

    if gen_json and collect:
        _process_json_data(session, items)


def pytest_collect_polarion_metadata(session, items):
    """Hook implementation that appends parsed metadata to items."""
    _set_cache(session)

    for item in items:
        if not is_test_dir(str(item.fspath), session._test_dirs_cache):
            continue

        get_testcase_data(item, session._docstrings_cache)


class MetadataCollectorHooks:
    """Hook specification for collecting metadata."""

    # pylint: disable=no-self-use
    def pytest_collect_polarion_metadata(self, session, items):
        """Called to collect metadata."""


def pytest_addhooks(pluginmanager):
    """Registers the hook with pytest."""
    pluginmanager.add_hookspecs(MetadataCollectorHooks)
