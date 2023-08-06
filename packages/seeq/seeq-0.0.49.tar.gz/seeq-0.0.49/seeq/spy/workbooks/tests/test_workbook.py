import pytest

from seeq import spy

from ...tests import test_common


def setup_module():
    test_common.login()


@pytest.mark.system2
def test_save_load():
    spy.login('mark.derbecker@seeq.com', 'DataLab!')
    #workbook = spy.workbooks.Workbook('EBA46551-EE20-43F0-9383-4E6E9337AC60')
    #workbook.save(r'D:\Scratch\WorkbookExport')

    workbook = spy.workbooks.Workbook.load(r'D:\Scratch\WorkbookExport')
    workbook.push(prefix='barf')
