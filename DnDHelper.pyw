import sys
from threading import Thread

from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, \
    QLineEdit, QGroupBox, QFormLayout, QMainWindow, QHBoxLayout, QScrollArea, QTextEdit, \
    QCheckBox, QComboBox, QDialog
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor, QRegExpValidator

import Database_Module
from Dice_Module import *
from Item_Module import Item
from Map_Module import BattleMap
from Monster_Module import Monster
from Spell_Module import Spell
from UserRoleEnum import UserRole
from Character_Module import Character
from Campaign_Module import Campaign
from User_Module import *

app = QApplication(sys.argv)
mainWindow = QMainWindow()
itemWindow = None
spellWindow = None
battlemapWindow = QWidget()
monsterWindow = None
sheetWindow = None
creationWindow = None
diceWindow = QWidget()
user: User = None
userRole: UserRole = None
campaign: Campaign = None
character: Character = None



def main():
    mainWindow.setWindowTitle("DND Helper")
    mainWindow.setFixedWidth(1400)
    mainWindow.setFixedHeight(700)
    mainWindow.setStyleSheet("background: #00b4ff;")

    login_frame()

    mainWindow.show()
    sys.exit(app.exec())

def login_frame():
    def login():
        userLogin = loginInput.text()
        userPassword = passwordInput.text()
        try:
            if authenticate_user(userLogin, userPassword):
                global user
                user = User.user_from_db_entry(DatabaseHandler.get_user(userLogin))
                role_frame()
            else:
                statusMessage.setText("Password is incorrect.")
        except TypeError as err:
            statusMessage.setText(err.__str__())

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
        background-color: white;
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
       background-color: white;
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
            background-color: white;
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
           background-color: white;
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
               background-color: white;
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


def role_frame():
    def logout():
        global user
        user = None
        global userRole
        userRole = None
        login_frame()

    def choosePlayer():
        global userRole
        userRole = UserRole.PLAYER
        campaign_frame()

    def chooseDM():
        global userRole
        userRole = UserRole.DUNGEON_MASTER
        campaign_frame()

    testWindow = QWidget()
    grid = QGridLayout()

    logoutButton = QPushButton("Log out")
    logoutButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    logoutButton.setFixedWidth(75)
    logoutButton.setStyleSheet('''
                background-color: lightgray;
                font-size: 15px;
                padding: 3px;
                margin: 10px 0 0 10px;
            ''')
    logoutButton.clicked.connect(logout)
    grid.addWidget(logoutButton, 0, 0, alignment=QtCore.Qt.AlignLeft)

    vbox = QVBoxLayout()
    vbox.setAlignment(QtCore.Qt.AlignCenter)
    titleLabel = QLabel("Choose your role")
    titleLabel.setStyleSheet('''
        font-size: 35px;
        font-weight: bold;
        margin-bottom: 25px;
        ''')
    titleLabel.setAlignment(QtCore.Qt.AlignCenter)
    vbox.addWidget(titleLabel, alignment=QtCore.Qt.AlignCenter)

    hbox = QHBoxLayout()
    playerButton = QPushButton("Continue as a player")
    playerButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    playerButton.setFixedWidth(350)
    playerButton.setFixedHeight(75)
    playerButton.setStyleSheet('''
            background-color: green;
            font-size: 20px;
            margin-right: 10px;
        ''')
    playerButton.clicked.connect(choosePlayer)

    dmButton = QPushButton("Continue as a Dungeon Master")
    dmButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    dmButton.setFixedWidth(350)
    dmButton.setFixedHeight(75)
    dmButton.setStyleSheet('''
            background-color: green;
            font-size: 20px;
            margin-left: 10px;
        ''')
    dmButton.clicked.connect(chooseDM)

    hbox.addWidget(playerButton)
    hbox.addWidget(dmButton)
    vbox.addLayout(hbox)
    grid.addLayout(vbox, 1, 0, alignment=QtCore.Qt.AlignCenter)

    testWindow.setLayout(grid)
    mainWindow.setCentralWidget(testWindow)

def campaign_frame():
    def logout():
        global user
        user = None
        global userRole
        userRole = None
        login_frame()

    def goBack():
        global userRole
        userRole = None
        role_frame()

    def chooseCampaign(campaignID):
        global campaign
        campaign = Campaign.campaign_from_db_entry(DatabaseHandler.get_campaign(campaignID))
        character_frame()

    def addCampaignDialog():
        def addCampaign():
            new_battlemap = BattleMap.battlemap_new(int(yInput.text()), int(xInput.text()))
            DatabaseHandler.insert_battlemap(new_battlemap)
            new_campaign = Campaign.campaign_new(addName.text(), new_battlemap.get_id())
            DatabaseHandler.insert_campaign(new_campaign)
            addDialog.close()
        addDialog = QDialog()
        addDialog.setWindowTitle("Add new campaign")
        addDialog.setStyleSheet('''
            background-color: #00b4ff;
        ''')
        addDialog.setFixedHeight(150)
        addDialog.setFixedWidth(350)
        gridDialog = QGridLayout()
        addLabel = QLabel("Campaign name: ")
        gridDialog.addWidget(addLabel, 0, 0, 1, 1)
        addName = QLineEdit()
        addName.setFixedWidth(150)
        addName.setStyleSheet('''
            background-color: white;
        ''')
        gridDialog.addWidget(addName, 0, 1, 1, 2)

        xyBox = QHBoxLayout()
        xyLabel = QLabel("Map X: ")
        xyBox.addWidget(xyLabel)
        xInput = QLineEdit()
        xInput.setFixedWidth(60)
        xInput.setStyleSheet('''
                    background-color: white;
                ''')
        xyBox.addWidget(xInput)
        yLabel = QLabel(" Y: ")
        xyBox.addWidget(yLabel)
        yInput = QLineEdit()
        yInput.setFixedWidth(60)
        yInput.setStyleSheet('''
                            background-color: white;
                        ''')
        xyBox.addWidget(yInput)
        gridDialog.addLayout(xyBox, 1, 0, 1, 2)

        addButton = QPushButton("Add")
        addButton.setFixedWidth(75)
        addButton.setFixedHeight(35)
        addButton.setStyleSheet('''
            background-color: green;
            font-size: 15px;
        ''')
        addButton.clicked.connect(addCampaign)
        gridDialog.addWidget(addButton, 1, 2)
        addDialog.setLayout(gridDialog)
        addDialog.exec_()

    campaignWindow = QWidget()
    grid = QGridLayout()

    hbox = QHBoxLayout()
    logoutButton = QPushButton("Log out")
    logoutButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    logoutButton.setFixedWidth(75)
    logoutButton.setStyleSheet('''
            background-color: lightgray;
            font-size: 15px;
            padding: 3px;
            margin: 10px 0 0 10px;
        ''')
    logoutButton.clicked.connect(logout)
    hbox.addWidget(logoutButton, alignment=QtCore.Qt.AlignLeft)

    backButton = QPushButton("Return")
    backButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    backButton.setFixedWidth(75)
    backButton.setStyleSheet('''
                    background-color: lightgray;
                    font-size: 15px;
                    padding: 3px;
                    margin-top: 10px 0px 0px 10px;
                ''')
    backButton.clicked.connect(goBack)
    hbox.addWidget(backButton, alignment=QtCore.Qt.AlignLeft)

    grid.addLayout(hbox, 0, 0, alignment=QtCore.Qt.AlignLeft)

    campaign_vbox = QVBoxLayout()
    campaign_label = QLabel("Choose campaign")
    campaign_label.setStyleSheet('''
            font-size: 35px;
            font-weight: bold;
            margin-bottom: 25px;
        ''')
    campaign_vbox.addWidget(campaign_label, alignment=QtCore.Qt.AlignCenter)
    campaign_list = QGroupBox()
    campaigns = QVBoxLayout()
    if userRole is UserRole.DUNGEON_MASTER:
        addCampaignButton = QPushButton("Add new campaign")
        addCampaignButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        addCampaignButton.clicked.connect(addCampaignDialog)
        addCampaignButton.setFixedHeight(50)
        addCampaignButton.setStyleSheet('''
           background-color: lightgreen;
           font-size: 15px;
       ''')
        campaigns.addWidget(addCampaignButton, alignment=QtCore.Qt.AlignCenter)
    for db_campaign in DatabaseHandler.get_campaigns_collection():
        campaign_from_db = Campaign.campaign_from_db_entry(db_campaign)
        global user
        if (userRole is UserRole.PLAYER and user.login in campaign_from_db.players) or userRole is UserRole.DUNGEON_MASTER:
            campaign_list_entry = QPushButton(campaign_from_db.campaign_name)
            campaign_list_entry.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            campaign_list_entry.clicked.connect(lambda _, ID=campaign_from_db.get_id(): chooseCampaign(ID))
            campaign_list_entry.setFixedHeight(50)
            campaign_list_entry.setStyleSheet('''
                background-color: green;
                font-size: 15px;
            ''')
            campaigns.addWidget(campaign_list_entry, alignment=QtCore.Qt.AlignCenter)
    campaign_list.setLayout(campaigns)
    scrollable_campaign_list = QScrollArea()
    scrollable_campaign_list.setWidget(campaign_list)
    scrollable_campaign_list.setWidgetResizable(True)
    scrollable_campaign_list.setFixedHeight(500)
    scrollable_campaign_list.setFixedWidth(800)
    scrollable_campaign_list.setStyleSheet('''
        background-color: lightgray;
    ''')
    campaign_vbox.addWidget(scrollable_campaign_list, alignment=QtCore.Qt.AlignCenter)
    grid.addLayout(campaign_vbox, 1, 0, alignment=QtCore.Qt.AlignCenter)

    campaignWindow.setLayout(grid)
    mainWindow.setCentralWidget(campaignWindow)

