import pytest

from seeq import spy

from ...tests import test_common


def setup_module():
    test_common.login()


@pytest.mark.system2
def test_save_load():
    spy.login('mark.derbecker@seeq.com', 'DataLab!')
    #workbook = spy.workbooks.Workbook('F2C5B87F-3EB4-4973-97A1-63C003F6481B')
    #workbook.save(r'D:\Scratch\WorkbookExport')

    workbook = spy.workbooks.Workbook.load(r'D:\Scratch\WorkbookExport')

    workbook.push(prefix='blah')
