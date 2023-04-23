# File content:
# Usage:

#coding=utf-8
import datetime
import os
import socket

import openpyxl
import pandas


def current_user():
    HostName, LoginName = socket.gethostname(), os.getlogin()
    return HostName, LoginName

# combo dir and filename, if dir not exist will be created
def Download_dir_confirm(main_path, output_file_name):
    HostName, LoginName = current_user()
    main_dir = main_path.format(LoginName)
    download_file = os.path.join(main_dir, output_file_name)

    if not os.path.exists(main_dir):
        os.makedirs(main_dir)
    return download_file

def result_csv_filename(output_result_csv_dir):
    # C:\Users\XXX\AppData\Local\Temp\CopyGeneration
    # output_result_csv_dir = "C:\\Users\\{}\\AppData\\Local\\Temp\\CopyGeneration"
    output_file_name = 'result_csv_{}.csv'.format(datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S"))
    download_file = Download_dir_confirm(output_result_csv_dir, output_file_name)
    return download_file

def download_csv_from_qt_table(output_result_csv_dir, table_widget):
    try:
        wb = openpyxl.Workbook()
        columnHeaders = []
        output_cvs_name = result_csv_filename(output_result_csv_dir)
        # create column header list
        for j in range(table_widget.columnCount()):
            columnHeaders.append(table_widget.horizontalHeaderItem(j).text())
        df = pandas.DataFrame(columns=columnHeaders)

        # create dataframe object recordset
        for row in range(table_widget.rowCount()):
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                df.at[row, columnHeaders[col]] = item.text() if item is not None else ""
        df.to_csv(output_cvs_name, index=False)

        return True

    except Exception as e:
        # print(e)
        return False