def character_frame():
    def logout():
        global user
        user = None
        global userRole
        userRole = None
        login_frame()

    def goBack():
        global campaign
        campaign = None
        campaign_frame()


    def chooseCharacter(character_id):
        character_sheet_frame(character_id)

    def seeItems():
        item_frame()

    def seeSpells():
        spell_frame()

    def seeMap():
        map_frame()

    def seeDice():
        dice_frame()

    def seeMonsters():
        monster_frame()

    def createCharacter():
        character_creation_frame()

    def addPlayerDialog():
        def addPlayer():
            campaign.add_player(addChoice.currentText())
            DatabaseHandler.update_campaign(campaign)
            addDialog.close()
        addDialog = QDialog()
        addDialog.setWindowTitle("Add new player")
        addDialog.setStyleSheet('''
            background-color: #00b4ff;
        ''')
        addDialog.setFixedHeight(150)
        addDialog.setFixedWidth(300)
        gridDialog = QGridLayout()
        addChoice = QComboBox()
        addChoice.setFixedWidth(150)
        addChoice.setStyleSheet('''
            background-color: white;
        ''')
        players = DatabaseHandler.get_users_collection()
        for player in players:
            player_from_db = User.user_from_db_entry(player)
            if player_from_db.login not in campaign.players:
                addChoice.addItem(player_from_db.login)
        gridDialog.addWidget(addChoice, 0, 0, 1, 2)
        addButton = QPushButton("Add")
        addButton.setFixedWidth(75)
        addButton.setFixedHeight(35)
        addButton.setStyleSheet('''
            background-color: green;
            font-size: 15px;
        ''')
        addButton.clicked.connect(addPlayer)
        gridDialog.addWidget(addButton, 1, 1)
        addDialog.setLayout(gridDialog)
        addDialog.exec_()


    characterWindow = QWidget()
    grid = QGridLayout()

    hbox = QHBoxLayout()
    logoutButton = QPushButton("Log out")
    logoutButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    logoutButton.setFixedWidth(75)
    logoutButton.setStyleSheet('''
            background-color: lightgray;
            font-size: 15px;
            padding: 3px;
            margin: 10px 0 0 10px;
        ''')
    logoutButton.clicked.connect(logout)
    hbox.addWidget(logoutButton, alignment=QtCore.Qt.AlignLeft)

    backButton = QPushButton("Return")
    backButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    backButton.setFixedWidth(75)
    backButton.setStyleSheet('''
                    background-color: lightgray;
                    font-size: 15px;
                    padding: 3px;
                    margin-top: 10px 0px 0px 10px;
                ''')
    backButton.clicked.connect(goBack)
    hbox.addWidget(backButton, alignment=QtCore.Qt.AlignLeft)

    grid.addLayout(hbox, 0, 0, alignment=QtCore.Qt.AlignLeft)

    character_label = QLabel(campaign.campaign_name)
    character_label.setAlignment(QtCore.Qt.AlignCenter)
    character_label.setWordWrap(True)
    character_label.setFixedWidth(1200)
    character_label.setStyleSheet('''
            font-size: 35px;
            font-weight: bold;
            margin-bottom: 25px;
        ''')
    grid.addWidget(character_label, 1, 0, alignment=QtCore.Qt.AlignCenter)
    hbox = QHBoxLayout()
    character_list = QGroupBox()
    characters = QVBoxLayout()
    characters.setAlignment(QtCore.Qt.AlignCenter)
    if userRole is UserRole.PLAYER:
        createCharacterButton = QPushButton("Create a new character")
        createCharacterButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        createCharacterButton.clicked.connect(createCharacter)
        createCharacterButton.setFixedHeight(50)
        createCharacterButton.setStyleSheet('''
                       background-color: lightgreen;
                       font-size: 15px;
                   ''')
        characters.addWidget(createCharacterButton, alignment=QtCore.Qt.AlignCenter)
    elif userRole is UserRole.DUNGEON_MASTER:
        addPlayerButton = QPushButton("Add player to this campaign")
        addPlayerButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        addPlayerButton.clicked.connect(addPlayerDialog)
        addPlayerButton.setFixedHeight(50)
        addPlayerButton.setStyleSheet('''
                               background-color: lightgreen;
                               font-size: 15px;
                           ''')
        characters.addWidget(addPlayerButton, alignment=QtCore.Qt.AlignCenter)

    for db_character in DatabaseHandler.get_characters_collection():
        character = Character.character_from_db_entry(db_character)
        if character.user in campaign.players and (user.login == character.user or userRole is UserRole.DUNGEON_MASTER):
            character_list_entry = QPushButton(character.name + ", " + character.c_class + " lvl." + str(character.level))
            character_list_entry.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            character_list_entry.clicked.connect(lambda _, ID=character.get_id(): chooseCharacter(ID))
            character_list_entry.setFixedHeight(50)
            character_list_entry.setStyleSheet('''
                background-color: green;
                font-size: 15px;
            ''')
            characters.addWidget(character_list_entry, alignment=QtCore.Qt.AlignCenter)
    character_list.setLayout(characters)
    scrollable_character_list = QScrollArea()
    scrollable_character_list.setWidget(character_list)
    scrollable_character_list.setWidgetResizable(True)
    scrollable_character_list.setFixedHeight(500)
    scrollable_character_list.setFixedWidth(800)
    scrollable_character_list.setStyleSheet('''
        background-color: lightgray;
    ''')
    hbox.addWidget(scrollable_character_list)

    button_grid = QGridLayout()
    button_grid.setAlignment(QtCore.Qt.AlignCenter)
    button_grid.setSpacing(30)
    itemButton = QPushButton("Items")
    itemButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    itemButton.setFixedWidth(150)
    itemButton.setFixedHeight(50)
    itemButton.setStyleSheet('''
                        background-color: lightgreen;
                        font-size: 30px;
                        padding: 3px;
                    ''')
    itemButton.clicked.connect(seeItems)
    button_grid.addWidget(itemButton, 0, 0)

    spellButton = QPushButton("Spells")
    spellButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    spellButton.setFixedWidth(150)
    spellButton.setFixedHeight(50)
    spellButton.setStyleSheet('''
                                background-color: lightgreen;
                                font-size: 30px;
                                padding: 3px;
                            ''')
    spellButton.clicked.connect(seeSpells)
    button_grid.addWidget(spellButton, 0, 1)

    mapButton = QPushButton("Map")
    mapButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    mapButton.setFixedWidth(150)
    mapButton.setFixedHeight(50)
    mapButton.setStyleSheet('''
                                background-color: lightgreen;
                                font-size: 30px;
                                padding: 3px;
                            ''')
    mapButton.clicked.connect(seeMap)
    button_grid.addWidget(mapButton, 1, 1)

    diceButton = QPushButton("Dice")
    diceButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    diceButton.setFixedWidth(150)
    diceButton.setFixedHeight(50)
    diceButton.setStyleSheet('''
                                    background-color: lightgreen;
                                    font-size: 30px;
                                    padding: 3px;
                                ''')
    diceButton.clicked.connect(seeDice)
    button_grid.addWidget(diceButton, 1, 0)

    if userRole is UserRole.DUNGEON_MASTER:
        monsterButton = QPushButton("Monsters")
        monsterButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        monsterButton.setFixedWidth(150)
        monsterButton.setFixedHeight(50)
        monsterButton.setStyleSheet('''
                                        background-color: lightgreen;
                                        font-size: 30px;
                                        padding: 3px;
                                    ''')
        monsterButton.clicked.connect(seeMonsters)
        button_grid.addWidget(monsterButton, 2, 0)
    hbox.addLayout(button_grid)
    grid.addLayout(hbox, 2, 0)

    characterWindow.setLayout(grid)
    mainWindow.setCentralWidget(characterWindow)

def item_frame():
    def addItemDialog():
        def addItem():
            new_item = Item.item_new(nameInput.text(), descInput.toPlainText())
            DatabaseHandler.insert_item(new_item)
            addDialog.close()
        addDialog = QDialog()
        addDialog.setWindowTitle("Add new item")
        addDialog.setStyleSheet('''
                    background-color: #00b4ff;
                ''')
        addDialog.setFixedHeight(300)
        addDialog.setFixedWidth(500)

        addBox = QVBoxLayout()

        nameBox = QHBoxLayout()
        nameInput = QLineEdit()
        nameInput.setFixedWidth(380)
        nameInput.setStyleSheet('''
                    border: 1px solid black;
                    height: 25px;
                    background-color: white;
                    font-size: 15px;
                ''')
        nameLabel = QLabel("Name:")
        nameLabel.setStyleSheet('''
                    font-size: 15px;
                ''')
        nameBox.addWidget(nameLabel)
        nameBox.addWidget(nameInput)
        addBox.addLayout(nameBox)

        descBox = QHBoxLayout()
        descInput = QTextEdit()
        descInput.setFixedWidth(380)
        descInput.setFixedHeight(150)
        descInput.setStyleSheet('''
                   border: 1px solid black;
                   height: 25px;
                   background-color: white;
                   font-size: 15px;
               ''')
        descLabel = QLabel("Description:")
        descLabel.setStyleSheet('''
                    font-size: 15px;
                ''')
        descBox.addWidget(descLabel)
        descBox.addWidget(descInput)
        addBox.addLayout(descBox)

        addButton = QPushButton("Add")
        addButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        addButton.setFixedWidth(75)
        addButton.setStyleSheet('''
                    background-color: green;
                    font-size: 15px;
                    padding: 3px;
                ''')
        addButton.clicked.connect(addItem)
        addBox.addWidget(addButton, alignment=QtCore.Qt.AlignCenter)
        addDialog.setLayout(addBox)
        addDialog.exec_()

    global itemWindow
    itemWindow = QWidget()
    itemWindow.setWindowTitle("DND Helper")
    itemWindow.setFixedWidth(1000)
    itemWindow.setFixedHeight(600)
    itemWindow.setStyleSheet("background: #00b4ff;")

    item_vbox = QVBoxLayout()
    item_vbox.setAlignment(QtCore.Qt.AlignCenter)

    item_list = QGroupBox()
    items = QVBoxLayout()
    if userRole is UserRole.DUNGEON_MASTER:
        addItemButton = QPushButton("Add new item")
        addItemButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        addItemButton.clicked.connect(addItemDialog)
        addItemButton.setFixedHeight(50)
        addItemButton.setStyleSheet('''
                           background-color: lightgreen;
                           font-size: 15px;
                       ''')
        items.addWidget(addItemButton, alignment=QtCore.Qt.AlignCenter)
    for db_item in DatabaseHandler.get_items_collection():
        item_from_db = Item.item_from_db_entry(db_item)
        item_list_entry = QLabel("Name: " + item_from_db.name + "\nDescription: " + item_from_db.description)
        item_list_entry.setFixedWidth(700)
        item_list_entry.setWordWrap(True)
        item_list_entry.setStyleSheet('''
                        background-color: green;
                        font-size: 15px;
                        padding: 5px;
                    ''')
        items.addWidget(item_list_entry, alignment=QtCore.Qt.AlignCenter)
    item_list.setLayout(items)
    scrollable_item_list = QScrollArea()
    scrollable_item_list.setWidget(item_list)
    scrollable_item_list.setWidgetResizable(True)
    scrollable_item_list.setFixedHeight(500)
    scrollable_item_list.setFixedWidth(800)
    scrollable_item_list.setStyleSheet('''
                            background-color: lightgray;
                        ''')
    item_vbox.addWidget(scrollable_item_list, alignment=QtCore.Qt.AlignCenter)

    itemWindow.setLayout(item_vbox)

    itemWindow.show()

def spell_frame():
    def addSpellDialog():
        def addSpell():
            new_spell = Spell.spell_new(nameInput.text(), descInput.toPlainText())
            DatabaseHandler.insert_spell(new_spell)
            addDialog.close()

        addDialog = QDialog()
        addDialog.setWindowTitle("Add new item")
        addDialog.setStyleSheet('''
                    background-color: #00b4ff;
                ''')
        addDialog.setFixedHeight(300)
        addDialog.setFixedWidth(500)

        addBox = QVBoxLayout()

        nameBox = QHBoxLayout()
        nameInput = QLineEdit()
        nameInput.setFixedWidth(380)
        nameInput.setStyleSheet('''
                    border: 1px solid black;
                    height: 25px;
                    background-color: white;
                    font-size: 15px;
                ''')
        nameLabel = QLabel("Name:")
        nameLabel.setStyleSheet('''
                    font-size: 15px;
                ''')
        nameBox.addWidget(nameLabel)
        nameBox.addWidget(nameInput)
        addBox.addLayout(nameBox)

        descBox = QHBoxLayout()
        descInput = QTextEdit()
        descInput.setFixedWidth(380)
        descInput.setFixedHeight(150)
        descInput.setStyleSheet('''
                   border: 1px solid black;
                   height: 25px;
                   background-color: white;
                   font-size: 15px;
               ''')
        descLabel = QLabel("Description:")
        descLabel.setStyleSheet('''
                    font-size: 15px;
                ''')
        descBox.addWidget(descLabel)
        descBox.addWidget(descInput)
        addBox.addLayout(descBox)

        addButton = QPushButton("Add")
        addButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        addButton.setFixedWidth(75)
        addButton.setStyleSheet('''
                    background-color: green;
                    font-size: 15px;
                    padding: 3px;
                ''')
        addButton.clicked.connect(addSpell)
        addBox.addWidget(addButton, alignment=QtCore.Qt.AlignCenter)
        addDialog.setLayout(addBox)
        addDialog.exec_()


    global spellWindow
    spellWindow = QWidget()
    spellWindow.setWindowTitle("DND Helper")
    spellWindow.setFixedWidth(1000)
    spellWindow.setFixedHeight(600)
    spellWindow.setStyleSheet("background: #00b4ff;")

    spell_vbox = QVBoxLayout()
    spell_vbox.setAlignment(QtCore.Qt.AlignCenter)

    spell_list = QGroupBox()
    spells = QVBoxLayout()
    if userRole is UserRole.DUNGEON_MASTER:
        addSpellButton = QPushButton("Add new spell")
        addSpellButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        addSpellButton.clicked.connect(addSpellDialog)
        addSpellButton.setFixedHeight(50)
        addSpellButton.setStyleSheet('''
           background-color: lightgreen;
           font-size: 15px;
       ''')
        spells.addWidget(addSpellButton, alignment=QtCore.Qt.AlignCenter)
    for db_spell in DatabaseHandler.get_spells_collection():
        spell_from_db = Spell.spell_from_db_entry(db_spell)
        spell_list_entry = QLabel("Name: " + spell_from_db.name + "\nDescription: " + spell_from_db.description)
        spell_list_entry.setFixedWidth(700)
        spell_list_entry.setWordWrap(True)
        spell_list_entry.setStyleSheet('''
                        background-color: green;
                        font-size: 15px;
                        padding: 5px;
                    ''')
        spells.addWidget(spell_list_entry, alignment=QtCore.Qt.AlignCenter)
    spell_list.setLayout(spells)
    scrollable_spell_list = QScrollArea()
    scrollable_spell_list.setWidget(spell_list)
    scrollable_spell_list.setWidgetResizable(True)
    scrollable_spell_list.setFixedHeight(500)
    scrollable_spell_list.setFixedWidth(800)
    scrollable_spell_list.setStyleSheet('''
            background-color: lightgray;
        ''')
    spell_vbox.addWidget(scrollable_spell_list, alignment=QtCore.Qt.AlignCenter)

    spellWindow.setLayout(spell_vbox)
    spellWindow.show()

