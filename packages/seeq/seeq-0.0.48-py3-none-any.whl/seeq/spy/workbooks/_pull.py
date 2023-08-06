import pandas as pd
import numpy as np

from seeq.sdk import *

from .. import _common
from .. import _login

from ._workbook import Workbook


def pull(workbooks):
    for index, row in workbooks.iterrows():
        if not _common.present(row, 'ID'):
            raise RuntimeError('All rows in "workbooks" argument must have valid "ID" column')

        if _common.get(row, 'Type') == 'Folder':
            continue

        workbook = Workbook(row['ID'])
