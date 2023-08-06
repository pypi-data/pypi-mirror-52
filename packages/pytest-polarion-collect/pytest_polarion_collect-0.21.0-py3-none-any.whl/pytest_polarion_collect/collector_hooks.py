"""pytest plugin for populating items with polarion test cases data"""

import pytest

from pytest_polarion_collect import utils

# pylint: disable=protected-access


class MetadataCollectorHooks:
    @pytest.hookimpl
    @staticmethod
    def pytest_collect_polarion_metadata(session, items):
        """Hook implementation that appends parsed metadata to items."""
        utils.set_cache(session)

        for item in items:
            if not utils.is_test_dir(str(item.fspath), session._test_dirs_cache):
                continue

            utils.get_testcase_data(item, session._docstrings_cache)


def pytest_addhooks(pluginmanager):
    """Registers the hook with pytest."""
    from pytest_polarion_collect import hookspec

    pluginmanager.add_hookspecs(hookspec)
    pluginmanager.register(MetadataCollectorHooks)