def map_frame():
    def watch_changes_to_battlemap():
        with Database_Module.DatabaseHandler.battlemaps_collection.watch(full_document="updateLookup") as stream:
            while stream.alive:
                if battlemapWindow.isHidden():
                    return
                change = stream.try_next()
                if change is not None and change["documentKey"]["_id"] == battlemap.get_id():
                    if change["operationType"] == "update":
                        updatedBattlemap = BattleMap.battlemap_from_db_entry(change["fullDocument"])
                        battlemapTokenPositions = list(battlemap.get_active_tokens().keys())
                        for key in battlemapTokenPositions:
                            tokens[key[1]][key[0]].setStyleSheet("border-radius: 40px;"
                                                                 "color: transparent;"
                                                                 "background-color: transparent;")
                            tokens[key[1]][key[0]].setText("")
                            battlemap.remove_token(key[0], key[1])
                        for key in updatedBattlemap.get_active_tokens().keys():
                            tokens[key[1]][key[0]].setStyleSheet("border-radius: 40px;"
                                                                 "color: white;"
                                                                 "background-color: " + updatedBattlemap.get_token_color(key[0], key[1]) + ";")
                            tokens[key[1]][key[0]].setText(updatedBattlemap.get_token_label(key[0], key[1]))
                            battlemap.add_token(key[0], key[1], updatedBattlemap.get_token_color(key[0], key[1]), updatedBattlemap.get_token_label(key[0], key[1]), updatedBattlemap.get_token_owner(key[0], key[1]))

    global battlemapWindow
    battlemapWindow = QWidget()

    changeStreamThread = Thread()
    changeStreamThread.run = watch_changes_to_battlemap

    db_entry = DatabaseHandler.get_battlemap(ObjectId(campaign.battlemap_id))
    battlemap = BattleMap.battlemap_from_db_entry(db_entry)

    left_button_pressed = False
    right_button_pressed = False

    def press_event(event, label, x, y):
        nonlocal left_button_pressed, right_button_pressed
        if event.button() == QtCore.Qt.LeftButton:
            left_button_pressed = True
        elif event.button() == QtCore.Qt.RightButton:
            right_button_pressed = True

        if (x, y) in battlemap.get_active_tokens().keys() and (userRole is UserRole.DUNGEON_MASTER or battlemap.get_token_owner(x, y) == user.login):
            label.setStyleSheet("border-radius: 0px;"
                                "color: transparent;"
                                "background-color: transparent;")
            label.setText("")
            if left_button_pressed and not right_button_pressed:
                nonlocal movableToken
                movableToken.hide()
                movableToken = QLabel("", gridWrapper)
                movableToken.setFixedWidth(80)
                movableToken.setFixedHeight(80)
                movableToken.setStyleSheet("border-radius: 40px;"
                                  "color: white;"
                                  "background-color: " + battlemap.get_token_color(x, y) + ";")
                movableToken.setAlignment(QtCore.Qt.AlignCenter)
                movableToken.setText(battlemap.get_token_label(x, y))
                movableToken.move(min(max(12, x * 80 + event.x() - 40), 80*(battlemap.columns-1)+12),
                         min(max(12, y * 80 + event.y() - 40), 80*(battlemap.rows-1)+12))
                movableToken.show()
            elif right_button_pressed and not left_button_pressed:
                battlemap.remove_token(x, y)
                DatabaseHandler.update_battlemap(battlemap)

    def release_event(event, label, x, y):
        nonlocal left_button_pressed, right_button_pressed

        if left_button_pressed and not right_button_pressed:
            if (x, y) in battlemap.get_active_tokens().keys() and (userRole is UserRole.DUNGEON_MASTER or battlemap.get_token_owner(x, y) == user.login):
                x_position = x + event.x() // 80
                x_position = min(max(0, x_position), battlemap.columns-1)
                y_position = y + event.y() // 80
                y_position = min(max(0, y_position), battlemap.rows-1)
                tokens[y_position][x_position].setStyleSheet("border-radius: 40px;"
                                                             "background-color: " + battlemap.get_token_color(x, y) + ";"
                                                                                                              "color: white;")
                tokens[y_position][x_position].setText(battlemap.get_token_label(x, y))
                nonlocal movableToken
                movableToken.hide()
                battlemap.move_token(x, y, x_position, y_position)
                DatabaseHandler.update_battlemap(battlemap)
        elif right_button_pressed and not left_button_pressed:
            pass

        if event.button() == QtCore.Qt.LeftButton:
            left_button_pressed = False
        elif event.button() == QtCore.Qt.RightButton:
            right_button_pressed = False

    def move_event(event, label, x, y):
        if (x, y) in battlemap.get_active_tokens().keys() and (userRole is UserRole.DUNGEON_MASTER or battlemap.get_token_owner(x, y) == user.login):
            nonlocal movableToken
            movableToken.hide()
            movableToken = QLabel("", gridWrapper)
            movableToken.setFixedWidth(80)
            movableToken.setFixedHeight(80)
            movableToken.setStyleSheet("border-radius: 40px;"
                                       "color: white;"
                                       "background-color: " + battlemap.get_token_color(x, y) + ";")
            movableToken.setText(battlemap.get_token_label(x, y))
            movableToken.setAlignment(QtCore.Qt.AlignCenter)

            movableToken.move(min(max(12, x * 80 + event.x() - 40), 80*(battlemap.columns-1)+12),
                              min(max(12, y * 80 + event.y() - 40), 80*(battlemap.rows-1)+12))
            movableToken.show()

    battlemapWindow.setWindowTitle("DND Helper - BattleMap")
    battlemapWindow.setMinimumWidth(1400)
    battlemapWindow.setMinimumHeight(700)
    battlemapWindow.setStyleSheet("background: #00b4ff;")

    layout = QHBoxLayout()
    scrollArea = QScrollArea()
    gridWrapper = QWidget()
    grid = QGridLayout()
    grid.setSpacing(0)

    tokens = []

    for i in range(0, battlemap.rows):
        row = []
        for j in range(0, battlemap.columns):
            fieldLabel = QLabel("X: " + str(j) + " , Y: " + str(i), battlemapWindow)
            fieldLabel.setFixedWidth(80)
            fieldLabel.setFixedHeight(80)
            fieldLabel.setStyleSheet("border: 1px solid black; "
                                     "border-radius: 0px;"
                                     "color: black;"
                                     "background-color: white;")
            fieldLabel.setAlignment(QtCore.Qt.AlignCenter)
            grid.addWidget(fieldLabel, i, j)

            tokenLabel = QLabel()
            tokenLabel.setFixedWidth(80)
            tokenLabel.setFixedHeight(80)
            tokenLabel.setStyleSheet("border-radius: 40px;"
                                     "color: transparent;"
                                     "background-color: transparent;")
            tokenLabel.setAlignment(QtCore.Qt.AlignCenter)
            tokenLabel.mousePressEvent = lambda event, label=tokenLabel, x=j, y=i: press_event(event, label, x, y)
            tokenLabel.mouseReleaseEvent = lambda event, label=tokenLabel, x=j, y=i: release_event(event, label, x, y)
            tokenLabel.mouseMoveEvent = lambda event, label=tokenLabel, x=j, y=i: move_event(event, label, x, y)
            row.append(tokenLabel)
            grid.addWidget(tokenLabel, i, j)
        tokens.append(row)

    gridWrapper.setLayout(grid)
    scrollArea.setWidget(gridWrapper)
    layout.addWidget(scrollArea)

    controlsWrapper = QWidget()
    controlsVBox = QVBoxLayout()

    titleHBox = QHBoxLayout()
    titleLabel = QLabel("Add a new token")
    titleLabel.setStyleSheet("font-size: 20px;")
    titleLabel.setFixedHeight(30)
    titleHBox.addWidget(titleLabel)
    controlsVBox.addLayout(titleHBox)

    colorHBox = QHBoxLayout()
    colorLabel = QLabel("Color: ")
    colorLabel.setStyleSheet("font-size: 15px; padding: 3px; background-color: Aqua;")
    colorChoiceBox = QComboBox()
    colorChoiceBox.addItems(
        ["Aqua", "Aquamarine", "Black", "Blue", "BlueViolet", "Brown", "Chartreuse", "Chocolate", "Coral",
         "CornflowerBlue", "Crimson", "DarkBlue", "DarkGoldenRod", "DarkGray", "DarkGreen", "DarkOrange",
         "DarkRed", "DarkViolet", "DeepSkyBlue", "DimGray", "DodgerBlue", "FireBrick", "ForestGreen",
         "Fuchsia", "Gold", "GoldenRod", "Gray", "Green", "GreenYellow", "Indigo", "LawnGreen", "LightGray",
         "Lime", "LimeGreen", "Maroon", "MediumBlue", "MediumVioletRed", "MidnightBlue", "Navy", "Olive",
         "OliveDrab", "Orange", "OrangeRed", "Purple", "Red", "RoyalBlue", "SaddleBrown", "SeaGreen",
         "Silver", "SkyBlue", "Yellow", "YellowGreen"])
    colorChoiceBox.setStyleSheet("background-color: white; font-size: 15px;")
    colorChoiceBox.currentIndexChanged.connect(lambda index: colorLabel.setStyleSheet(
        "font-size: 15px; padding: 3px; background-color: " + colorChoiceBox.currentText()))
    colorHBox.addWidget(colorLabel)
    colorHBox.addWidget(colorChoiceBox)
    controlsVBox.addLayout(colorHBox)

    labelHBox = QHBoxLayout()
    labelLabel = QLabel("Label: ")
    labelLabel.setStyleSheet("font-size: 15px;")
    labelLabel.setFixedWidth(200)
    labelInput = QLineEdit("")
    labelInput.setStyleSheet("font-size: 15px; background-color: white;")
    labelInput.setFixedWidth(100)
    labelHBox.addWidget(labelLabel)
    labelHBox.addWidget(labelInput)
    controlsVBox.addLayout(labelHBox)

    xPositionHBox = QHBoxLayout()
    xPositionLabel = QLabel("X: ")
    xPositionLabel.setStyleSheet("font-size: 15px;")
    xPositionLabel.setFixedWidth(200)
    xPositionInput = QLineEdit("0")
    xPositionInput.setStyleSheet("font-size: 15px; background-color: white;")
    xPositionInput.setFixedWidth(100)
    xPositionHBox.addWidget(xPositionLabel)
    xPositionHBox.addWidget(xPositionInput)
    controlsVBox.addLayout(xPositionHBox)

    yPositionHBox = QHBoxLayout()
    yPositionLabel = QLabel("Y: ")
    yPositionLabel.setStyleSheet("font-size: 15px;")
    yPositionLabel.setFixedWidth(200)
    yPositionInput = QLineEdit("0")
    yPositionInput.setStyleSheet("font-size: 15px; background-color: white;")
    yPositionInput.setFixedWidth(100)
    yPositionHBox.addWidget(yPositionLabel)
    yPositionHBox.addWidget(yPositionInput)
    controlsVBox.addLayout(yPositionHBox)

    def create_token():
        x = int(xPositionInput.text())
        y = int(yPositionInput.text())
        if 0 <= x < battlemap.columns and 0 <= y < battlemap.rows:
            battlemap.add_token(x, y, colorChoiceBox.currentText(), labelInput.text(), user.login)
            DatabaseHandler.update_battlemap(battlemap)
            tokens[y][x].setStyleSheet("border-radius: 40px;"
                                       "color: white;"
                                       "background-color: " + battlemap.get_token_color(x, y) + ";")
            tokens[y][x].setText(battlemap.get_token_label(x, y))

    addHBox = QHBoxLayout()
    addButton = QPushButton("Create token")
    addButton.setStyleSheet("background-color: green; font-size: 15px;")
    addButton.clicked.connect(create_token)
    addHBox.addWidget(addButton)
    controlsVBox.addLayout(addHBox)

    controlsWrapper.setLayout(controlsVBox)
    controlsWrapper.setFixedWidth(300)
    layout.addWidget(controlsWrapper)

    battlemapWindow.setLayout(layout)

    movableToken = QLabel("", battlemapWindow)
    movableToken.hide()

    for key in battlemap.get_active_tokens().keys():
        tokens[key[1]][key[0]].setStyleSheet("border-radius: 40px;"
                                             "color: white;"
                                             "background-color: " + battlemap.get_active_tokens()[key][0] + ";")
        tokens[key[1]][key[0]].setText(battlemap.get_active_tokens()[key][1])

    battlemapWindow.show()
    changeStreamThread.start()

