# File content:
# Usage:

#coding=utf-8
from PySide2.QtWidgets import QVBoxLayout, QGroupBox, QHBoxLayout, QWidget


class BasicWidget(QWidget):
    def __init__(self):
        self.basic_main_lay = QVBoxLayout()
        self.display_group = QGroupBox()
        self.display_lay = QVBoxLayout()
        self.interactive_group = QGroupBox()
        self.interactive_lay = QHBoxLayout()
        self.left_group = QGroupBox()
        self.left_lay = QVBoxLayout()
        self.right_group = QGroupBox()
        self.right_lay = QHBoxLayout()

        self.display_group.setTitle('Display')
        self.display_group.setLayout(self.display_lay)
        self.interactive_group.setTitle('Interactive')
        self.interactive_group.setLayout(self.interactive_lay)
        # self.left_group.setTitle('Left')
        self.left_group.setLayout(self.left_lay)
        # self.right_group.setTitle('Right')
        self.right_group.setLayout(self.right_lay)

        self.interactive_lay.addWidget(self.left_group)
        self.interactive_lay.addWidget(self.right_group)
        self.basic_main_lay.addWidget(self.display_group)
        self.basic_main_lay.addWidget(self.interactive_group)

        super(BasicWidget, self).__init__()
        self.construct()
        self.set_lay()
        self.style_setting()

    def construct(self):
        pass

    def set_lay(self):
        self.setLayout(self.basic_main_lay)

    def style_setting(self):
        pass