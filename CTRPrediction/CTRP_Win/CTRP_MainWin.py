# File content:
# Usage:

#coding=utf-8
import sys

from PySide2.QtWidgets import QApplication, QLabel, QPushButton

from CTRP_Customize import window_size
from CTRP_Win.CTRP_ExecuteWin import ExecuteWin
from CTRP_general.ClassRedefine import BasicWidget
from CTRP_general.Structure import Global


class CTRP_MainWin(BasicWidget):
    def __init__(self):
        self.tips_label = None
        self.auto_btn = None
        self.assigned_btn = None

        super(CTRP_MainWin, self).__init__()
        self.slot_click_auto_btn()

    def construct(self):
        self.tips_label = QLabel()
        self.auto_btn = QPushButton()
        self.assigned_btn = QPushButton()
        self.display_lay.addWidget(self.tips_label)
        self.left_lay.addWidget(self.auto_btn)
        self.right_lay.addWidget(self.assigned_btn)

    def style_setting(self):
        self.tips_label.setText("Which U Want")
        self.auto_btn.setText('Auto_mode')
        self.assigned_btn.setText('Specific_mode')
        self.display_group.setMaximumSize(800, 50)
        self.auto_btn.setMaximumSize(250, 250)
        self.assigned_btn.setMaximumSize(250, 250)

    def slot_click_auto_btn(self):
        self.auto_btn.clicked.connect(self.click_auto_btn)

    def click_auto_btn(self):
        self.auto_widget = ExecuteWin()
        self.auto_widget.resize(window_size['weight'], window_size['height'])
        self.auto_widget.show()
        # self.hide()

        Global.current_mode = self.auto_btn.text()


app = QApplication()
widget = CTRP_MainWin()
widget.resize(window_size['weight'], window_size['height'])
widget.show()
sys.exit(app.exec_())