def dice_frame():
    def reset_results():
        labelD4Results.setText("")
        labelD6Results.setText("")
        labelD8Results.setText("")
        labelD10Results.setText("")
        labelD12Results.setText("")
        labelD20Results.setText("")
        labelD100Results.setText("")
        labelCustomResults.setText("")
        labelTotalRoll.setText("")
    def reset():
        reset_results()
        inputD4.setText("0")
        inputD6.setText("0")
        inputD8.setText("0")
        inputD10.setText("0")
        inputD12.setText("0")
        inputD20.setText("0")
        inputD100.setText("0")
        inputCustomAmount.setText("0")
    def roll():
        reset_results()
        totalRoll = 0
        if inputD4.text().isdigit() and int(inputD4.text()) > 0:
            totalD4, rollsD4 = roll_d4(int(inputD4.text()))
            totalRoll += totalD4
            labelD4Results.setText("Total: " + str(totalD4) + ", rolls: " + str(rollsD4))
        if inputD6.text().isdigit() and int(inputD6.text()) > 0:
            totalD6, rollsD6 = roll_d6(int(inputD6.text()))
            totalRoll += totalD6
            labelD6Results.setText("Total: " + str(totalD6) + ", rolls: " + str(rollsD6))
        if inputD8.text().isdigit() and int(inputD8.text()) > 0:
            totalD8, rollsD8 = roll_d8(int(inputD8.text()))
            totalRoll += totalD8
            labelD8Results.setText("Total: " + str(totalD8) + ", rolls: " + str(rollsD8))
        if inputD10.text().isdigit() and int(inputD10.text()) > 0:
            totalD10, rollsD10 = roll_d10(int(inputD10.text()))
            totalRoll += totalD10
            labelD10Results.setText("Total: " + str(totalD10) + ", rolls: " + str(rollsD10))
        if inputD12.text().isdigit() and int(inputD12.text()) > 0:
            totalD12, rollsD12 = roll_d12(int(inputD12.text()))
            totalRoll += totalD12
            labelD12Results.setText("Total: " + str(totalD12) + ", rolls: " + str(rollsD12))
        if inputD20.text().isdigit() and int(inputD20.text()) > 0:
            totalD20, rollsD20 = roll_d20(int(inputD20.text()))
            totalRoll += totalD20
            labelD20Results.setText("Total: " + str(totalD20) + ", rolls: " + str(rollsD20))
        if inputD100.text().isdigit() and int(inputD100.text()) > 0:
            totalD100, rollsD100 = roll_d100(int(inputD100.text()))
            totalRoll += totalD100
            labelD100Results.setText("Total: " + str(totalD100) + ", rolls: " + str(rollsD100))
        if inputCustomAmount.text().isdigit() and inputCustomDice.text().isdigit() and int(inputCustomAmount.text()) > 0:
            totalCustom, rollsCustom = roll_dice(int(inputCustomAmount.text()), int(inputCustomDice.text()))
            totalRoll += totalCustom
            labelCustomResults.setText("Total: " + str(totalCustom) + ", rolls: " + str(rollsCustom))
        if totalRoll > 0:
            labelTotalRoll.setText("Roll total: " + str(totalRoll))
    global diceWindow
    diceWindow.hide()
    diceWindow = QWidget()

    diceWindow.setWindowTitle("DND Helper")
    diceWindow.setFixedWidth(1000)
    diceWindow.setFixedHeight(500)
    diceWindow.setStyleSheet("background: #00b4ff;")

    diceGrid = QGridLayout()
    diceGrid.setAlignment(QtCore.Qt.AlignTop)
    vboxRolls = QVBoxLayout()
    vboxRolls.setContentsMargins(0, 0, 0, 0)
    wrapperWidgetRolls = QWidget()
    wrapperWidgetRolls.setFixedWidth(130)

    labelTitle = QLabel("Roll the dice!")
    labelTitle.setStyleSheet('''
        font-size: 40px;
        margin: 10px;
    ''')
    diceGrid.addWidget(labelTitle, 0, 0, 1, 2)

    hboxD4 = QHBoxLayout()
    labelD4 = QLabel("d4: ")
    inputD4 = QLineEdit("0")
    inputD4.setFixedWidth(40)
    hboxD4.addWidget(labelD4)
    hboxD4.addWidget(inputD4)
    vboxRolls.addLayout(hboxD4)

    hboxD6 = QHBoxLayout()
    labelD6 = QLabel("d6: ")
    inputD6 = QLineEdit("0")
    inputD6.setFixedWidth(40)
    hboxD6.addWidget(labelD6)
    hboxD6.addWidget(inputD6)
    vboxRolls.addLayout(hboxD6)

    hboxD8 = QHBoxLayout()
    labelD8 = QLabel("d8: ")
    inputD8 = QLineEdit("0")
    inputD8.setFixedWidth(40)
    hboxD8.addWidget(labelD8)
    hboxD8.addWidget(inputD8)
    vboxRolls.addLayout(hboxD8)

    hboxD10 = QHBoxLayout()
    labelD10 = QLabel("d10: ")
    inputD10 = QLineEdit("0")
    inputD10.setFixedWidth(40)
    hboxD10.addWidget(labelD10)
    hboxD10.addWidget(inputD10)
    vboxRolls.addLayout(hboxD10)

    hboxD12 = QHBoxLayout()
    labelD12 = QLabel("d12: ")
    inputD12 = QLineEdit("0")
    inputD12.setFixedWidth(40)
    hboxD12.addWidget(labelD12)
    hboxD12.addWidget(inputD12)
    vboxRolls.addLayout(hboxD12)

    hboxD20 = QHBoxLayout()
    labelD20 = QLabel("d20: ")
    inputD20 = QLineEdit("0")
    inputD20.setFixedWidth(40)
    hboxD20.addWidget(labelD20)
    hboxD20.addWidget(inputD20)
    vboxRolls.addLayout(hboxD20)

    hboxD100 = QHBoxLayout()
    labelD100 = QLabel("d100: ")
    inputD100 = QLineEdit("0")
    inputD100.setFixedWidth(40)
    hboxD100.addWidget(labelD100)
    hboxD100.addWidget(inputD100)
    vboxRolls.addLayout(hboxD100)

    hboxCustom = QHBoxLayout()
    labelCustom1 = QLabel("d")
    inputCustomDice = QLineEdit("1")
    inputCustomDice.setFixedWidth(40)
    labelCustom2 = QLabel(": ")
    inputCustomAmount = QLineEdit("0")
    inputCustomAmount.setFixedWidth(40)
    hboxCustom.addWidget(labelCustom1)
    hboxCustom.addWidget(inputCustomDice)
    hboxCustom.addWidget(labelCustom2)
    hboxCustom.addWidget(inputCustomAmount)
    vboxRolls.addLayout(hboxCustom)

    buttonBox = QHBoxLayout()
    rollButton = QPushButton("Roll")
    rollButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    rollButton.setFixedWidth(50)
    rollButton.setStyleSheet('''
                background-color: green;
                font-size: 15px;
                padding: 3px;
            ''')
    rollButton.clicked.connect(roll)
    buttonBox.addWidget(rollButton)

    resetButton = QPushButton("Reset")
    resetButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    resetButton.setFixedWidth(50)
    resetButton.setStyleSheet('''
                background-color: green;
                font-size: 15px;
                padding: 3px;
            ''')
    resetButton.clicked.connect(reset)
    buttonBox.addWidget(resetButton)
    vboxRolls.addLayout(buttonBox)

    wrapperWidgetRolls.setLayout(vboxRolls)
    diceGrid.addWidget(wrapperWidgetRolls, 1, 0, 9, 1)

    vboxResults = QVBoxLayout()
    vboxResults.setContentsMargins(0, 5, 0, 0)

    diceGrid.setVerticalSpacing(6)
    labelD4Results = QLabel()
    labelD4Results.setFixedHeight(25)
    diceGrid.addWidget(labelD4Results, 1, 1)
    labelD6Results = QLabel()
    labelD6Results.setFixedHeight(25)
    diceGrid.addWidget(labelD6Results, 2, 1)
    labelD8Results = QLabel()
    labelD8Results.setFixedHeight(25)
    diceGrid.addWidget(labelD8Results, 3, 1)
    labelD10Results = QLabel()
    labelD10Results.setFixedHeight(25)
    diceGrid.addWidget(labelD10Results, 4, 1)
    labelD12Results = QLabel()
    labelD12Results.setFixedHeight(25)
    diceGrid.addWidget(labelD12Results, 5, 1)
    labelD20Results = QLabel()
    labelD20Results.setFixedHeight(25)
    diceGrid.addWidget(labelD20Results, 6, 1)
    labelD100Results = QLabel()
    labelD100Results.setFixedHeight(25)
    diceGrid.addWidget(labelD100Results, 7, 1)
    labelCustomResults = QLabel()
    labelCustomResults.setFixedHeight(25)
    diceGrid.addWidget(labelCustomResults, 8, 1)
    labelTotalRoll = QLabel()
    labelTotalRoll.setFixedHeight(25)
    diceGrid.addWidget(labelTotalRoll, 9, 1)

    diceWindow.setLayout(diceGrid)
    diceWindow.show()

