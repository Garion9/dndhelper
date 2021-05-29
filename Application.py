import sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, \
    QLineEdit, QGroupBox, QFormLayout, QMainWindow, QStackedLayout
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QRegExpValidator
from User_Module import *

app = QApplication(sys.argv)
mainWindow = QMainWindow()
user = None

def main():
    mainWindow.setWindowTitle("DND Helper")
    mainWindow.setMinimumWidth(1400)
    mainWindow.setMinimumHeight(700)
    mainWindow.setStyleSheet("background: #00b4ff;")

    login_frame()
    #register_frame()

    mainWindow.show()
    sys.exit(app.exec())

def login_frame():
    def login():
        userLogin = loginInput.text()
        userPassword = passwordInput.text()
        try:
            if authenticate_user(userLogin, userPassword):
                global user
                user = DatabaseHandler.get_user(userLogin)
                test_frame()
            else:
                statusMessage.setText("Password is incorrect.")
                #layout.addWidget(QLabel("Password is incorrect."))
        except TypeError as err:
            statusMessage.setText(err.__str__())
            #layout.addWidget(QLabel(err.__str__()))

    def register():
        register_frame()

    loginWindow = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(QtCore.Qt.AlignCenter)
    titleLabel = QLabel("DND HELPER")
    titleLabel.setStyleSheet('''
        font-size: 75px;
        font-weight: bold;
        border: 15px inset lightgreen;
        padding: 20px;
        margin-bottom: 50px;
        ''')
    titleLabel.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(titleLabel)

    loginForm = QGroupBox()
    loginForm.setMaximumWidth(600)
    loginForm.setStyleSheet('''
        border: none;
        margin: 0px 125px;
    ''')
    loginForm.setAlignment(QtCore.Qt.AlignCenter)
    loginFormLayout = QFormLayout()
    loginFormLayout.setAlignment(QtCore.Qt.AlignHCenter)
    loginFormLayout.setLabelAlignment(QtCore.Qt.AlignHCenter)
    loginInput = QLineEdit()
    loginInput.setFixedWidth(200)
    loginInput.setStyleSheet('''
        border: 1px solid black;
        margin: 0px;
        height: 25px;
        font-size: 15px;
    ''')
    loginLabel = QLabel("Login:")
    loginLabel.setStyleSheet('''
        margin: 0px;
        font-size: 15px;
    ''')
    loginFormLayout.addRow(loginLabel, loginInput)
    passwordInput = QLineEdit()
    passwordInput.setFixedWidth(200)
    passwordInput.setStyleSheet('''
       border: 1px solid black;
       margin: 0px;
       height: 25px;
       font-size: 15px;
   ''')
    passwordInput.setEchoMode(QLineEdit.Password)
    passwordLabel = QLabel("Password:")
    passwordLabel.setStyleSheet('''
        margin: 0px;
        font-size: 15px;
    ''')
    loginFormLayout.addRow(passwordLabel, passwordInput)
    loginForm.setLayout(loginFormLayout)
    layout.addWidget(loginForm)

    loginButton = QPushButton("Log in")
    loginButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    loginButton.setFixedWidth(75)
    loginButton.setStyleSheet('''
        background-color: green;
        font-size: 15px;
        border: none;
        padding: 3px;
    ''')
    loginButton.clicked.connect(login)
    layout.addWidget(loginButton, alignment=QtCore.Qt.AlignCenter)

    registerButton = QPushButton("Create account")
    registerButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    registerButton.setFixedWidth(125)
    registerButton.setStyleSheet('''
        background-color: green;
        font-size: 15px;
        border: none;
        padding: 3px;
    ''')
    registerButton.clicked.connect(register)
    layout.addWidget(registerButton, alignment=QtCore.Qt.AlignCenter)

    statusMessage = QLabel("")
    layout.addWidget(statusMessage)
    statusMessage.setAlignment(QtCore.Qt.AlignCenter)
    statusMessage.setStyleSheet('''
        color: 'red';
        font-size: 20px;
        margin-top: 25px;
    ''')

    loginWindow.setLayout(layout)
    mainWindow.setCentralWidget(loginWindow)

