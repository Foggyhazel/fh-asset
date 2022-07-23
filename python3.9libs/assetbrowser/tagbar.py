from PySide2.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QSizePolicy,
    QFrame,
    QApplication,
    QLabel,
    QPushButton
)
import sys
from functools import partial
import re


class TagBar(QWidget):
    """
    tag edit ui
    edited from https://robonobodojo.wordpress.com/2018/09/11/creating-a-tag-bar-in-pyside/
    """

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle('Tag Bar')
        self.tags = []
        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(4)
        self.setLayout(self.h_layout)
        self.line_edit = QLineEdit()
        self.line_edit.setSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.setSizePolicy(QSizePolicy.Minimum,
                           QSizePolicy.Minimum)
        # self.setContentsMargins(2, 2, 2, 2)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.refresh()
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.line_edit.returnPressed.connect(self.create_tags)
        # cause crash when try to delete tag
        # self.line_edit.editingFinished.connect(self.create_tags)

    def create_tags(self):
        new_tags = [s for s in re.split(r'\W+', self.line_edit.text()) if s]
        self.line_edit.setText('')
        self.tags.extend(new_tags)
        self.tags = list(set(self.tags))
        self.tags.sort(key=lambda x: x.lower())
        self.refresh()

    def refresh(self):
        while(self.h_layout.count()):
            child = self.h_layout.takeAt(0)
            child.widget().setParent(None)
        for tag in self.tags:
            self.add_tag_to_bar(tag)
        self.h_layout.addWidget(self.line_edit)
        self.line_edit.setFocus()

    def add_tag_to_bar(self, text):
        tag = QFrame()
        tag.setStyleSheet(
            'border:1px solid rgb(192, 192, 192); border-radius: 4px;')
        tag.setContentsMargins(2, 2, 2, 2)
        # tag.setFixedHeight(20)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(4, 4, 4, 4)
        hbox.setSpacing(10)
        tag.setLayout(hbox)
        label = QLabel(text)
        label.setStyleSheet('border:0px')
        label.setFixedHeight(16)
        hbox.addWidget(label)
        x_button = QPushButton('x')
        x_button.setFixedSize(20, 20)
        x_button.setStyleSheet('border:0px; font-weight:bold')
        x_button.setSizePolicy(QSizePolicy.Maximum,
                               QSizePolicy.Maximum)
        x_button.clicked.connect(partial(self.delete_tag, text))
        hbox.addWidget(x_button)
        tag.setSizePolicy(QSizePolicy.Maximum,
                          QSizePolicy.Preferred)
        self.h_layout.addWidget(tag)

    def delete_tag(self, tag_name):
        self.tags.remove(tag_name)
        self.refresh()