def monster_frame():
    def addMonsterDialog():
        def addMonster():
            new_monster = Monster.monster_new(nameInput.text(), familyInput.text(),
                              int(armorInput.text()), int(lifeInput.text()),
                              int(speedInput.text()), int(strInput.text()),
                              int(dexInput.text()), int(constInput.text()),
                              int(intInput.text()), int(wisInput.text()),
                              int(chaInput.text()), int(challengeInput.text()),
                              descInput.toPlainText()
                              )
            DatabaseHandler.insert_monster(new_monster)
            addDialog.close()

        addDialog = QDialog()
        addDialog.setWindowTitle("Add new item")
        addDialog.setStyleSheet('''
                    background-color: #00b4ff;
                ''')
        addDialog.setFixedHeight(450)
        addDialog.setFixedWidth(500)

        addBox = QVBoxLayout()

        nameBox = QHBoxLayout()
        nameInput = QLineEdit()
        nameInput.setFixedWidth(380)
        nameInput.setStyleSheet('''
                    border: 1px solid black;
                    height: 25px;
                    background-color: white;
                    font-size: 15px;
                ''')
        nameLabel = QLabel("Name:")
        nameLabel.setStyleSheet('''
                    font-size: 15px;
                ''')
        nameBox.addWidget(nameLabel)
        nameBox.addWidget(nameInput)
        addBox.addLayout(nameBox)

        familyBox = QHBoxLayout()
        familyInput = QLineEdit()
        familyInput.setFixedWidth(380)
        familyInput.setStyleSheet('''
                            border: 1px solid black;
                            height: 25px;
                            background-color: white;
                            font-size: 15px;
                        ''')
        familyLabel = QLabel("Family:")
        familyLabel.setStyleSheet('''
                            font-size: 15px;
                        ''')
        familyBox.addWidget(familyLabel)
        familyBox.addWidget(familyInput)
        addBox.addLayout(familyBox)

        armorBox = QHBoxLayout()
        armorInput = QLineEdit()
        armorInput.setFixedWidth(180)
        armorInput.setStyleSheet('''
                border: 1px solid black;
                height: 25px;
                background-color: white;
                font-size: 15px;
            ''')
        armorLabel = QLabel("Armor:")
        armorLabel.setStyleSheet('''
                font-size: 15px;
            ''')
        speedInput = QLineEdit()
        speedInput.setFixedWidth(180)
        speedInput.setStyleSheet('''
                border: 1px solid black;
                height: 25px;
                background-color: white;
                font-size: 15px;
            ''')
        speedLabel = QLabel("Speed:")
        speedLabel.setStyleSheet('''
                font-size: 15px;
            ''')
        armorBox.addWidget(armorLabel)
        armorBox.addWidget(armorInput)
        armorBox.addWidget(speedLabel)
        armorBox.addWidget(speedInput)
        addBox.addLayout(armorBox)

        lifeBox = QHBoxLayout()
        lifeInput = QLineEdit()
        lifeInput.setFixedWidth(180)
        lifeInput.setStyleSheet('''
                                border: 1px solid black;
                                height: 25px;
                                background-color: white;
                                font-size: 15px;
                            ''')
        lifeLabel = QLabel("HP:")
        lifeLabel.setStyleSheet('''
                                font-size: 15px;
                            ''')
        challengeInput = QLineEdit()
        challengeInput.setFixedWidth(180)
        challengeInput.setStyleSheet('''
                                border: 1px solid black;
                                height: 25px;
                                background-color: white;
                                font-size: 15px;
                            ''')
        challengeLabel = QLabel("Challenge:")
        challengeLabel.setStyleSheet('''
                                font-size: 15px;
                            ''')
        lifeBox.addWidget(lifeLabel)
        lifeBox.addWidget(lifeInput)
        lifeBox.addWidget(challengeLabel)
        lifeBox.addWidget(challengeInput)
        addBox.addLayout(lifeBox)

        statsUpBox = QHBoxLayout()
        strInput = QLineEdit()
        strInput.setFixedWidth(50)
        strInput.setStyleSheet('''
                                border: 1px solid black;
                                height: 25px;
                                background-color: white;
                                font-size: 15px;
                            ''')
        strLabel = QLabel("Strength:")
        strLabel.setStyleSheet('''
                                font-size: 15px;
                            ''')
        dexInput = QLineEdit()
        dexInput.setFixedWidth(50)
        dexInput.setStyleSheet('''
                                border: 1px solid black;
                                height: 25px;
                                background-color: white;
                                font-size: 15px;
                            ''')
        dexLabel = QLabel("Dexterity:")
        dexLabel.setStyleSheet('''
                                font-size: 15px;
                            ''')
        constInput = QLineEdit()
        constInput.setFixedWidth(50)
        constInput.setStyleSheet('''
                        border: 1px solid black;
                        height: 25px;
                        background-color: white;
                        font-size: 15px;
                    ''')
        constLabel = QLabel("Constitution:")
        constLabel.setStyleSheet('''
                    font-size: 15px;
        ''')
        statsUpBox.addWidget(strLabel)
        statsUpBox.addWidget(strInput)
        statsUpBox.addWidget(dexLabel)
        statsUpBox.addWidget(dexInput)
        statsUpBox.addWidget(constLabel)
        statsUpBox.addWidget(constInput)
        addBox.addLayout(statsUpBox)

        statsDownBox = QHBoxLayout()
        intInput = QLineEdit()
        intInput.setFixedWidth(50)
        intInput.setStyleSheet('''
                                border: 1px solid black;
                                height: 25px;
                                background-color: white;
                                font-size: 15px;
                            ''')
        intLabel = QLabel("Intelligence:")
        intLabel.setStyleSheet('''
                                font-size: 15px;
                            ''')
        wisInput = QLineEdit()
        wisInput.setFixedWidth(50)
        wisInput.setStyleSheet('''
                                border: 1px solid black;
                                height: 25px;
                                background-color: white;
                                font-size: 15px;
                            ''')
        wisLabel = QLabel("Wisdom:")
        wisLabel.setStyleSheet('''
                                    font-size: 15px;
                                ''')
        chaInput = QLineEdit()
        chaInput.setFixedWidth(50)
        chaInput.setStyleSheet('''
                                border: 1px solid black;
                                height: 25px;
                                background-color: white;
                                font-size: 15px;
                            ''')
        chaLabel = QLabel("Charisma:")
        chaLabel.setStyleSheet('''
                                font-size: 15px;
                            ''')
        statsDownBox.addWidget(intLabel)
        statsDownBox.addWidget(intInput)
        statsDownBox.addWidget(wisLabel)
        statsDownBox.addWidget(wisInput)
        statsDownBox.addWidget(chaLabel)
        statsDownBox.addWidget(chaInput)
        addBox.addLayout(statsDownBox)

        descBox = QHBoxLayout()
        descInput = QTextEdit()
        descInput.setFixedWidth(380)
        descInput.setFixedHeight(150)
        descInput.setStyleSheet('''
                   border: 1px solid black;
                   height: 25px;
                   background-color: white;
                   font-size: 15px;
               ''')
        descLabel = QLabel("Description:")
        descLabel.setStyleSheet('''
                    font-size: 15px;
                ''')
        descBox.addWidget(descLabel)
        descBox.addWidget(descInput)
        addBox.addLayout(descBox)

        addButton = QPushButton("Add")
        addButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        addButton.setFixedWidth(75)
        addButton.setStyleSheet('''
                    background-color: green;
                    font-size: 15px;
                    padding: 3px;
                ''')
        addButton.clicked.connect(addMonster)
        addBox.addWidget(addButton, alignment=QtCore.Qt.AlignCenter)
        addDialog.setLayout(addBox)
        addDialog.exec_()

    global monsterWindow
    monsterWindow = QWidget()
    monsterWindow.setWindowTitle("DND Helper")
    monsterWindow.setFixedWidth(1000)
    monsterWindow.setFixedHeight(600)
    monsterWindow.setStyleSheet("background: #00b4ff;")

    monster_vbox = QVBoxLayout()
    monster_vbox.setAlignment(QtCore.Qt.AlignCenter)

    monster_list = QGroupBox()
    monsters = QVBoxLayout()
    if userRole is UserRole.DUNGEON_MASTER:
        addMonsterButton = QPushButton("Add new monster")
        addMonsterButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        addMonsterButton.clicked.connect(addMonsterDialog)
        addMonsterButton.setFixedHeight(50)
        addMonsterButton.setStyleSheet('''
           background-color: lightgreen;
           font-size: 15px;
       ''')
        monsters.addWidget(addMonsterButton, alignment=QtCore.Qt.AlignCenter)
    for db_monster in DatabaseHandler.get_monsters_collection():
        monster_from_db = Monster.monster_from_db_entry(db_monster)
        monster_list_entry = QLabel(
            "Name: " + monster_from_db.name + "\nFamily: " + monster_from_db.family +
            "\nArmor class: " + str(monster_from_db.armor_class) + "\t\tSpeed: " + str(monster_from_db.speed) +
            "\nMaximum hit points: " + str(monster_from_db.max_hit_points) +
            "\nStrength: " + str(monster_from_db.strength) + " (" + str(monster_from_db.get_strength_modifier()) + ")" +
            "\t\tDexterity: " + str(monster_from_db.dexterity) + " (" + str(monster_from_db.get_dexterity_modifier()) + ")" +
            "\nConstitution: " + str(monster_from_db.constitution) + " (" + str(monster_from_db.get_constitution_modifier()) + ")" +
            "\t\tIntelligence: " + str(monster_from_db.intelligence) + " (" + str(monster_from_db.get_intelligence_modifier()) + ")" +
            "\nWisdom: " + str(monster_from_db.wisdom) + " (" + str(monster_from_db.get_wisdom_modifier()) + ")" +
            "\t\tCharisma: " + str(monster_from_db.charisma) + " (" + str(monster_from_db.get_charisma_modifier()) + ")" +
            "\nChallenge rating: " + str(monster_from_db.challenge_rating) + " (exp: " + str(monster_from_db.get_exp_value()) + ", prof: " + str(monster_from_db.get_prof_bonus()) + ")" +
            "\nDescription: " + monster_from_db.description
        )
        monster_list_entry.setFixedWidth(700)
        monster_list_entry.setWordWrap(True)
        monster_list_entry.setStyleSheet('''
                        background-color: green;
                        font-size: 15px;
                        padding: 5px;
                    ''')
        monsters.addWidget(monster_list_entry, alignment=QtCore.Qt.AlignCenter)
    monster_list.setLayout(monsters)
    scrollable_monster_list = QScrollArea()
    scrollable_monster_list.setWidget(monster_list)
    scrollable_monster_list.setWidgetResizable(True)
    scrollable_monster_list.setFixedHeight(500)
    scrollable_monster_list.setFixedWidth(800)
    scrollable_monster_list.setStyleSheet('''
            background-color: lightgray;
        ''')
    monster_vbox.addWidget(scrollable_monster_list, alignment=QtCore.Qt.AlignCenter)

    monsterWindow.setLayout(monster_vbox)
    monsterWindow.show()