def register_frame():
    def register():
        userLogin = loginInput.text()
        userPassword = passwordInput.text()
        userNickname = nicknameInput.text()
        if len(userLogin) < 3:
            statusMessage.setText("Login needs to be at least 3 characters long.")
            return
        elif len(userPassword) < 3:
            statusMessage.setText("Password needs to be at least 3 characters long.")
            return
        elif len(userNickname) < 3:
            statusMessage.setText("Nickname needs to be at least 3 characters long.")
            return
        try:
            register_user(userLogin, userNickname, userPassword)
            login_frame()
        except pymongo.errors.DuplicateKeyError:
            statusMessage.setText("User with chosen username already exists.")

    def goBack():
        login_frame()

    registerWindow = QWidget()
    grid = QGridLayout()
    layout = QVBoxLayout()
    layout.setAlignment(QtCore.Qt.AlignCenter)

    backButton = QPushButton("Return")
    backButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    backButton.setFixedWidth(75)
    backButton.setStyleSheet('''
                background-color: lightgray;
                font-size: 15px;
                border: none;
                padding: 3px;
                margin-top: 10px 0px 0px 10px;
            ''')
    backButton.clicked.connect(goBack)
    grid.addWidget(backButton, 0, 0, alignment=QtCore.Qt.AlignLeft)

    titleLabel = QLabel("Create a new account")
    titleLabel.setStyleSheet('''
            font-size: 35px;
            font-weight: bold;
            margin-bottom: 25px;
            ''')
    titleLabel.setAlignment(QtCore.Qt.AlignCenter)
    layout.addWidget(titleLabel)

    registerForm = QGroupBox()
    registerForm.setMaximumWidth(600)
    registerForm.setStyleSheet('''
            border: none;
            margin: 0px 125px;
        ''')
    registerForm.setAlignment(QtCore.Qt.AlignCenter)
    registerFormLayout = QFormLayout()
    registerFormLayout.setAlignment(QtCore.Qt.AlignHCenter)
    registerFormLayout.setLabelAlignment(QtCore.Qt.AlignHCenter)

    loginInput = QLineEdit()
    loginInput.setFixedWidth(200)
    loginInput.setStyleSheet('''
            border: 1px solid black;
            margin: 0px;
            height: 25px;
            font-size: 15px;
        ''')
    loginRegex = QRegExp('^[0-9a-zA-ZąćęłńóśźżĄĘĆĘŁŃÓŚŹŻ]{30}$')
    loginValidator = QRegExpValidator(loginRegex, loginInput)
    loginInput.setValidator(loginValidator)
    loginLabel = QLabel("Login:")
    loginLabel.setStyleSheet('''
            margin: 0px;
            font-size: 15px;
        ''')
    registerFormLayout.addRow(loginLabel, loginInput)

    passwordInput = QLineEdit()
    passwordInput.setFixedWidth(200)
    passwordInput.setStyleSheet('''
           border: 1px solid black;
           margin: 0px;
           height: 25px;
           font-size: 15px;
       ''')
    passwordRegex = QRegExp('^[0-9a-zA-ZąćęłńóśźżĄĘĆĘŁŃÓŚŹŻ!@#$%&_-?]{30}$')
    passwordValidator = QRegExpValidator(passwordRegex, passwordInput)
    passwordInput.setValidator(passwordValidator)
    passwordInput.setEchoMode(QLineEdit.Password)
    passwordLabel = QLabel("Password:")
    passwordLabel.setStyleSheet('''
            margin: 0px;
            font-size: 15px;
        ''')
    registerFormLayout.addRow(passwordLabel, passwordInput)

    nicknameInput = QLineEdit()
    nicknameInput.setFixedWidth(200)
    nicknameInput.setStyleSheet('''
               border: 1px solid black;
               margin: 0px;
               height: 25px;
               font-size: 15px;
           ''')
    nicknameRegex = QRegExp('^[0-9a-zA-ZąćęłńóśźżĄĘĆĘŁŃÓŚŹŻ]{30}$')
    nicknameValidator = QRegExpValidator(nicknameRegex, nicknameInput)
    nicknameInput.setValidator(nicknameValidator)
    nicknameLabel = QLabel("Nickname:")
    nicknameLabel.setStyleSheet('''
                margin: 0px;
                font-size: 15px;
            ''')
    registerFormLayout.addRow(nicknameLabel, nicknameInput)

    registerForm.setLayout(registerFormLayout)
    layout.addWidget(registerForm)

    registerButton = QPushButton("Create account")
    registerButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    registerButton.setFixedWidth(125)
    registerButton.setStyleSheet('''
            background-color: green;
            font-size: 15px;
            border: none;
            padding: 3px;
            margin-top: 10px;
        ''')
    registerButton.clicked.connect(register)
    layout.addWidget(registerButton, alignment=QtCore.Qt.AlignCenter)

    statusMessage = QLabel("")
    layout.addWidget(statusMessage)
    statusMessage.setAlignment(QtCore.Qt.AlignCenter)
    statusMessage.setStyleSheet('''
            color: 'red';
            font-size: 20px;
            margin-top: 25px;
        ''')
    grid.addLayout(layout, 1, 0, alignment=QtCore.Qt.AlignCenter)
    registerWindow.setLayout(grid)
    mainWindow.setCentralWidget(registerWindow)


def test_frame():
    def logout():
        global user
        user = None
        login_frame()

    testWindow = QWidget()
    grid = QGridLayout()
    backButton = QPushButton("Log out")
    backButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    backButton.setFixedWidth(75)
    backButton.setStyleSheet('''
                    background-color: lightgray;
                    font-size: 15px;
                    border: none;
                    padding: 3px;
                    margin-top: 10px 0px 0px 10px;
                ''')
    backButton.clicked.connect(logout)
    grid.addWidget(backButton, 0, 0, alignment=QtCore.Qt.AlignCenter)
    testWindow.setLayout(grid)
    mainWindow.setCentralWidget(testWindow)

if __name__ == '__main__':
    main()


