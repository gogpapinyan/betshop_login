from PyQt5 import QtWidgets, QtCore
import sys
from os import path
from clipboard import copy
from conn import Ftp


class App(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()
        self.initUI()
        self.addPartners()

    def initUI(self):

        self.programPath = path.dirname(path.realpath(__file__))
        self.setObjectName("MainWindow")
        self.setWindowTitle('BetshopClient Login')
        self.setStyleSheet(self.createStyleSheet('stylesheet.css'))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setLayout(self.createLayout())
        self.left = 800
        self.right = 200
        self.width = 400
        self.height = 600
        self.setGeometry(self.left, self.right, self.width, self.height)
        self.adjustSize()
        self.show()

    def createStyleSheet(self, styleSheetName):

        styleSheetPath = self.programPath + path.sep + styleSheetName
        styleSheet = open(styleSheetPath, 'r').read()
        return styleSheet

    def createLayout(self):

        layout = QtWidgets.QVBoxLayout()
        titleWidget = self.createTitleWidget()
        layout.addWidget(titleWidget, 0)
        layout.addStretch(2)
        self.comboBoxWidget = self.createComboBoxWidget()
        self.comboBoxWidget.setObjectName('comboBoxWidget')
        layout.addWidget(self.comboBoxWidget, 1)
        layout.addStretch(1)
        infoWidget = self.createInfoWidget()
        layout.addWidget(infoWidget)
        buttonsWidget = self.createButtonsWidget()
        layout.addWidget(buttonsWidget, 2)
        return layout

    def createTitleWidget(self):
        titleWidget = QtWidgets.QWidget()
        titleWidget.setObjectName('Title')
        titleLayout = QtWidgets.QHBoxLayout()
        titleLabel = QtWidgets.QLabel('Test Login')
        titleLabel.setObjectName('TitleLabel')
        titleLayout.addWidget(titleLabel)
        titleWidget.setLayout(titleLayout)
        return titleWidget

    def createComboBoxWidget(self):

        comboBox = QtWidgets.QComboBox()
        return comboBox

    def createInfoWidget(self):

        infoWidget = QtWidgets.QWidget()
        infoLayout = QtWidgets.QVBoxLayout()
        infoTitle = QtWidgets.QLabel('Information')
        infoTitle.setObjectName('infoTitle')
        self.infoTextEdit = QtWidgets.QTextEdit()
        self.infoTextEdit.setObjectName('infoTextEdit')
        self.infoTextEdit.setReadOnly(True)
        infoLayout.addWidget(infoTitle)
        infoLayout.addStretch(1)
        infoLayout.addWidget(self.infoTextEdit)
        infoWidget.setLayout(infoLayout)
        return infoWidget

    def createButtonsWidget(self):
        buttonsWidget = QtWidgets.QWidget()
        buttonsLayout = QtWidgets.QHBoxLayout()

        loginCopyButton = QtWidgets.QPushButton('Login\ncopy')
        loginCopyButton.setObjectName('loginCopyButton')
        loginCopyButton.clicked.connect(self.onLoginCopy)

        passwordCopyButton = QtWidgets.QPushButton('Password\ncopy')
        passwordCopyButton.setObjectName('passwordCopyButton')
        passwordCopyButton.clicked.connect(self.onPasswordCopy)

        cancelButton = QtWidgets.QPushButton('Cancel')
        cancelButton.setObjectName('cancelButton')
        cancelButton.clicked.connect(self.onCancel)

        buttonsLayout.addWidget(loginCopyButton)
        buttonsLayout.addWidget(passwordCopyButton)
        buttonsLayout.addWidget(cancelButton)
        buttonsWidget.setLayout(buttonsLayout)
        return buttonsWidget

    def addPartners(self):
        connection = Ftp('10.25.57.73', 'admin', 'admin123')
        self.dictionaryPartners = connection.grabFile('partners.json')

        self.comboBoxWidget.currentIndexChanged.connect(self.onChangeInfo)
        for partner in self.dictionaryPartners:
            self.comboBoxWidget.addItem(partner)

    def onChangeInfo(self):
        partnerName = self.comboBoxWidget.currentText()
        # partnerIndex = self.comboBoxWidget.currentIndex()
        partnerUserName = self.dictionaryPartners[partnerName]['username']
        partnerPassword = self.dictionaryPartners[partnerName]['password']
        partnerId = self.dictionaryPartners[partnerName]['pid']
        information = f"Partner id: {partnerId} \n\nPartner name: {partnerName} \n\nTest user name: {partnerUserName}\n\nTest password: {partnerPassword}"
        self.infoTextEdit.setText(information)

    def onCancel(self):
        self.close()

    def onLoginCopy(self):
        partnerName = self.comboBoxWidget.currentText()
        if partnerName:
            partnerUserName = self.dictionaryPartners[partnerName]['username']
            copy(partnerUserName)

    def onPasswordCopy(self):
        partnerName = self.comboBoxWidget.currentText()
        if partnerName:
            partnerPassword = self.dictionaryPartners[partnerName]['password']
            copy(partnerPassword)

    def mousePressEvent(self, event):

        if event.buttons() == QtCore.Qt.RightButton:
            self.dragPos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):

        if event.buttons() == QtCore.Qt.RightButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()


app = QtWidgets.QApplication(sys.argv)
app.setApplicationName('Betshop Login')
app.setApplicationVersion('1.0.0')
instantApp = App()
sys.exit(app.exec())
