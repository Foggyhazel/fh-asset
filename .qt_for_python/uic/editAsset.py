# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editAsset.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_EditAsset(object):
    def setupUi(self, EditAsset):
        if not EditAsset.objectName():
            EditAsset.setObjectName(u"EditAsset")
        EditAsset.resize(459, 407)
        self.formLayout_2 = QFormLayout(EditAsset)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lb_type = QLabel(EditAsset)
        self.lb_type.setObjectName(u"lb_type")
        self.lb_type.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lb_type)

        self.asset_type = QLabel(EditAsset)
        self.asset_type.setObjectName(u"asset_type")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asset_type.sizePolicy().hasHeightForWidth())
        self.asset_type.setSizePolicy(sizePolicy)
        self.asset_type.setMinimumSize(QSize(0, 0))
        self.asset_type.setLayoutDirection(Qt.LeftToRight)
        self.asset_type.setAutoFillBackground(False)
        self.asset_type.setFrameShape(QFrame.NoFrame)
        self.asset_type.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.asset_type.setMargin(0)
        self.asset_type.setOpenExternalLinks(False)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.asset_type)

        self.lb_title = QLabel(EditAsset)
        self.lb_title.setObjectName(u"lb_title")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lb_title)

        self.asset_title = QLineEdit(EditAsset)
        self.asset_title.setObjectName(u"asset_title")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.asset_title)

        self.lb_version = QLabel(EditAsset)
        self.lb_version.setObjectName(u"lb_version")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lb_version)

        self.asset_version = QLineEdit(EditAsset)
        self.asset_version.setObjectName(u"asset_version")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.asset_version)

        self.lb_tags = QLabel(EditAsset)
        self.lb_tags.setObjectName(u"lb_tags")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lb_tags)

        self.asset_tags = QLineEdit(EditAsset)
        self.asset_tags.setObjectName(u"asset_tags")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.asset_tags)

        self.lb_description = QLabel(EditAsset)
        self.lb_description.setObjectName(u"lb_description")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lb_description)

        self.asset_description = QTextEdit(EditAsset)
        self.asset_description.setObjectName(u"asset_description")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.asset_description)

        self.lb_preview = QLabel(EditAsset)
        self.lb_preview.setObjectName(u"lb_preview")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.lb_preview)

        self.preview_layout = QHBoxLayout()
        self.preview_layout.setObjectName(u"preview_layout")
        self.asset_preview = QLabel(EditAsset)
        self.asset_preview.setObjectName(u"asset_preview")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.asset_preview.sizePolicy().hasHeightForWidth())
        self.asset_preview.setSizePolicy(sizePolicy1)
        self.asset_preview.setMinimumSize(QSize(100, 100))
        self.asset_preview.setAutoFillBackground(False)
        self.asset_preview.setStyleSheet(u"border:1px solid rgb(192, 192, 192); \n"
"border-radius: 2px;")
        self.asset_preview.setFrameShape(QFrame.NoFrame)

        self.preview_layout.addWidget(self.asset_preview)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_capture = QPushButton(EditAsset)
        self.btn_capture.setObjectName(u"btn_capture")

        self.verticalLayout.addWidget(self.btn_capture)

        self.btn_choose = QPushButton(EditAsset)
        self.btn_choose.setObjectName(u"btn_choose")

        self.verticalLayout.addWidget(self.btn_choose)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btn_clear = QPushButton(EditAsset)
        self.btn_clear.setObjectName(u"btn_clear")

        self.verticalLayout.addWidget(self.btn_clear)


        self.preview_layout.addLayout(self.verticalLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.preview_layout.addItem(self.horizontalSpacer)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.preview_layout)


        self.formLayout_2.setLayout(0, QFormLayout.SpanningRole, self.formLayout)

        self.form_buttons = QDialogButtonBox(EditAsset)
        self.form_buttons.setObjectName(u"form_buttons")
        self.form_buttons.setAutoFillBackground(False)
        self.form_buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.form_buttons.setCenterButtons(False)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.form_buttons)


        self.retranslateUi(EditAsset)

        QMetaObject.connectSlotsByName(EditAsset)
    # setupUi

    def retranslateUi(self, EditAsset):
        EditAsset.setWindowTitle(QCoreApplication.translate("EditAsset", u"Form", None))
        self.lb_type.setText(QCoreApplication.translate("EditAsset", u"Type", None))
        self.asset_type.setText(QCoreApplication.translate("EditAsset", u"TextLabel", None))
        self.lb_title.setText(QCoreApplication.translate("EditAsset", u"Asset Name", None))
        self.lb_version.setText(QCoreApplication.translate("EditAsset", u"Version", None))
        self.lb_tags.setText(QCoreApplication.translate("EditAsset", u"Tags", None))
        self.lb_description.setText(QCoreApplication.translate("EditAsset", u"Description", None))
        self.lb_preview.setText(QCoreApplication.translate("EditAsset", u"Preview", None))
        self.asset_preview.setText(QCoreApplication.translate("EditAsset", u"TextLabel", None))
        self.btn_capture.setText(QCoreApplication.translate("EditAsset", u"Capture", None))
        self.btn_choose.setText(QCoreApplication.translate("EditAsset", u"Choose..", None))
        self.btn_clear.setText(QCoreApplication.translate("EditAsset", u"Clear", None))
    # retranslateUi