def character_creation_frame():
    def create_character():
        skillList = []
        for skill in skillCheckList:
            if skill.isChecked():
                skillList.append(skill.text())
        savingList = []
        for attr in savingCheckList:
            if attr.isChecked():
                savingList.append(attr.text())
        new_character = Character.character_new(
            user.login, nameField.text(), classField.text(), raceField.text(), alignmentField.text(),
            backgroundField.text(), int(strField.text()), int(dexField.text()), int(constField.text()),
            int(intField.text()), int(wisField.text()), int(chaField.text()), int(armorField.text()),
            int(speedField.text()), int(hitDiceField.text()), traitsField.toPlainText(), profLangField.toPlainText(),
            eqField.toPlainText(), notesField.toPlainText(), spellField.toPlainText(),
            int(inspirationField.text()), int(levelField.text()), int(expField.text()),
            skillList, savingList
        )
        DatabaseHandler.insert_character(new_character)

    global creationWindow
    creationWindow = QWidget()
    creationWindow.setWindowTitle("DND Helper")
    creationWindow.setFixedWidth(1000)
    creationWindow.setFixedHeight(875)
    creationWindow.setStyleSheet("background: #00b4ff;")

    grid = QGridLayout()
    grid.setAlignment(QtCore.Qt.AlignCenter)

    nameBox = QHBoxLayout()
    nameBox.setAlignment(QtCore.Qt.AlignCenter)
    nameLabel = QLabel("Name:")
    nameLabel.setAlignment(QtCore.Qt.AlignCenter)
    nameField = QLineEdit()
    nameField.setStyleSheet('''color: black;
            background-color: white;
        ''')
    nameField.setFixedWidth(75)
    nameField.setAlignment(QtCore.Qt.AlignCenter)
    nameBox.addWidget(nameLabel)
    nameBox.addWidget(nameField)
    grid.addLayout(nameBox, 0, 0, alignment=QtCore.Qt.AlignCenter)

    classBox = QHBoxLayout()
    classBox.setAlignment(QtCore.Qt.AlignCenter)
    classLabel = QLabel("Class:")
    classLabel.setAlignment(QtCore.Qt.AlignCenter)
    classField = QLineEdit()
    classField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    classField.setFixedWidth(75)
    classField.setAlignment(QtCore.Qt.AlignCenter)
    classBox.addWidget(classLabel)
    classBox.addWidget(classField)
    grid.addLayout(classBox, 0, 1, alignment=QtCore.Qt.AlignCenter)

    levelBox = QHBoxLayout()
    levelBox.setAlignment(QtCore.Qt.AlignCenter)
    levelLabel = QLabel("Level:")
    levelLabel.setAlignment(QtCore.Qt.AlignCenter)
    levelField = QLineEdit()
    levelField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    levelField.setFixedWidth(75)
    levelField.setAlignment(QtCore.Qt.AlignCenter)
    levelBox.addWidget(levelLabel)
    levelBox.addWidget(levelField)
    grid.addLayout(levelBox, 0, 2, alignment=QtCore.Qt.AlignCenter)

    backgroundBox = QHBoxLayout()
    backgroundBox.setAlignment(QtCore.Qt.AlignCenter)
    backgroundLabel = QLabel("Background:")
    backgroundLabel.setAlignment(QtCore.Qt.AlignCenter)
    backgroundField = QLineEdit()
    backgroundField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    backgroundField.setFixedWidth(75)
    backgroundField.setAlignment(QtCore.Qt.AlignCenter)
    backgroundBox.addWidget(backgroundLabel)
    backgroundBox.addWidget(backgroundField)
    grid.addLayout(backgroundBox, 0, 3, alignment=QtCore.Qt.AlignCenter)

    playerBox = QHBoxLayout()
    playerBox.setAlignment(QtCore.Qt.AlignCenter)
    playerLabel = QLabel("Player:")
    playerLabel.setAlignment(QtCore.Qt.AlignCenter)
    playerField = QLineEdit(user.login)
    playerField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    playerField.setDisabled(True)
    playerField.setFixedWidth(75)
    playerField.setAlignment(QtCore.Qt.AlignCenter)
    playerBox.addWidget(playerLabel)
    playerBox.addWidget(playerField)
    grid.addLayout(playerBox, 0, 4, alignment=QtCore.Qt.AlignCenter)

    raceBox = QHBoxLayout()
    raceBox.setAlignment(QtCore.Qt.AlignCenter)
    raceLabel = QLabel("Race:")
    raceLabel.setAlignment(QtCore.Qt.AlignCenter)
    raceField = QLineEdit()
    raceField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    raceField.setFixedWidth(75)
    raceField.setAlignment(QtCore.Qt.AlignCenter)
    raceBox.addWidget(raceLabel)
    raceBox.addWidget(raceField)
    grid.addLayout(raceBox, 1, 1, alignment=QtCore.Qt.AlignCenter)

    alignmentBox = QHBoxLayout()
    alignmentBox.setAlignment(QtCore.Qt.AlignCenter)
    alignmentLabel = QLabel("Alignment:")
    alignmentLabel.setAlignment(QtCore.Qt.AlignCenter)
    alignmentField = QLineEdit()
    alignmentField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    alignmentField.setFixedWidth(75)
    alignmentField.setAlignment(QtCore.Qt.AlignCenter)
    alignmentBox.addWidget(alignmentLabel)
    alignmentBox.addWidget(alignmentField)
    grid.addLayout(alignmentBox, 1, 2, alignment=QtCore.Qt.AlignCenter)

    expBox = QHBoxLayout()
    expBox.setAlignment(QtCore.Qt.AlignCenter)
    expLabel = QLabel("Experience:")
    expLabel.setAlignment(QtCore.Qt.AlignCenter)
    expField = QLineEdit()
    expField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    expField.setFixedWidth(75)
    expField.setAlignment(QtCore.Qt.AlignCenter)
    expBox.addWidget(expLabel)
    expBox.addWidget(expField)
    grid.addLayout(expBox, 1, 3, alignment=QtCore.Qt.AlignCenter)

    inspirationBox = QHBoxLayout()
    inspirationBox.setAlignment(QtCore.Qt.AlignCenter)
    inspirationLabel = QLabel("Inspiration:")
    inspirationLabel.setAlignment(QtCore.Qt.AlignCenter)
    inspirationField = QLineEdit("0")
    inspirationField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    inspirationField.setFixedWidth(75)
    inspirationField.setAlignment(QtCore.Qt.AlignCenter)
    inspirationBox.addWidget(inspirationLabel)
    inspirationBox.addWidget(inspirationField)
    grid.addLayout(inspirationBox, 3, 0, alignment=QtCore.Qt.AlignCenter)

    strBox = QHBoxLayout()
    strBox.setAlignment(QtCore.Qt.AlignCenter)
    strLabel = QLabel("Strength:")
    strLabel.setAlignment(QtCore.Qt.AlignCenter)
    strField = QLineEdit("0")
    strField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    strField.setFixedWidth(75)
    strField.setAlignment(QtCore.Qt.AlignCenter)
    strBox.addWidget(strLabel)
    strBox.addWidget(strField)
    grid.addLayout(strBox, 6, 0, alignment=QtCore.Qt.AlignCenter)

    dexBox = QHBoxLayout()
    dexBox.setAlignment(QtCore.Qt.AlignCenter)
    dexLabel = QLabel("Dexterity:")
    dexLabel.setAlignment(QtCore.Qt.AlignCenter)
    dexField = QLineEdit("0")
    dexField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    dexField.setFixedWidth(75)
    dexField.setAlignment(QtCore.Qt.AlignCenter)
    dexBox.addWidget(dexLabel)
    dexBox.addWidget(dexField)
    grid.addLayout(dexBox, 7, 0, alignment=QtCore.Qt.AlignCenter)

    constBox = QHBoxLayout()
    constBox.setAlignment(QtCore.Qt.AlignCenter)
    constLabel = QLabel("Constitution:")
    constLabel.setAlignment(QtCore.Qt.AlignCenter)
    constField = QLineEdit("0")
    constField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    constField.setFixedWidth(75)
    constField.setAlignment(QtCore.Qt.AlignCenter)
    constBox.addWidget(constLabel)
    constBox.addWidget(constField)
    grid.addLayout(constBox, 8, 0, alignment=QtCore.Qt.AlignCenter)

    intBox = QHBoxLayout()
    intBox.setAlignment(QtCore.Qt.AlignCenter)
    intLabel = QLabel("Intelligence:")
    intLabel.setAlignment(QtCore.Qt.AlignCenter)
    intField = QLineEdit("0")
    intField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    intField.setFixedWidth(75)
    intField.setAlignment(QtCore.Qt.AlignCenter)
    intBox.addWidget(intLabel)
    intBox.addWidget(intField)
    grid.addLayout(intBox, 9, 0, alignment=QtCore.Qt.AlignCenter)

    wisBox = QHBoxLayout()
    wisBox.setAlignment(QtCore.Qt.AlignCenter)
    wisLabel = QLabel("Wisdom:")
    wisLabel.setAlignment(QtCore.Qt.AlignCenter)
    wisField = QLineEdit("0")
    wisField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    wisField.setFixedWidth(75)
    wisField.setAlignment(QtCore.Qt.AlignCenter)
    wisBox.addWidget(wisLabel)
    wisBox.addWidget(wisField)
    grid.addLayout(wisBox, 10, 0, alignment=QtCore.Qt.AlignCenter)

    chaBox = QHBoxLayout()
    chaBox.setAlignment(QtCore.Qt.AlignCenter)
    chaLabel = QLabel("Charisma:")
    chaLabel.setAlignment(QtCore.Qt.AlignCenter)
    chaField = QLineEdit("0")
    chaField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    chaField.setFixedWidth(75)
    chaField.setAlignment(QtCore.Qt.AlignCenter)
    chaBox.addWidget(chaLabel)
    chaBox.addWidget(chaField)
    grid.addLayout(chaBox, 11, 0, alignment=QtCore.Qt.AlignCenter)

    savingBox = QHBoxLayout()
    savingBox.setAlignment(QtCore.Qt.AlignCenter)
    savingLabel = QLabel("Saving throws\nproficiencies:")
    savingLabel.setAlignment(QtCore.Qt.AlignCenter)

    savingVBox = QVBoxLayout()
    savingCheckList = []
    savingAttrList = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    for attr in savingAttrList:
        savingCheck = QCheckBox(attr)
        savingCheckList.append(savingCheck)
        savingVBox.addWidget(savingCheck)
    savingBox.addWidget(savingLabel)
    savingBox.addLayout(savingVBox)
    grid.addLayout(savingBox, 2, 1, 4, 1, alignment=QtCore.Qt.AlignCenter)

    skillBox = QHBoxLayout()
    skillBox.setAlignment(QtCore.Qt.AlignCenter)
    skillLabel = QLabel("Skill\nproficiencies:")
    skillLabel.setAlignment(QtCore.Qt.AlignCenter)

    skillVBox = QVBoxLayout()
    skillCheckList = []
    skillProfList = ["acrobatics", "animal handling", "arcana", "athletics", "deception", "history", "insight",
                     "intimidation", "investigation", "medicine", "nature", "perception", "performance", "persuasion",
                     "religion", "sleight of hand", "stealth", "survival"]
    for prof in skillProfList:
        skillCheck = QCheckBox(prof)
        skillCheckList.append(skillCheck)
        skillVBox.addWidget(skillCheck)
    skillBox.addWidget(skillLabel)
    skillBox.addLayout(skillVBox)
    grid.addLayout(skillBox, 6, 1, 7, 1, alignment=QtCore.Qt.AlignCenter)

    armorBox = QHBoxLayout()
    armorBox.setAlignment(QtCore.Qt.AlignCenter)
    armorLabel = QLabel("Armor class:")
    armorLabel.setAlignment(QtCore.Qt.AlignCenter)
    armorField = QLineEdit("0")
    armorField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    armorField.setFixedWidth(75)
    armorField.setAlignment(QtCore.Qt.AlignCenter)
    armorBox.addWidget(armorLabel)
    armorBox.addWidget(armorField)
    grid.addLayout(armorBox, 3, 2, alignment=QtCore.Qt.AlignCenter)

    speedBox = QHBoxLayout()
    speedBox.setAlignment(QtCore.Qt.AlignCenter)
    speedLabel = QLabel("Speed:")
    speedLabel.setAlignment(QtCore.Qt.AlignCenter)
    speedField = QLineEdit("0")
    speedField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    speedField.setFixedWidth(75)
    speedField.setAlignment(QtCore.Qt.AlignCenter)
    speedBox.addWidget(speedLabel)
    speedBox.addWidget(speedField)
    grid.addLayout(speedBox, 4, 2, alignment=QtCore.Qt.AlignCenter)

    hitDiceBox = QHBoxLayout()
    hitDiceBox.setAlignment(QtCore.Qt.AlignCenter)
    hitDiceLabel = QLabel("Hit Dice: d")
    hitDiceLabel.setAlignment(QtCore.Qt.AlignCenter)
    hitDiceField = QLineEdit()
    hitDiceField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    hitDiceField.setFixedWidth(75)
    hitDiceField.setAlignment(QtCore.Qt.AlignCenter)
    hitDiceBox.addWidget(hitDiceLabel)
    hitDiceBox.addWidget(hitDiceField)
    grid.addLayout(hitDiceBox, 6, 2, alignment=QtCore.Qt.AlignCenter)

    traitsBox = QHBoxLayout()
    traitsBox.setAlignment(QtCore.Qt.AlignCenter)
    traitsLabel = QLabel("Traits:")
    traitsLabel.setAlignment(QtCore.Qt.AlignCenter)
    traitsField = QTextEdit()
    traitsField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    traitsField.setFixedWidth(250)
    traitsField.setFixedHeight(125)
    traitsField.setAlignment(QtCore.Qt.AlignLeft)
    traitsBox.addWidget(traitsLabel)
    traitsBox.addWidget(traitsField)
    grid.addLayout(traitsBox, 3, 3, 2, 2, alignment=QtCore.Qt.AlignCenter)

    profLangBox = QHBoxLayout()
    profLangBox.setAlignment(QtCore.Qt.AlignCenter)
    profLangLabel = QLabel("Other proficiencies\nand languages:")
    profLangLabel.setAlignment(QtCore.Qt.AlignCenter)
    profLangField = QTextEdit()
    profLangField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    profLangField.setFixedWidth(250)
    profLangField.setFixedHeight(125)
    profLangField.setAlignment(QtCore.Qt.AlignLeft)
    profLangBox.addWidget(profLangLabel)
    profLangBox.addWidget(profLangField)
    grid.addLayout(profLangBox, 5, 3, 2, 2, alignment=QtCore.Qt.AlignCenter)

    eqBox = QHBoxLayout()
    eqBox.setAlignment(QtCore.Qt.AlignCenter)
    eqLabel = QLabel("Equipment:")
    eqLabel.setAlignment(QtCore.Qt.AlignCenter)
    eqField = QTextEdit()
    eqField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    eqField.setFixedWidth(250)
    eqField.setFixedHeight(125)
    eqField.setAlignment(QtCore.Qt.AlignLeft)
    eqBox.addWidget(eqLabel)
    eqBox.addWidget(eqField)
    grid.addLayout(eqBox, 7, 3, 2, 2, alignment=QtCore.Qt.AlignCenter)

    spellBox = QHBoxLayout()
    spellBox.setAlignment(QtCore.Qt.AlignCenter)
    spellLabel = QLabel("Spells:")
    spellLabel.setAlignment(QtCore.Qt.AlignCenter)
    spellField = QTextEdit()
    spellField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    spellField.setFixedWidth(250)
    spellField.setFixedHeight(125)
    spellField.setAlignment(QtCore.Qt.AlignLeft)
    spellBox.addWidget(spellLabel)
    spellBox.addWidget(spellField)
    grid.addLayout(spellBox, 9, 3, 2, 2, alignment=QtCore.Qt.AlignCenter)

    notesLabel = QLabel("Notes:")
    notesLabel.setAlignment(QtCore.Qt.AlignCenter)
    grid.addWidget(notesLabel, 12, 0)
    notesField = QTextEdit()
    notesField.setStyleSheet('''color: black;
                background-color: white;
        ''')
    notesField.setFixedWidth(800)
    notesField.setFixedHeight(125)
    notesField.setAlignment(QtCore.Qt.AlignLeft)
    grid.addWidget(notesField, 13, 0, 2, 4, alignment=QtCore.Qt.AlignLeft)

    createButton = QPushButton("Create")
    createButton.setFixedHeight(40)
    createButton.setFixedWidth(80)
    createButton.setStyleSheet('''
            background-color: green;
        ''')
    createButton.clicked.connect(create_character)
    grid.addWidget(createButton, 14, 4, alignment=QtCore.Qt.AlignCenter)

    creationWindow.setLayout(grid)

    creationWindow.show()

