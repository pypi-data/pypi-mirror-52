# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galacteek/ui/profileeditdialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProfileEditDialog(object):
    def setupUi(self, ProfileEditDialog):
        ProfileEditDialog.setObjectName("ProfileEditDialog")
        ProfileEditDialog.resize(621, 400)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ProfileEditDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(ProfileEditDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 6, 0, 1, 1)
        self.username = QtWidgets.QLineEdit(self.tab)
        self.username.setMaxLength(128)
        self.username.setObjectName("username")
        self.gridLayout_2.addWidget(self.username, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)
        self.firstname = QtWidgets.QLineEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.firstname.sizePolicy().hasHeightForWidth())
        self.firstname.setSizePolicy(sizePolicy)
        self.firstname.setMaxLength(64)
        self.firstname.setObjectName("firstname")
        self.gridLayout_2.addWidget(self.firstname, 4, 1, 1, 1)
        self.profileCryptoId = QtWidgets.QLabel(self.tab)
        self.profileCryptoId.setText("")
        self.profileCryptoId.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.profileCryptoId.setObjectName("profileCryptoId")
        self.gridLayout_2.addWidget(self.profileCryptoId, 13, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 7, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 4, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 8, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.gridLayout_2.addItem(spacerItem, 11, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 5, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 13, 0, 1, 1)
        self.lastname = QtWidgets.QLineEdit(self.tab)
        self.lastname.setMaxLength(128)
        self.lastname.setObjectName("lastname")
        self.gridLayout_2.addWidget(self.lastname, 5, 1, 1, 1)
        self.labelWarning = QtWidgets.QLabel(self.tab)
        self.labelWarning.setWordWrap(True)
        self.labelWarning.setObjectName("labelWarning")
        self.gridLayout_2.addWidget(self.labelWarning, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout_2.addItem(spacerItem1, 3, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 10, 0, 1, 1)
        self.countryBox = QtWidgets.QComboBox(self.tab)
        self.countryBox.setObjectName("countryBox")
        self.gridLayout_2.addWidget(self.countryBox, 10, 1, 1, 1)
        self.email = QtWidgets.QLineEdit(self.tab)
        self.email.setMaxLength(128)
        self.email.setObjectName("email")
        self.gridLayout_2.addWidget(self.email, 6, 1, 1, 1)
        self.org = QtWidgets.QLineEdit(self.tab)
        self.org.setMaxLength(128)
        self.org.setObjectName("org")
        self.gridLayout_2.addWidget(self.org, 7, 1, 1, 1)
        self.city = QtWidgets.QLineEdit(self.tab)
        self.city.setObjectName("city")
        self.gridLayout_2.addWidget(self.city, 8, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 9, 0, 1, 1)
        self.gender = QtWidgets.QComboBox(self.tab)
        self.gender.setObjectName("gender")
        self.gridLayout_2.addWidget(self.gender, 9, 1, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.iconHash = QtWidgets.QLabel(self.tab_2)
        self.iconHash.setText("")
        self.iconHash.setObjectName("iconHash")
        self.verticalLayout_4.addWidget(self.iconHash)
        self.iconPixmap = QtWidgets.QLabel(self.tab_2)
        self.iconPixmap.setText("")
        self.iconPixmap.setObjectName("iconPixmap")
        self.verticalLayout_4.addWidget(self.iconPixmap)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.changeIconButton = QtWidgets.QPushButton(self.tab_2)
        self.changeIconButton.setObjectName("changeIconButton")
        self.verticalLayout_4.addWidget(self.changeIconButton)
        self.verticalLayout_3.addLayout(self.verticalLayout_4)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.bio = QtWidgets.QTextEdit(self.tab_3)
        self.bio.setObjectName("bio")
        self.verticalLayout_5.addWidget(self.bio)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cancelButton = QtWidgets.QPushButton(ProfileEditDialog)
        self.cancelButton.setMaximumSize(QtCore.QSize(120, 16777215))
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.updateButton = QtWidgets.QPushButton(ProfileEditDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.updateButton.sizePolicy().hasHeightForWidth())
        self.updateButton.setSizePolicy(sizePolicy)
        self.updateButton.setMaximumSize(QtCore.QSize(120, 16777215))
        self.updateButton.setObjectName("updateButton")
        self.horizontalLayout_2.addWidget(self.updateButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(ProfileEditDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ProfileEditDialog)

    def retranslateUi(self, ProfileEditDialog):
        _translate = QtCore.QCoreApplication.translate
        ProfileEditDialog.setWindowTitle(_translate("ProfileEditDialog", "Dialog"))
        self.label_4.setText(_translate("ProfileEditDialog", "Email"))
        self.label.setText(_translate("ProfileEditDialog", "Username"))
        self.label_6.setText(_translate("ProfileEditDialog", "Organization"))
        self.label_2.setText(_translate("ProfileEditDialog", "First name"))
        self.label_8.setText(_translate("ProfileEditDialog", "City"))
        self.label_3.setText(_translate("ProfileEditDialog", "Last name"))
        self.label_5.setText(_translate("ProfileEditDialog", "Current cryptographic identifier"))
        self.labelWarning.setText(_translate("ProfileEditDialog", "Only the username is strictly required"))
        self.label_7.setText(_translate("ProfileEditDialog", "Country"))
        self.label_9.setText(_translate("ProfileEditDialog", "Gender"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("ProfileEditDialog", "User information"))
        self.changeIconButton.setText(_translate("ProfileEditDialog", "Change Icon"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("ProfileEditDialog", "Avatar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("ProfileEditDialog", "Bio"))
        self.cancelButton.setText(_translate("ProfileEditDialog", "Cancel"))
        self.updateButton.setText(_translate("ProfileEditDialog", "Update"))

