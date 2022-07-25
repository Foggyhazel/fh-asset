# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'assetInfo.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_AssetInfo(object):
    def setupUi(self, AssetInfo):
        if not AssetInfo.objectName():
            AssetInfo.setObjectName(u"AssetInfo")
        AssetInfo.resize(384, 448)
        self.verticalLayout_2 = QVBoxLayout(AssetInfo)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.asset_name = QLabel(AssetInfo)
        self.asset_name.setObjectName(u"asset_name")
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.asset_name.setFont(font)
        self.asset_name.setStyleSheet(u"")

        self.verticalLayout_3.addWidget(self.asset_name)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.asset_versionSelect = QComboBox(AssetInfo)
        self.asset_versionSelect.setObjectName(u"asset_versionSelect")
        self.asset_versionSelect.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.asset_versionSelect)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.scrollArea = QScrollArea(AssetInfo)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"QLabel[type=\"0\"] {\n"
"	color: rgb(158, 158, 158);\n"
"}\n"
"\n"
"QLabel[type=\"1\"] {\n"
"	margin-bottom: 4px;\n"
"}")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 364, 376))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.lb_description = QLabel(self.scrollAreaWidgetContents_2)
        self.lb_description.setObjectName(u"lb_description")
        self.lb_description.setStyleSheet(u"")
        self.lb_description.setProperty("type", 0)

        self.verticalLayout_4.addWidget(self.lb_description)

        self.asset_description = QLabel(self.scrollAreaWidgetContents_2)
        self.asset_description.setObjectName(u"asset_description")
        self.asset_description.setWordWrap(True)
        self.asset_description.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)
        self.asset_description.setProperty("type", 1)

        self.verticalLayout_4.addWidget(self.asset_description)

        self.lb_changes = QLabel(self.scrollAreaWidgetContents_2)
        self.lb_changes.setObjectName(u"lb_changes")
        self.lb_changes.setProperty("type", 0)

        self.verticalLayout_4.addWidget(self.lb_changes)

        self.asset_changes = QLabel(self.scrollAreaWidgetContents_2)
        self.asset_changes.setObjectName(u"asset_changes")
        self.asset_changes.setProperty("type", 1)

        self.verticalLayout_4.addWidget(self.asset_changes)

        self.lb_createdDate = QLabel(self.scrollAreaWidgetContents_2)
        self.lb_createdDate.setObjectName(u"lb_createdDate")
        self.lb_createdDate.setProperty("type", 0)

        self.verticalLayout_4.addWidget(self.lb_createdDate)

        self.asset_createdDate = QLabel(self.scrollAreaWidgetContents_2)
        self.asset_createdDate.setObjectName(u"asset_createdDate")
        self.asset_createdDate.setProperty("type", 1)

        self.verticalLayout_4.addWidget(self.asset_createdDate)

        self.lb_tags = QLabel(self.scrollAreaWidgetContents_2)
        self.lb_tags.setObjectName(u"lb_tags")
        self.lb_tags.setProperty("type", 0)

        self.verticalLayout_4.addWidget(self.lb_tags)

        self.asset_tags = QLabel(self.scrollAreaWidgetContents_2)
        self.asset_tags.setObjectName(u"asset_tags")
        self.asset_tags.setProperty("type", 1)

        self.verticalLayout_4.addWidget(self.asset_tags)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_3.addWidget(self.scrollArea)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)


        self.retranslateUi(AssetInfo)

        QMetaObject.connectSlotsByName(AssetInfo)
    # setupUi

    def retranslateUi(self, AssetInfo):
        AssetInfo.setWindowTitle(QCoreApplication.translate("AssetInfo", u"Form", None))
        self.asset_name.setText(QCoreApplication.translate("AssetInfo", u"Asset Name", None))
        self.asset_versionSelect.setCurrentText("")
        self.lb_description.setText(QCoreApplication.translate("AssetInfo", u"Description", None))
        self.asset_description.setText(QCoreApplication.translate("AssetInfo", u"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent eget volutpat velit, ut vulputate ligula. Donec placerat nulla vitae dolor ultrices, et mollis enim mattis. Ut egestas quam ex, quis tincidunt arcu tempus vel. Nullam dictum, enim nec tristique porttitor, ante ligula volutpat neque, sed fringilla ligula purus eget risus. Donec velit nisi, dictum ac suscipit vel, tincidunt eget lorem. Fusce arcu turpis, suscipit at convallis eu, efficitur at urna. Curabitur lorem tortor, blandit a metus sit amet, lobortis hendrerit massa. Suspendisse molestie justo vitae malesuada commodo. Fusce euismod leo id arcu semper, at finibus velit fermentum.", None))
        self.lb_changes.setText(QCoreApplication.translate("AssetInfo", u"Changes", None))
        self.asset_changes.setText(QCoreApplication.translate("AssetInfo", u"- shome changes", None))
        self.lb_createdDate.setText(QCoreApplication.translate("AssetInfo", u"Created", None))
        self.asset_createdDate.setText(QCoreApplication.translate("AssetInfo", u"16 Sep 2020", None))
        self.lb_tags.setText(QCoreApplication.translate("AssetInfo", u"Tags", None))
        self.asset_tags.setText(QCoreApplication.translate("AssetInfo", u"tagA, tagB, C", None))
    # retranslateUi

