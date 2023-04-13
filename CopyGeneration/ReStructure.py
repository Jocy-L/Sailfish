from PySide2.QtWidgets import QLineEdit

table_titles = ['关键词', '标题', '描述1', '描述2']

request_dict = {
    'title': 'between 5 to 25',
    'description1': 'between 15 to 25',
    'description2': 'between 0 to 25'
}

class CustomLineEdit(QLineEdit):
    def __init__(self):
        super(CustomLineEdit, self).__init__()