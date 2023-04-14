# File content: Logical about window show, etc: widgets\slot\click event\logging...
# Usage: python "this file"

#coding=utf-8
import logging
import os
import sys
import openpyxl, pandas

from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QApplication, QTableWidget, \
    QHeaderView, QTableWidgetItem, QMessageBox

from AskToOpenAi import AskToOpenAi
from ReStructure import request_dict, table_titles, CustomLineEdit, result_filename, \
    LoggingInfo_filename


class AskWidget(QWidget):
    def __init__(self):
        self.logger = None
        self.run_ask = None
        self.key_words = None

        self.main_lay = None
        self.setting_lay = None
        self.condition_lay = None

        self.OPENAI_API_KEY = None

        self.request_items_num_lineEdit = None
        self.request_type = None
        self.request_key_words_lineEdit = None
        self.words_length = None
        self.submit_btn = None
        self.clear_btn = None
        self.download_btn = None
        self.result_show_table = None

        super(AskWidget, self).__init__()
        self.construt()
        self.slot_click_clear_btn()
        self.slot_click_submit_btn()
        self.slot_click_download_btn()
        self.logging_markdown()

    # widget name Instantiation
    def construt(self):
        self.logger = logging.getLogger()
        self.run_ask = AskToOpenAi()
        self.key_words = []
        self.request_type = ''

        self.main_lay = QVBoxLayout()
        self.setting_lay = QHBoxLayout()
        self.condition_lay = QVBoxLayout()

        self.OPENAI_API_KEY = QLineEdit()

        self.request_items_num_lineEdit = QLineEdit()
        self.request_key_words_lineEdit = CustomLineEdit()
        self.submit_btn = QPushButton('提交')
        self.clear_btn = QPushButton('清屏')
        self.download_btn = QPushButton('下载')
        self.result_show_table = QTableWidget()

        self.condition_lay.addWidget(self.OPENAI_API_KEY)
        self.condition_lay.addWidget(self.request_items_num_lineEdit)
        self.condition_lay.addWidget(self.request_key_words_lineEdit)

        self.setting_lay.addLayout(self.condition_lay)
        self.setting_lay.addWidget(self.submit_btn)
        self.setting_lay.addWidget(self.clear_btn)
        self.setting_lay.addWidget(self.download_btn)

        self.main_lay.addLayout(self.setting_lay)
        self.main_lay.addWidget(self.result_show_table)

        self.setLayout(self.main_lay)
        self.style_setting()

    # set default widget style
    def style_setting(self):
        self.logger.setLevel(logging.DEBUG)

        # condition_lay setting
        self.OPENAI_API_KEY.setPlaceholderText("请输入OPENAI_API_KEY")
        # Locked row edits and cannot change the number of requested items
        # self.request_items_num_lineEdit.setPlaceholderText("请输入需要获取多少条数据")
        self.request_items_num_lineEdit.setText('1')
        self.request_items_num_lineEdit.setReadOnly(True)
        self.request_key_words_lineEdit.setPlaceholderText("请输入关键词（文件）")

        # table style setting
        self.result_show_table.setColumnCount(len(table_titles))
        self.result_show_table.setHorizontalHeaderLabels(table_titles)
        self.result_show_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_show_table.alternatingRowColors()

    # btn clicked slot
    def slot_click_clear_btn(self):
        self.clear_btn.clicked.connect(self.click_clear_btn)

    def slot_click_download_btn(self):
        self.download_btn.clicked.connect(self.click_download_btn)

    def slot_click_submit_btn(self):
        self.submit_btn.clicked.connect(self.click_submit_btn)

    # btn click event
    def click_clear_btn(self):
        # result table clear up totally
        self.result_show_table.setRowCount(0)
        self.result_show_table.clearContents()

    def click_download_btn(self):
        try:
            wb = openpyxl.Workbook()
            columnHeaders = []
            output_cvs_name = result_filename()
            # create column header list
            for j in range(self.result_show_table.columnCount()):
                columnHeaders.append(self.result_show_table.horizontalHeaderItem(j).text())
            df = pandas.DataFrame(columns=columnHeaders)
            # print(df)

            # create dataframe object recordset
            for row in range(self.result_show_table.rowCount()):
                for col in range(self.result_show_table.columnCount()):
                    item = self.result_show_table.item(row, col)
                    df.at[row, columnHeaders[col]] = item.text() if item is not None else ""
            df.to_csv(output_cvs_name, index=False)

        except Exception as e:
            print(e)
            # self.warning_box('download')

    def click_submit_btn(self):
        try:
            self.run_ask.OPENAI_API_KEY = self.OPENAI_API_KEY.text()
            self.run_ask.request_items_num = self.request_items_num_lineEdit.text()

            self.create_key_words_list_from_file()
            if len(self.key_words) != 0:
                for key in self.key_words:
                    self.run_ask.request_key_words = key
                    self.run_ask_and_show_res()
            else:
                self.run_ask.request_key_words = self.request_key_words_lineEdit.text()
                self.run_ask_and_show_res()

        except Exception as e:
            print(e)
            # self.warning_box('submit')

    # Widgets Logical function module
    def create_key_words_list_from_file(self):
        file_name = self.request_key_words_lineEdit.text()
        is_file = os.path.isfile(file_name)

        if is_file:
            with open(file_name, 'r', encoding='utf-8') as f:
                for key in f.readlines():
                    self.key_words.append(key.strip('\n'))
        return is_file

    def run_ask_and_show_res(self):
        result = {}
        for key, value in request_dict.items():
            self.request_type = key
            self.words_length = value
            self.run_ask.request_type = self.request_type
            self.run_ask.words_length = self.words_length

            res = self.run_ask.run()
            result[key] = res

        self.result_show_table.insertRow(self.result_show_table.rowCount())
        row = self.result_show_table.rowCount() - 1
        self.result_show_table.setItem(row, 0, QTableWidgetItem(self.run_ask.request_key_words))
        for n, i in enumerate(result):
            self.result_show_table.setItem(row, n+1, QTableWidgetItem(result[i][0]))

    def logging_markdown(self):
        output_logging_txt = LoggingInfo_filename()
        file_handler = logging.FileHandler(output_logging_txt, mode='a+')
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def warning_box(self, site):
        self.warning_widget = QMessageBox(QMessageBox.Warning,
                                   'Warning',
                                   'Something is wrong in {}, please check by output logging!'.format(site))
        self.warning_widget.addButton('OK', QMessageBox.YesRole)
        self.warning_widget.show()


app = QApplication()
widget = AskWidget()
widget.resize(800, 600)
widget.show()
sys.exit(app.exec_())

# C:\Users\11\Desktop\11.txt