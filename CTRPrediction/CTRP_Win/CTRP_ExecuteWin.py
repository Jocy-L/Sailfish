# File content:
# Usage:

#coding=utf-8
from PySide2.QtWidgets import QTableWidget, QLineEdit, QPushButton, QHeaderView, QMessageBox

from CTRP_Customize import auto_res_table_titles, specific_res_table_titles
from CTRP_general.ClassRedefine import BasicWidget
from CTRP_general.Structure import Global


class ExecuteWin(BasicWidget):
    def __init__(self):
        self.res_return_table = None
        # self.Hits_range = None
        # self.num_for_require = None
        self.input_line = None
        self.next_step_btn = None
        self.previous_step_btn = None
        self.change_model_btn = None

        super(ExecuteWin, self).__init__()

    def construct(self):
        self.res_return_table = QTableWidget()
        self.input_line = QLineEdit()
        self.next_step_btn = QPushButton()
        self.previous_step_btn = QPushButton()
        self.change_model_btn = QPushButton()

        self.display_lay.addWidget(self.res_return_table)
        self.left_lay.addWidget(self.input_line)
        self.right_lay.addWidget(self.next_step_btn)
        self.right_lay.addWidget(self.previous_step_btn)
        self.right_lay.addWidget(self.change_model_btn)

    def style_setting(self):
        self.input_line.setPlaceholderText('please input XXX')
        self.next_step_btn.setText('next')
        self.previous_step_btn.setText('previous')
        self.change_model_btn.setText('change model')
        self.left_group.setTitle('input')
        self.right_group.setTitle('Fuc')

        if Global.current_mode == 'Auto_mode':
            self.set_res_table_title(auto_res_table_titles)
        elif Global.current_mode == 'Specific_mode':
            self.set_res_table_title(specific_res_table_titles)
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