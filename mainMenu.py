# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainMenu.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(450, 600)
        font = QtGui.QFont()
        font.setFamily("Kaufmann BT")
        mainWindow.setFont(font)
        mainWindow.setWindowOpacity(1.0)
        mainWindow.setWhatsThis("")
        mainWindow.setAccessibleName("")
        mainWindow.setAccessibleDescription("")
        mainWindow.setAutoFillBackground(False)
        mainWindow.setDocumentMode(False)
        mainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        mainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        font = QtGui.QFont()
        font.setFamily("Kaufmann BT")
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(90, 150, 261, 371))
        self.frame.setAutoFillBackground(False)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(2)
        self.frame.setObjectName("frame")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(100, 60, 241, 451))
        self.widget.setObjectName("widget")
        self.general_lo = QtWidgets.QVBoxLayout(self.widget)
        self.general_lo.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.general_lo.setContentsMargins(0, 0, 0, 0)
        self.general_lo.setSpacing(0)
        self.general_lo.setObjectName("general_lo")
        self.title_lb = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Kaufmann BT")
        font.setPointSize(35)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.title_lb.setFont(font)
        self.title_lb.setAutoFillBackground(False)
        self.title_lb.setScaledContents(False)
        self.title_lb.setAlignment(QtCore.Qt.AlignCenter)
        self.title_lb.setWordWrap(False)
        self.title_lb.setObjectName("title_lb")
        self.general_lo.addWidget(self.title_lb)
        self.butt_lo = QtWidgets.QVBoxLayout()
        self.butt_lo.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.butt_lo.setContentsMargins(-1, -1, -1, 10)
        self.butt_lo.setSpacing(36)
        self.butt_lo.setObjectName("butt_lo")
        self.face_detect_bt = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(11)
        self.face_detect_bt.setFont(font)
        self.face_detect_bt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.face_detect_bt.setObjectName("face_detect_bt")
        self.butt_lo.addWidget(self.face_detect_bt)
        self.face_db_bt = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Kaufmann BT")
        font.setPointSize(11)
        self.face_db_bt.setFont(font)
        self.face_db_bt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.face_db_bt.setObjectName("face_db_bt")
        self.butt_lo.addWidget(self.face_db_bt)
        self.face_recogn_bt = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(11)
        self.face_recogn_bt.setFont(font)
        self.face_recogn_bt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.face_recogn_bt.setObjectName("face_recogn_bt")
        self.butt_lo.addWidget(self.face_recogn_bt)
        self.info_bt = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(11)
        self.info_bt.setFont(font)
        self.info_bt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.info_bt.setObjectName("info_bt")
        self.butt_lo.addWidget(self.info_bt)
        self.exit_bt = QtWidgets.QPushButton(self.widget)
        self.exit_bt.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(11)
        self.exit_bt.setFont(font)
        self.exit_bt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exit_bt.setMouseTracking(False)
        self.exit_bt.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.exit_bt.setAutoFillBackground(False)
        self.exit_bt.setShortcut("")
        self.exit_bt.setAutoDefault(False)
        self.exit_bt.setDefault(False)
        self.exit_bt.setObjectName("exit_bt")
        self.butt_lo.addWidget(self.exit_bt)
        self.butt_lo.setStretch(0, 1)
        self.butt_lo.setStretch(1, 1)
        self.butt_lo.setStretch(2, 1)
        self.butt_lo.setStretch(3, 1)
        self.butt_lo.setStretch(4, 40)
        self.general_lo.addLayout(self.butt_lo)
        self.general_lo.setStretch(0, 1)
        self.general_lo.setStretch(1, 4)
        self.frame.raise_()
        self.title_lb.raise_()
        self.face_detect_bt.raise_()
        self.face_db_bt.raise_()
        self.face_recogn_bt.raise_()
        self.info_bt.raise_()
        self.exit_bt.raise_()
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Главное меню"))
        self.title_lb.setText(_translate("mainWindow", "VisFace"))
        self.face_detect_bt.setText(_translate("mainWindow", "Определение лиц"))
        self.face_db_bt.setText(_translate("mainWindow", "База лиц"))
        self.face_recogn_bt.setText(_translate("mainWindow", "Распознавание лиц"))
        self.info_bt.setText(_translate("mainWindow", "О программе"))
        self.exit_bt.setText(_translate("mainWindow", "Выход"))
