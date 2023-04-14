# File content: Including Custom modules about in/output and generic methods and class refactoring modules
# Usage: import modules

#coding=utf-8
import datetime
import os

import socket
from PySide2.QtWidgets import QLineEdit

# Custom modules: custom information reset in this part and no more other parts support to user except developer
table_titles = ['关键词', '标题', '描述1', '描述2']

request_dict = {
    'title': 'between 5 to 25',
    'words1': 'more than 10 and less than 20',
    'words2': 'between 0 to 15'
}

output_result_csv_dir = "C:\\Users\\{}\\AppData\\Local\\Temp\\CopyGeneration"
output_logging_txt_dir = "C:\\Users\\{}\\AppData\\Local\\Temp\\CopyGeneration\\logging"

# ----------------------------------------------------------------------------------------------------------------------
# Customization part finished and next part is sys need function


# About generic methods and class refactoring modules
def current_user():
    HostName, LoginName = socket.gethostname(), os.getlogin()
    return HostName, LoginName

def result_filename():
    # C:\Users\11\AppData\Local\Temp\CopyGeneration
    output_file_name = 'result_csv_{}.csv'.format(datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S"))
    download_file = Download_dir_confirm(output_result_csv_dir, output_file_name)
    return download_file

def LoggingInfo_filename():
    # C:\Users\11\AppData\Local\Temp\CopyGeneration\logging
    output_file_name = 'logging_{}.txt'.format(datetime.datetime.now().strftime("%Y-%m-%d"))
    download_file = Download_dir_confirm(output_logging_txt_dir, output_file_name)
    return download_file

# combo dir and filename, if dir not exist will be created
def Download_dir_confirm(main_path, output_file_name):
    HostName, LoginName = current_user()
    main_dir = main_path.format(LoginName)
    download_file = os.path.join(main_dir, output_file_name)

    if not os.path.exists(main_dir):
        os.makedirs(main_dir)
    return download_file

class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(CustomLineEdit, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        path_str = event.mimeData().urls()
        path_str = path_str[0].path().lstrip("/").replace("/", "//")
        self.setText(str(path_str))