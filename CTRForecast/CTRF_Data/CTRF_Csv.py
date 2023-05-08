# File content:
# Usage:

#coding=utf-8
import datetime
import os

import pandas as pd
from pathlib import Path

from CTRF_General.Language import language


def csv_read_current_column(file, columns):
    columns_mes = {}
    # pd.read_csv("file path", skiprows=9, nrows=5)，ignore 9 rows [0:8]，read follow 5 rows
    df = pd.read_csv(file, skiprows=5, encoding='gbk')
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    for i in columns:
        column_mes_list = []
        # <class 'pandas.core.series.Series'>
        column_mes = df[i]
        for item in column_mes.values:
            column_mes_list.append(item)
        columns_mes[language[i]] = column_mes_list

    # print(columns_mes)
    return columns_mes

def create_update_datafile_save_dir():
    path_dir = 'E:\\Project\\CTRF\\Data\\Columns\\{}'.format(datetime.date.today())
    if os.path.isdir(path_dir):
        pass
    else:
        os.makedirs(path_dir)
    return path_dir

def create_update_datafile_save_file(columns_mes):
    for key in columns_mes.keys():
        path_dir = create_update_datafile_save_dir()
        with open(os.path.join(path_dir, '{}.txt'.format(key)), 'a+') as f:
            f.write(str(columns_mes[key]))
    return True


