import pytest

from seeq import spy

from ...tests import test_common


def setup_module():
    test_common.login()


@pytest.mark.disabled
def test_search():
    # spy.login('mark.derbecker@seeq.com', 'DataLab!')
    results_df = spy.workbooks.search(all_properties=True, recursive=True)
    print(results_df)
