import sys

from PySide2.QtWidgets import QVBoxLayout, QGroupBox, QHBoxLayout, QWidget, QApplication


class BasicWidget(QWidget):
    def __init__(self):
        self.basic_main_lay = None
        self.display_group = None
        self.display_lay = None
        self.interactive_group = None
        self.interactive_lay = None
        self.input_group = None
        self.input_lay = None
        self.fuc_group = None
        self.fuc_lay = None

        super(BasicWidget, self).__init__()
        self.construct()
        self.set_lay()

    def construct(self):
        self.basic_main_lay = QVBoxLayout()
        self.display_group = QGroupBox()
        self.display_lay = QVBoxLayout()
        self.interactive_group = QGroupBox()
        self.interactive_lay = QHBoxLayout()
        self.input_group = QGroupBox()
        self.input_lay = QVBoxLayout()
        self.fuc_group = QGroupBox()
        self.fuc_lay = QHBoxLayout()

        self.display_group.setLayout(self.display_lay)
        self.input_group.setLayout(self.input_lay)
        self.fuc_group.setLayout(self.fuc_lay)
        self.interactive_group.setLayout(self.interactive_lay)
        self.interactive_lay.addWidget(self.input_group)
        self.interactive_lay.addWidget(self.fuc_group)
        self.basic_main_lay.addWidget(self.display_group)
        self.basic_main_lay.addWidget(self.interactive_group)

        self.style_setting()

    def set_lay(self):
        self.setLayout(self.basic_main_lay)

    def style_setting(self):
        pass

app = QApplication()
widget = BasicWidget()
widget.resize(400, 200)
widget.show()
sys.exit(app.exec_())