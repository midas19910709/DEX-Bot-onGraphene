# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dexbot/views/orig/create_bot_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(418, 474)
        Dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(179, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.cancel_button = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_2.addWidget(self.cancel_button)
        self.save_button = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_button.sizePolicy().hasHeightForWidth())
        self.save_button.setSizePolicy(sizePolicy)
        self.save_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_button.setObjectName("save_button")
        self.horizontalLayout_2.addWidget(self.save_button)
        self.gridLayout.addWidget(self.widget, 4, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_3)
        self.formLayout.setObjectName("formLayout")
        self.amount_label = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amount_label.sizePolicy().hasHeightForWidth())
        self.amount_label.setSizePolicy(sizePolicy)
        self.amount_label.setMinimumSize(QtCore.QSize(110, 0))
        self.amount_label.setMaximumSize(QtCore.QSize(110, 16777215))
        self.amount_label.setObjectName("amount_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.amount_label)
        self.amount_input = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amount_input.sizePolicy().hasHeightForWidth())
        self.amount_input.setSizePolicy(sizePolicy)
        self.amount_input.setMinimumSize(QtCore.QSize(140, 0))
        self.amount_input.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.amount_input.setDecimals(5)
        self.amount_input.setMaximum(999999999.999)
        self.amount_input.setObjectName("amount_input")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.amount_input)
        self.center_price_label = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.center_price_label.sizePolicy().hasHeightForWidth())
        self.center_price_label.setSizePolicy(sizePolicy)
        self.center_price_label.setMinimumSize(QtCore.QSize(110, 0))
        self.center_price_label.setMaximumSize(QtCore.QSize(110, 16777215))
        self.center_price_label.setObjectName("center_price_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.center_price_label)
        self.center_price_input = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.center_price_input.sizePolicy().hasHeightForWidth())
        self.center_price_input.setSizePolicy(sizePolicy)
        self.center_price_input.setMinimumSize(QtCore.QSize(140, 0))
        self.center_price_input.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.center_price_input.setAccelerated(False)
        self.center_price_input.setProperty("showGroupSeparator", False)
        self.center_price_input.setDecimals(5)
        self.center_price_input.setMinimum(-999999999.999)
        self.center_price_input.setMaximum(999999999.999)
        self.center_price_input.setObjectName("center_price_input")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.center_price_input)
        self.spread_label = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spread_label.sizePolicy().hasHeightForWidth())
        self.spread_label.setSizePolicy(sizePolicy)
        self.spread_label.setMinimumSize(QtCore.QSize(110, 0))
        self.spread_label.setMaximumSize(QtCore.QSize(110, 16777215))
        self.spread_label.setObjectName("spread_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.spread_label)
        self.spread_input = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spread_input.sizePolicy().hasHeightForWidth())
        self.spread_input.setSizePolicy(sizePolicy)
        self.spread_input.setMinimumSize(QtCore.QSize(140, 0))
        self.spread_input.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.spread_input.setMaximum(100000.0)
        self.spread_input.setProperty("value", 5.0)
        self.spread_input.setObjectName("spread_input")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spread_input)
        self.gridLayout.addWidget(self.groupBox_3, 2, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_2.setRowWrapPolicy(QtWidgets.QFormLayout.WrapLongRows)
        self.formLayout_2.setObjectName("formLayout_2")
        self.account_label = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.account_label.sizePolicy().hasHeightForWidth())
        self.account_label.setSizePolicy(sizePolicy)
        self.account_label.setMinimumSize(QtCore.QSize(110, 0))
        self.account_label.setMaximumSize(QtCore.QSize(110, 16777215))
        self.account_label.setObjectName("account_label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.account_label)
        self.account_input = QtWidgets.QLineEdit(self.groupBox_2)
        self.account_input.setObjectName("account_input")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.account_input)
        self.private_key_label = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.private_key_label.sizePolicy().hasHeightForWidth())
        self.private_key_label.setSizePolicy(sizePolicy)
        self.private_key_label.setMinimumSize(QtCore.QSize(110, 0))
        self.private_key_label.setMaximumSize(QtCore.QSize(110, 16777215))
        self.private_key_label.setScaledContents(False)
        self.private_key_label.setWordWrap(True)
        self.private_key_label.setObjectName("private_key_label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.private_key_label)
        self.private_key_input = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.private_key_input.sizePolicy().hasHeightForWidth())
        self.private_key_input.setSizePolicy(sizePolicy)
        self.private_key_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.private_key_input.setClearButtonEnabled(False)
        self.private_key_input.setObjectName("private_key_input")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.private_key_input)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout_3.setObjectName("formLayout_3")
        self.strategy_label = QtWidgets.QLabel(self.groupBox)
        self.strategy_label.setMinimumSize(QtCore.QSize(110, 0))
        self.strategy_label.setMaximumSize(QtCore.QSize(110, 16777215))
        self.strategy_label.setObjectName("strategy_label")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.strategy_label)
        self.strategy_input = QtWidgets.QComboBox(self.groupBox)
        self.strategy_input.setObjectName("strategy_input")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.strategy_input)
        self.bot_name_label = QtWidgets.QLabel(self.groupBox)
        self.bot_name_label.setMinimumSize(QtCore.QSize(110, 0))
        self.bot_name_label.setMaximumSize(QtCore.QSize(110, 16777215))
        self.bot_name_label.setObjectName("bot_name_label")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.bot_name_label)
        self.bot_name_input = QtWidgets.QLineEdit(self.groupBox)
        self.bot_name_input.setObjectName("bot_name_input")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.bot_name_input)
        self.base_asset_label = QtWidgets.QLabel(self.groupBox)
        self.base_asset_label.setMinimumSize(QtCore.QSize(110, 0))
        self.base_asset_label.setMaximumSize(QtCore.QSize(110, 16777215))
        self.base_asset_label.setObjectName("base_asset_label")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.base_asset_label)
        self.quote_asset_label = QtWidgets.QLabel(self.groupBox)
        self.quote_asset_label.setMinimumSize(QtCore.QSize(110, 0))
        self.quote_asset_label.setMaximumSize(QtCore.QSize(110, 16777215))
        self.quote_asset_label.setObjectName("quote_asset_label")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.quote_asset_label)
        self.quote_asset_input = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quote_asset_input.sizePolicy().hasHeightForWidth())
        self.quote_asset_input.setSizePolicy(sizePolicy)
        self.quote_asset_input.setMaximumSize(QtCore.QSize(80, 16777215))
        self.quote_asset_input.setObjectName("quote_asset_input")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.quote_asset_input)
        self.base_asset_input = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.base_asset_input.sizePolicy().hasHeightForWidth())
        self.base_asset_input.setSizePolicy(sizePolicy)
        self.base_asset_input.setMinimumSize(QtCore.QSize(105, 0))
        self.base_asset_input.setEditable(True)
        self.base_asset_input.setObjectName("base_asset_input")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.base_asset_input)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.amount_label.setBuddy(self.amount_input)
        self.center_price_label.setBuddy(self.center_price_input)
        self.spread_label.setBuddy(self.spread_input)
        self.account_label.setBuddy(self.account_input)
        self.private_key_label.setBuddy(self.private_key_input)
        self.strategy_label.setBuddy(self.strategy_input)
        self.bot_name_label.setBuddy(self.bot_name_input)
        self.quote_asset_label.setBuddy(self.quote_asset_input)

        self.retranslateUi(Dialog)
        self.strategy_input.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.strategy_input, self.bot_name_input)
        Dialog.setTabOrder(self.bot_name_input, self.quote_asset_input)
        Dialog.setTabOrder(self.quote_asset_input, self.account_input)
        Dialog.setTabOrder(self.account_input, self.private_key_input)
        Dialog.setTabOrder(self.private_key_input, self.amount_input)
        Dialog.setTabOrder(self.amount_input, self.center_price_input)
        Dialog.setTabOrder(self.center_price_input, self.spread_input)
        Dialog.setTabOrder(self.spread_input, self.save_button)
        Dialog.setTabOrder(self.save_button, self.cancel_button)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "DEXBot - Create Bot"))
        self.cancel_button.setText(_translate("Dialog", "Cancel"))
        self.save_button.setText(_translate("Dialog", "Save"))
        self.groupBox_3.setTitle(_translate("Dialog", "Bot Parameters"))
        self.amount_label.setText(_translate("Dialog", "Amount"))
        self.center_price_label.setText(_translate("Dialog", "Center Price"))
        self.spread_label.setText(_translate("Dialog", "Spread"))
        self.spread_input.setSuffix(_translate("Dialog", "%"))
        self.groupBox_2.setTitle(_translate("Dialog", "Bitshares Account Details"))
        self.account_label.setText(_translate("Dialog", "Account"))
        self.private_key_label.setText(_translate("Dialog", "Private Active Key"))
        self.groupBox.setTitle(_translate("Dialog", "Bot Details"))
        self.strategy_label.setText(_translate("Dialog", "Strategy"))
        self.bot_name_label.setText(_translate("Dialog", "Bot Name"))
        self.base_asset_label.setText(_translate("Dialog", "Base Asset"))
        self.quote_asset_label.setText(_translate("Dialog", "Quote Asset"))

