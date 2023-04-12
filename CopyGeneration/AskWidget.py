import sys

from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QTextBrowser, QLineEdit, QPushButton, \
    QApplication, QLabel

from CopyGeneration.AskToOpenAi import AskToOpenAi


class AskWidget(QWidget):
    def __init__(self):
        self.main_lay = None
        self.setting_lay = None
        self.condition_lay = None

        self.OPENAI_API_KEY = None

        self.request_items_num_combo = None
        self.request_type_combo = None
        self.request_key_words_lineEdit = None
        self.words_legth = None
        self.submit_btn = None
        self.clear_btn = None
        self.result_show_textBrowser = None

        super(AskWidget, self).__init__()
        self.construt()
        self.slot_click_clear_btn()
        self.slot_click_submit_btn()
        self.words_limite()

    def construt(self):
        self.main_lay = QVBoxLayout()
        self.setting_lay = QHBoxLayout()
        self.condition_lay = QVBoxLayout()

        self.OPENAI_API_KEY = QLineEdit()

        self.request_items_num_lineEdit = QLineEdit()
        self.request_type_combo = QComboBox()
        self.request_key_words_lineEdit = QLineEdit()
        self.submit_btn = QPushButton('提交')
        self.clear_btn = QPushButton('清屏')
        self.result_show_textBrowser = QTextBrowser()

        self.condition_lay.addWidget(self.OPENAI_API_KEY)
        self.condition_lay.addWidget(self.request_items_num_lineEdit)
        self.condition_lay.addWidget(self.request_key_words_lineEdit)
        self.condition_lay.addWidget(QLabel('内容类型'))
        self.condition_lay.addWidget(self.request_type_combo)
        self.condition_lay.addWidget(QLabel('内容字数'))

        self.setting_lay.addLayout(self.condition_lay)
        self.setting_lay.addWidget(self.submit_btn)
        self.setting_lay.addWidget(self.clear_btn)

        self.main_lay.addLayout(self.setting_lay)
        self.main_lay.addWidget(self.result_show_textBrowser)

        self.setLayout(self.main_lay)
        self.condition_setting()

    def condition_setting(self):
        request_type_combo_list = ['title', 'description']

        self.request_type_combo.addItems(request_type_combo_list)

        self.OPENAI_API_KEY.setPlaceholderText("请输入OPENAI_API_KEY")
        self.request_items_num_lineEdit.setPlaceholderText("请输入需要获取多少条数据")
        self.request_key_words_lineEdit.setPlaceholderText("请输入关键词")

    def words_limite(self):
        words_legth_combo_list = ['less than 10', 'more than 10 words and less than 15']
        if self.request_type_combo.currentText() == 'title':
            self.words_legth = words_legth_combo_list[0]
        else:
            self.words_legth = words_legth_combo_list[1]

    def slot_click_clear_btn(self):
        self.clear_btn.clicked.connect(self.click_clear_btn)

    def click_clear_btn(self):
        self.result_show_textBrowser.clear()

    def slot_click_submit_btn(self):
        self.submit_btn.clicked.connect(self.click_submit_btn)

    def click_submit_btn(self):
        try:
            run_ask = AskToOpenAi()
            run_ask.OPENAI_API_KEY = self.OPENAI_API_KEY.text()
            run_ask.request_items_num = self.request_items_num_lineEdit.text()
            run_ask.request_key_words = self.request_key_words_lineEdit.text()
            run_ask.request_type = self.request_type_combo.currentText()
            run_ask.words_legth = self.words_legth
            res = run_ask.run()
            self.result_show_textBrowser.append('Items: ' + str(len(res)))
            for text in res:
                self.result_show_textBrowser.append(str(text))
            self.result_show_textBrowser.append('\n')
        except EOFError as e:
            self.result_show_textBrowser.append(e)


app = QApplication()
widget = AskWidget()
widget.resize(800, 600)
widget.show()
sys.exit(app.exec_())