def character_sheet_frame(character_id):
    def refresh_character_sheet():
        levelField.setText(str(character.level))
        expField.setText(str(character.exp))
        profField.setText(str(character.get_proficiency_bonus()))
        strModLabel.setText("Mod: " + str(character.get_strength_modifier()))
        dexModLabel.setText("Mod: " + str(character.get_dexterity_modifier()))
        constModLabel.setText("Mod: " + str(character.get_constitution_modifier()))
        intModLabel.setText("Mod: " + str(character.get_intelligence_modifier()))
        wisModLabel.setText("Mod: " + str(character.get_wisdom_modifier()))
        chaModLabel.setText("Mod: " + str(character.get_charisma_modifier()))
        hpField.setText(str(character.current_hit_points))
        hpMaxLabel.setText(" / " + str(character.max_hit_points))
        hitDiceFacesLabel.setText(" / " + str(character.level) + " d" + str(character.hit_dice_faces))
        hitDiceField.setText(str(character.no_hit_dice))


    def save_changes():
        global character
        character.alignment = alignmentField.text()
        character.inspiration = int(inspirationField.text())
        character.strength = int(strField.text())
        character.dexterity = int(dexField.text())
        character.constitution = int(constField.text())
        character.intelligence = int(intField.text())
        character.wisdom = int(wisField.text())
        character.charisma = int(chaField.text())

        newSavings = []
        for check in savingCheckList:
            if check.isChecked():
                newSavings.append(check.text())
        character.saving_throw_proficiency = newSavings

        newSkills = []
        for check in skillCheckList:
            if check.isChecked():
                newSkills.append(check.text())
        character.skill_proficiency = newSkills

        character.armor_class = int(armorField.text())
        character.speed = int(speedField.text())
        character.current_hit_points = int(hpField.text())
        character.no_hit_dice = int(hitDiceField.text())
        character.death_saving_throw_failures = int(deathFailureField.text())
        character.death_saving_throw_successes = int(deathSuccessField.text())
        character.features_traits = traitsField.toPlainText()
        character.proficiencies_languages = profLangField.toPlainText()
        character.equipment = eqField.toPlainText()
        character.spells_list = spellField.toPlainText()
        character.notes = notesField.toPlainText()
        character.add_exp(int(expField.text()) - character.exp)
        DatabaseHandler.update_character(character)
        refresh_character_sheet()

    global sheetWindow
    sheetWindow = QWidget()
    sheetWindow.setWindowTitle("DND Helper")
    sheetWindow.setFixedWidth(1000)
    sheetWindow.setFixedHeight(875)
    sheetWindow.setStyleSheet("background: #00b4ff;")

    global character
    character = Character.character_from_db_entry(DatabaseHandler.get_character(character_id))

    grid = QGridLayout()
    grid.setAlignment(QtCore.Qt.AlignCenter)

    nameBox = QHBoxLayout()
    nameBox.setAlignment(QtCore.Qt.AlignCenter)
    nameLabel = QLabel("Name:")
    nameLabel.setAlignment(QtCore.Qt.AlignCenter)
    nameField = QLineEdit(character.name)
    nameField.setStyleSheet('''color: black;
        background-color: white;
    ''')
    nameField.setDisabled(True)
    nameField.setFixedWidth(75)
    nameField.setAlignment(QtCore.Qt.AlignCenter)
    nameBox.addWidget(nameLabel)
    nameBox.addWidget(nameField)
    grid.addLayout(nameBox, 0, 0, alignment=QtCore.Qt.AlignCenter)

    classBox = QHBoxLayout()
    classBox.setAlignment(QtCore.Qt.AlignCenter)
    classLabel = QLabel("Class:")
    classLabel.setAlignment(QtCore.Qt.AlignCenter)
    classField = QLineEdit(character.c_class)
    classField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    classField.setDisabled(True)
    classField.setFixedWidth(75)
    classField.setAlignment(QtCore.Qt.AlignCenter)
    classBox.addWidget(classLabel)
    classBox.addWidget(classField)
    grid.addLayout(classBox, 0, 1, alignment=QtCore.Qt.AlignCenter)

    levelBox = QHBoxLayout()
    levelBox.setAlignment(QtCore.Qt.AlignCenter)
    levelLabel = QLabel("Level:")
    levelLabel.setAlignment(QtCore.Qt.AlignCenter)
    levelField = QLineEdit(str(character.level))
    levelField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    levelField.setDisabled(True)
    levelField.setFixedWidth(75)
    levelField.setAlignment(QtCore.Qt.AlignCenter)
    levelBox.addWidget(levelLabel)
    levelBox.addWidget(levelField)
    grid.addLayout(levelBox, 0, 2, alignment=QtCore.Qt.AlignCenter)

    backgroundBox = QHBoxLayout()
    backgroundBox.setAlignment(QtCore.Qt.AlignCenter)
    backgroundLabel = QLabel("Background:")
    backgroundLabel.setAlignment(QtCore.Qt.AlignCenter)
    backgroundField = QLineEdit(character.background)
    backgroundField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    backgroundField.setDisabled(True)
    backgroundField.setFixedWidth(75)
    backgroundField.setAlignment(QtCore.Qt.AlignCenter)
    backgroundBox.addWidget(backgroundLabel)
    backgroundBox.addWidget(backgroundField)
    grid.addLayout(backgroundBox, 0, 3, alignment=QtCore.Qt.AlignCenter)

    playerBox = QHBoxLayout()
    playerBox.setAlignment(QtCore.Qt.AlignCenter)
    playerLabel = QLabel("Player:")
    playerLabel.setAlignment(QtCore.Qt.AlignCenter)
    playerField = QLineEdit(character.user)
    playerField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    playerField.setDisabled(True)
    playerField.setFixedWidth(75)
    playerField.setAlignment(QtCore.Qt.AlignCenter)
    playerBox.addWidget(playerLabel)
    playerBox.addWidget(playerField)
    grid.addLayout(playerBox, 0, 4, alignment=QtCore.Qt.AlignCenter)

    raceBox = QHBoxLayout()
    raceBox.setAlignment(QtCore.Qt.AlignCenter)
    raceLabel = QLabel("Race:")
    raceLabel.setAlignment(QtCore.Qt.AlignCenter)
    raceField = QLineEdit(character.race)
    raceField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    raceField.setDisabled(True)
    raceField.setFixedWidth(75)
    raceField.setAlignment(QtCore.Qt.AlignCenter)
    raceBox.addWidget(raceLabel)
    raceBox.addWidget(raceField)
    grid.addLayout(raceBox, 1, 1, alignment=QtCore.Qt.AlignCenter)

    alignmentBox = QHBoxLayout()
    alignmentBox.setAlignment(QtCore.Qt.AlignCenter)
    alignmentLabel = QLabel("Alignment:")
    alignmentLabel.setAlignment(QtCore.Qt.AlignCenter)
    alignmentField = QLineEdit(character.alignment)
    alignmentField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    alignmentField.setFixedWidth(75)
    alignmentField.setAlignment(QtCore.Qt.AlignCenter)
    alignmentBox.addWidget(alignmentLabel)
    alignmentBox.addWidget(alignmentField)
    grid.addLayout(alignmentBox, 1, 2, alignment=QtCore.Qt.AlignCenter)

    expBox = QHBoxLayout()
    expBox.setAlignment(QtCore.Qt.AlignCenter)
    expLabel = QLabel("Experience:")
    expLabel.setAlignment(QtCore.Qt.AlignCenter)
    expField = QLineEdit(str(character.exp))
    expField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    expField.setFixedWidth(75)
    expField.setAlignment(QtCore.Qt.AlignCenter)
    expBox.addWidget(expLabel)
    expBox.addWidget(expField)
    grid.addLayout(expBox, 1, 3, alignment=QtCore.Qt.AlignCenter)

    inspirationBox = QHBoxLayout()
    inspirationBox.setAlignment(QtCore.Qt.AlignCenter)
    inspirationLabel = QLabel("Inspiration:")
    inspirationLabel.setAlignment(QtCore.Qt.AlignCenter)
    inspirationField = QLineEdit(str(character.inspiration))
    inspirationField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    inspirationField.setFixedWidth(75)
    inspirationField.setAlignment(QtCore.Qt.AlignCenter)
    inspirationBox.addWidget(inspirationLabel)
    inspirationBox.addWidget(inspirationField)
    grid.addLayout(inspirationBox, 3, 0, alignment=QtCore.Qt.AlignCenter)

    profBox = QHBoxLayout()
    profBox.setAlignment(QtCore.Qt.AlignCenter)
    profLabel = QLabel("Proficiency bonus:")
    profLabel.setAlignment(QtCore.Qt.AlignCenter)
    profField = QLineEdit(str(character.get_proficiency_bonus()))
    profField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    profField.setDisabled(True)
    profField.setFixedWidth(75)
    profField.setAlignment(QtCore.Qt.AlignCenter)
    profBox.addWidget(profLabel)
    profBox.addWidget(profField)
    grid.addLayout(profBox, 4, 0, alignment=QtCore.Qt.AlignCenter)

    strBox = QHBoxLayout()
    strBox.setAlignment(QtCore.Qt.AlignCenter)
    strLabel = QLabel("Strength:")
    strLabel.setAlignment(QtCore.Qt.AlignCenter)
    strField = QLineEdit(str(character.strength))
    strField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    strField.setFixedWidth(75)
    strField.setAlignment(QtCore.Qt.AlignCenter)
    strModLabel = QLabel("Mod: " + str(character.get_strength_modifier()))
    strModLabel.setAlignment(QtCore.Qt.AlignCenter)
    strBox.addWidget(strLabel)
    strBox.addWidget(strField)
    strBox.addWidget(strModLabel)
    grid.addLayout(strBox, 6, 0, alignment=QtCore.Qt.AlignCenter)

    dexBox = QHBoxLayout()
    dexBox.setAlignment(QtCore.Qt.AlignCenter)
    dexLabel = QLabel("Dexterity:")
    dexLabel.setAlignment(QtCore.Qt.AlignCenter)
    dexField = QLineEdit(str(character.dexterity))
    dexField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    dexField.setFixedWidth(75)
    dexField.setAlignment(QtCore.Qt.AlignCenter)
    dexModLabel = QLabel("Mod: " + str(character.get_dexterity_modifier()))
    dexModLabel.setAlignment(QtCore.Qt.AlignCenter)
    dexBox.addWidget(dexLabel)
    dexBox.addWidget(dexField)
    dexBox.addWidget(dexModLabel)
    grid.addLayout(dexBox, 7, 0, alignment=QtCore.Qt.AlignCenter)

    constBox = QHBoxLayout()
    constBox.setAlignment(QtCore.Qt.AlignCenter)
    constLabel = QLabel("Constitution:")
    constLabel.setAlignment(QtCore.Qt.AlignCenter)
    constField = QLineEdit(str(character.constitution))
    constField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    constField.setFixedWidth(75)
    constField.setAlignment(QtCore.Qt.AlignCenter)
    constModLabel = QLabel("Mod: " + str(character.get_constitution_modifier()))
    constModLabel.setAlignment(QtCore.Qt.AlignCenter)
    constBox.addWidget(constLabel)
    constBox.addWidget(constField)
    constBox.addWidget(constModLabel)
    grid.addLayout(constBox, 8, 0, alignment=QtCore.Qt.AlignCenter)

    intBox = QHBoxLayout()
    intBox.setAlignment(QtCore.Qt.AlignCenter)
    intLabel = QLabel("Intelligence:")
    intLabel.setAlignment(QtCore.Qt.AlignCenter)
    intField = QLineEdit(str(character.intelligence))
    intField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    intField.setFixedWidth(75)
    intField.setAlignment(QtCore.Qt.AlignCenter)
    intModLabel = QLabel("Mod: " + str(character.get_intelligence_modifier()))
    intModLabel.setAlignment(QtCore.Qt.AlignCenter)
    intBox.addWidget(intLabel)
    intBox.addWidget(intField)
    intBox.addWidget(intModLabel)
    grid.addLayout(intBox, 9, 0, alignment=QtCore.Qt.AlignCenter)

    wisBox = QHBoxLayout()
    wisBox.setAlignment(QtCore.Qt.AlignCenter)
    wisLabel = QLabel("Wisdom:")
    wisLabel.setAlignment(QtCore.Qt.AlignCenter)
    wisField = QLineEdit(str(character.wisdom))
    wisField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    wisField.setFixedWidth(75)
    wisField.setAlignment(QtCore.Qt.AlignCenter)
    wisModLabel = QLabel("Mod: " + str(character.get_wisdom_modifier()))
    wisModLabel.setAlignment(QtCore.Qt.AlignCenter)
    wisBox.addWidget(wisLabel)
    wisBox.addWidget(wisField)
    wisBox.addWidget(wisModLabel)
    grid.addLayout(wisBox, 10, 0, alignment=QtCore.Qt.AlignCenter)

    chaBox = QHBoxLayout()
    chaBox.setAlignment(QtCore.Qt.AlignCenter)
    chaLabel = QLabel("Charisma:")
    chaLabel.setAlignment(QtCore.Qt.AlignCenter)
    chaField = QLineEdit(str(character.charisma))
    chaField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    chaField.setFixedWidth(75)
    chaField.setAlignment(QtCore.Qt.AlignCenter)
    chaModLabel = QLabel("Mod: " + str(character.get_charisma_modifier()))
    chaModLabel.setAlignment(QtCore.Qt.AlignCenter)
    chaBox.addWidget(chaLabel)
    chaBox.addWidget(chaField)
    chaBox.addWidget(chaModLabel)
    grid.addLayout(chaBox, 11, 0, alignment=QtCore.Qt.AlignCenter)

    savingBox = QHBoxLayout()
    savingBox.setAlignment(QtCore.Qt.AlignCenter)
    savingLabel = QLabel("Saving throws\nproficiencies:")
    savingLabel.setAlignment(QtCore.Qt.AlignCenter)

    savingVBox = QVBoxLayout()
    savingCheckList = []
    savingAttrList = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    for attr in savingAttrList:
        savingCheck = QCheckBox(attr)
        savingCheck.setChecked(attr in character.saving_throw_proficiency)
        savingCheckList.append(savingCheck)
        savingVBox.addWidget(savingCheck)
    savingBox.addWidget(savingLabel)
    savingBox.addLayout(savingVBox)
    grid.addLayout(savingBox, 2, 1, 4, 1, alignment=QtCore.Qt.AlignCenter)

    skillBox = QHBoxLayout()
    skillBox.setAlignment(QtCore.Qt.AlignCenter)
    skillLabel = QLabel("Skill\nproficiencies:")
    skillLabel.setAlignment(QtCore.Qt.AlignCenter)


    skillVBox = QVBoxLayout()
    skillCheckList = []
    skillProfList = ["acrobatics", "animal handling", "arcana", "athletics", "deception", "history", "insight",
                     "intimidation", "investigation", "medicine", "nature", "perception", "performance", "persuasion",
                     "religion", "sleight of hand", "stealth", "survival"]
    for prof in skillProfList:
        skillCheck = QCheckBox(prof)
        skillCheck.setChecked(prof in character.skill_proficiency)
        skillCheckList.append(skillCheck)
        skillVBox.addWidget(skillCheck)
    skillBox.addWidget(skillLabel)
    skillBox.addLayout(skillVBox)
    grid.addLayout(skillBox, 6, 1, 7, 1, alignment=QtCore.Qt.AlignCenter)

    armorBox = QHBoxLayout()
    armorBox.setAlignment(QtCore.Qt.AlignCenter)
    armorLabel = QLabel("Armor class:")
    armorLabel.setAlignment(QtCore.Qt.AlignCenter)
    armorField = QLineEdit(str(character.armor_class))
    armorField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    armorField.setFixedWidth(75)
    armorField.setAlignment(QtCore.Qt.AlignCenter)
    armorBox.addWidget(armorLabel)
    armorBox.addWidget(armorField)
    grid.addLayout(armorBox, 3, 2, alignment=QtCore.Qt.AlignCenter)

    speedBox = QHBoxLayout()
    speedBox.setAlignment(QtCore.Qt.AlignCenter)
    speedLabel = QLabel("Speed:")
    speedLabel.setAlignment(QtCore.Qt.AlignCenter)
    speedField = QLineEdit(str(character.speed))
    speedField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    speedField.setFixedWidth(75)
    speedField.setAlignment(QtCore.Qt.AlignCenter)
    speedBox.addWidget(speedLabel)
    speedBox.addWidget(speedField)
    grid.addLayout(speedBox, 4, 2, alignment=QtCore.Qt.AlignCenter)

    hpBox = QHBoxLayout()
    hpBox.setAlignment(QtCore.Qt.AlignCenter)
    hpLabel = QLabel("Hit Points:")
    hpLabel.setAlignment(QtCore.Qt.AlignCenter)
    hpField = QLineEdit(str(character.current_hit_points))
    hpField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    hpField.setFixedWidth(25)
    hpField.setAlignment(QtCore.Qt.AlignCenter)
    hpMaxLabel = QLabel(" / " + str(character.max_hit_points))
    hpMaxLabel.setContentsMargins(0, 4, 0, 0)
    hpMaxLabel.setAlignment(QtCore.Qt.AlignLeft)
    hpBox.addWidget(hpLabel)
    hpBox.addWidget(hpField)
    hpBox.addWidget(hpMaxLabel)
    grid.addLayout(hpBox, 5, 2, alignment=QtCore.Qt.AlignCenter)

    hitDiceBox = QHBoxLayout()
    hitDiceBox.setAlignment(QtCore.Qt.AlignCenter)
    hitDiceLabel = QLabel("Hit Dice:")
    hitDiceLabel.setAlignment(QtCore.Qt.AlignCenter)
    hitDiceField = QLineEdit(str(character.no_hit_dice))
    hitDiceField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    hitDiceField.setFixedWidth(25)
    hitDiceField.setAlignment(QtCore.Qt.AlignCenter)
    hitDiceFacesLabel = QLabel(" / " + str(character.level) + " d" + str(character.hit_dice_faces))
    hitDiceFacesLabel.setContentsMargins(0, 4, 0, 0)
    hitDiceFacesLabel.setAlignment(QtCore.Qt.AlignLeft)
    hitDiceBox.addWidget(hitDiceLabel)
    hitDiceBox.addWidget(hitDiceField)
    hitDiceBox.addWidget(hitDiceFacesLabel)
    grid.addLayout(hitDiceBox, 6, 2, alignment=QtCore.Qt.AlignCenter)

    deathSuccessBox = QHBoxLayout()
    deathSuccessBox.setAlignment(QtCore.Qt.AlignCenter)
    deathSuccessLabel = QLabel("Death ST successes:")
    deathSuccessLabel.setAlignment(QtCore.Qt.AlignCenter)
    deathSuccessField = QLineEdit(str(character.death_saving_throw_successes))
    deathSuccessField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    deathSuccessField.setFixedWidth(25)
    deathSuccessField.setAlignment(QtCore.Qt.AlignCenter)
    deathSuccessMaxLabel = QLabel(" / 3")
    deathSuccessMaxLabel.setContentsMargins(0, 4, 0, 0)
    deathSuccessMaxLabel.setAlignment(QtCore.Qt.AlignLeft)
    deathSuccessBox.addWidget(deathSuccessLabel)
    deathSuccessBox.addWidget(deathSuccessField)
    deathSuccessBox.addWidget(deathSuccessMaxLabel)
    grid.addLayout(deathSuccessBox, 7, 2, alignment=QtCore.Qt.AlignCenter)

    deathFailureBox = QHBoxLayout()
    deathFailureBox.setAlignment(QtCore.Qt.AlignCenter)
    deathFailureLabel = QLabel("Death ST failures:")
    deathFailureLabel.setAlignment(QtCore.Qt.AlignCenter)
    deathFailureField = QLineEdit(str(character.death_saving_throw_failures))
    deathFailureField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    deathFailureField.setFixedWidth(25)
    deathFailureField.setAlignment(QtCore.Qt.AlignCenter)
    deathFailureMaxLabel = QLabel(" / 3")
    deathFailureMaxLabel.setContentsMargins(0, 4, 0, 0)
    deathFailureMaxLabel.setAlignment(QtCore.Qt.AlignLeft)
    deathFailureBox.addWidget(deathFailureLabel)
    deathFailureBox.addWidget(deathFailureField)
    deathFailureBox.addWidget(deathFailureMaxLabel)
    grid.addLayout(deathFailureBox, 8, 2, alignment=QtCore.Qt.AlignCenter)

    traitsBox = QHBoxLayout()
    traitsBox.setAlignment(QtCore.Qt.AlignCenter)
    traitsLabel = QLabel("Traits:")
    traitsLabel.setAlignment(QtCore.Qt.AlignCenter)
    traitsField = QTextEdit(character.features_traits)
    traitsField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    traitsField.setFixedWidth(250)
    traitsField.setFixedHeight(125)
    traitsField.setAlignment(QtCore.Qt.AlignLeft)
    traitsBox.addWidget(traitsLabel)
    traitsBox.addWidget(traitsField)
    grid.addLayout(traitsBox, 3, 3, 2, 2, alignment=QtCore.Qt.AlignCenter)

    profLangBox = QHBoxLayout()
    profLangBox.setAlignment(QtCore.Qt.AlignCenter)
    profLangLabel = QLabel("Other proficiencies\nand languages:")
    profLangLabel.setAlignment(QtCore.Qt.AlignCenter)
    profLangField = QTextEdit(character.proficiencies_languages)
    profLangField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    profLangField.setFixedWidth(250)
    profLangField.setFixedHeight(125)
    profLangField.setAlignment(QtCore.Qt.AlignLeft)
    profLangBox.addWidget(profLangLabel)
    profLangBox.addWidget(profLangField)
    grid.addLayout(profLangBox, 5, 3, 2, 2, alignment=QtCore.Qt.AlignCenter)

    eqBox = QHBoxLayout()
    eqBox.setAlignment(QtCore.Qt.AlignCenter)
    eqLabel = QLabel("Equipment:")
    eqLabel.setAlignment(QtCore.Qt.AlignCenter)
    eqField = QTextEdit(character.equipment)
    eqField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    eqField.setFixedWidth(250)
    eqField.setFixedHeight(125)
    eqField.setAlignment(QtCore.Qt.AlignLeft)
    eqBox.addWidget(eqLabel)
    eqBox.addWidget(eqField)
    grid.addLayout(eqBox, 7, 3, 2, 2, alignment=QtCore.Qt.AlignCenter)

    spellBox = QHBoxLayout()
    spellBox.setAlignment(QtCore.Qt.AlignCenter)
    spellLabel = QLabel("Spells:")
    spellLabel.setAlignment(QtCore.Qt.AlignCenter)
    spellField = QTextEdit(str(character.spells_list))
    spellField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    spellField.setFixedWidth(250)
    spellField.setFixedHeight(125)
    spellField.setAlignment(QtCore.Qt.AlignLeft)
    spellBox.addWidget(spellLabel)
    spellBox.addWidget(spellField)
    grid.addLayout(spellBox, 9, 3, 2, 2, alignment=QtCore.Qt.AlignCenter)


    notesLabel = QLabel("Notes:")
    notesLabel.setAlignment(QtCore.Qt.AlignCenter)
    grid.addWidget(notesLabel, 12, 0)
    notesField = QTextEdit(character.notes)
    notesField.setStyleSheet('''color: black;
            background-color: white;
    ''')
    notesField.setFixedWidth(800)
    notesField.setFixedHeight(125)
    notesField.setAlignment(QtCore.Qt.AlignLeft)
    grid.addWidget(notesField, 13, 0, 2, 4, alignment=QtCore.Qt.AlignLeft)

    saveButton = QPushButton("Save")
    saveButton.setFixedHeight(40)
    saveButton.setFixedWidth(80)
    saveButton.setStyleSheet('''
        background-color: green;
    ''')
    saveButton.clicked.connect(save_changes)
    grid.addWidget(saveButton, 14, 4, alignment=QtCore.Qt.AlignCenter)

    refresh_character_sheet()
    sheetWindow.setLayout(grid)

    sheetWindow.show()



if __name__ == '__main__':
    main()


