# File content:
# Usage:

#coding=utf-8
from PySide2.QtWidgets import QTableWidget, QLineEdit, QPushButton, QHeaderView, QMessageBox

import CTRF_Customize
from CTRF_General.ClassRedefine import BasicWidget
from CTRF_General.Structure import Global
import General


class ExecuteWin(BasicWidget):
    def __init__(self):
        self.res_return_table = None
        self.request_receive_line = None
        self.submit_btn = None
        self.download_btn = None
        self.change_model_btn = None

        # self.Hits_range_line_text = None
        # self.num_for_require_line_text = None
        # self.key_words_line_text = None

        super(ExecuteWin, self).__init__()
        self.set_match_mode()
        self.slot_click_submit_btn()
        # self.slot_click_download_btn()
        self.slot_click_change_model_btn()

    def construct(self):
        self.res_return_table = QTableWidget()
        self.request_receive_line = QLineEdit()
        self.submit_btn = QPushButton()
        self.download_btn = QPushButton()
        self.change_model_btn = QPushButton()

        self.display_lay.addWidget(self.res_return_table)
        self.left_lay.addWidget(self.request_receive_line)
        self.right_lay.addWidget(self.submit_btn)
        self.right_lay.addWidget(self.download_btn)
        self.right_lay.addWidget(self.change_model_btn)

    def style_setting(self):
        self.submit_btn.setText('submit')
        self.download_btn.setText('download')
        self.change_model_btn.setText('change model')
        self.left_group.setTitle('input')
        self.right_group.setTitle('Fuc')

    def set_match_mode(self):
        self.display_group.setTitle(Global.current_mode)

        if Global.current_mode == 'Auto_mode':
            self.set_res_table_title(CTRF_Customize.auto_res_table_titles)
            self.request_receive_line.clear()
            self.request_receive_line.setPlaceholderText(CTRF_Customize.auto_input_tips)
        elif Global.current_mode == 'Specific_mode':
            self.set_res_table_title(CTRF_Customize.specific_res_table_idea_titles)
            self.request_receive_line.clear()
            self.request_receive_line.setPlaceholderText(CTRF_Customize.specific_input_tips)
        else:
            self.warning_box('Undefault mode have not add to selected_mode')

        self.res_return_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.res_return_table.alternatingRowColors()

    def set_res_table_title(self, mode_table_title):
        self.res_return_table.setColumnCount(len(mode_table_title))
        self.res_return_table.setHorizontalHeaderLabels(mode_table_title)

    def warning_box(self, warning_message):
        self.warning_widget = QMessageBox(QMessageBox.Warning,
                                   'Warning',
                                   '{}'.format(warning_message))
        self.warning_widget.addButton('OK', QMessageBox.YesRole)
        self.warning_widget.show()

    def slot_click_change_model_btn(self):
        self.change_model_btn.clicked.connect(self.click_change_model_btn)

    def click_change_model_btn(self):
        if Global.current_mode == 'Auto_mode':
            Global.current_mode = 'Specific_mode'
            self.set_match_mode()
        elif Global.current_mode == 'Specific_mode':
            Global.current_mode = 'Auto_mode'
            self.set_match_mode()

    def slot_click_submit_btn(self):
        self.submit_btn.clicked.connect(self.click_submit_btn)

    def click_submit_btn(self):
        request_receive_list = self.request_receive_line.text().split(',')
            # todo I/O parameters fuc
        if Global.current_mode == 'Auto_mode':
            if len(request_receive_list) > 3:
                warning_message = 'IndexError: Input list index out of range (3)\n' \
                                  'Solve: Check out your input values'
                self.warning_box(warning_message)
            # link to auto mode requests def
            else:
                print(request_receive_list)
        elif Global.current_mode == 'Specific_mode':
            # link to specific mode requests def XXX(aaa, *bbb):
            print(request_receive_list)

    def slot_click_download_btn(self):
        self.download_btn.clicked.connect(self.click_download_btn)

    def click_download_btn(self):
        General.Def.download_csv_from_qt_table(output_result_csv_dir=CTRF_Customize.output_result_csv_dir,
                                               table_widget=self.res_return_table)