import math
import sys
import sqlite3
import datetime

import winsound
import io
import PIL.Image as Image

from PyQt6 import QtWidgets
from PyQt6 import QtGui
from PyQt6 import QtCore

class Start(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.con = sqlite3.connect("DarkAndDarkerItemList.db")
        self.cur = self.con.cursor()

        self.setGeometry(650, 250, 410, 200)
        self.setWindowTitle('Авторизация')


        self.frameStart = QtWidgets.QFrame(self)
        self.frameStart.setGeometry(QtCore.QRect(5, 5, 401, 191))
        self.frameStart.setStyleSheet(
            "background-color: gray;")
        self.frameStart.setObjectName("frame")



        self.textEditWarning = QtWidgets.QLabel(self.frameStart)
        self.textEditWarning.setGeometry(QtCore.QRect(20, 130, 271, 31))
        self.textEditWarning.setStyleSheet("background-color: rgb(244, 243, 255);\n"
                                    "border: 1px rgb(244, 243, 255);")



        self.pushButtonEnter = QtWidgets.QPushButton(self.frameStart)

        self.pushButtonEnter.setGeometry(QtCore.QRect(300, 130, 71, 31))
        self.pushButtonEnter.setStyleSheet("background-color: rgb(244, 243, 255);\n"
                                      "border: 1px rgb(244, 243, 255);")
        self.pushButtonEnter.setObjectName("pushButton")
        self.pushButtonEnter.setText("Вход")
        self.pushButtonEnter.clicked.connect(self.PasswordLoginCheck)



        self.textEdit_TextLogin = QtWidgets.QTextEdit(self.frameStart)
        self.textEdit_TextLogin.setGeometry(20, 30, 60, 32)
        self.textEdit_TextLogin.setStyleSheet("background-color: rgb(216, 216, 255);")
        self.textEdit_TextLogin.setText("Логин")
        self.textEdit_TextLogin.setReadOnly(True)

        self.textEdit_TextPassword = QtWidgets.QTextEdit(self.frameStart)
        self.textEdit_TextPassword.setGeometry(20, 80, 60, 32)
        self.textEdit_TextPassword.setStyleSheet("background-color: rgb(216, 216, 255);")
        self.textEdit_TextPassword.setText("Пароль")
        self.textEdit_TextPassword.setReadOnly(True)



        self.lineEdit_password = QtWidgets.QLineEdit(self)
        self.lineEdit_password.setGeometry(85, 85, 301, 30)
        self.lineEdit_password.setStyleSheet("background-color: rgb(244, 243, 255);\n"
                                    "border: 1px rgb(244, 243, 255);")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)



        self.lineEdit_login = QtWidgets.QLineEdit(self.frameStart)
        self.lineEdit_login.setGeometry(80, 30, 301, 31)
        self.lineEdit_login.setStyleSheet("background-color: rgb(244, 243, 255);\n"
                                      "border: 1px rgb(244, 243, 255);")

        self.show()


    def PasswordLoginCheck(self):
        self.login = self.lineEdit_login.text()
        self.password = self.lineEdit_password.text()
        self.key = self.login + self.password
        user = self.cur.execute("SELECT id FROM authorization1 WHERE login = ? AND password = ?",(self.lineEdit_login.text(), self.lineEdit_password.text())).fetchone()
        if user is None:
            self.textEditWarning.setText("Пароль или логин введён неверно!")
        else:
            Start.Enter(self)



    def Enter(self):
        self.historyWindow = HistoryWindow()
        self.main_window = MainWindow(self.lineEdit_login.text())
        self.main_stacked = MainStacked(self.main_window, self.historyWindow)
        self.main_stacked.show()
        self.close()


class MainStacked(QtWidgets.QMainWindow):
    def __init__(self, first, second):
        super().__init__()
        self.setWindowTitle("Dark & Darker Helper")
        self.setWindowIcon(QtGui.QIcon("./icon.jpg"))
        self.setGeometry(100,100, 475, 500)
        self.setFixedSize(800,550)

        self.con = sqlite3.connect("DarkAndDarkerItemList.db")
        self.cur = self.con.cursor()

        self.totalcostinfo = QtWidgets.QLabel(self)
        self.totalcostinfo.setText("Заработанная сумма с продажи всех предметов: ")
        self.totalcostinfo.setGeometry(150, 460,100,100)
        self.totalcostinfo.adjustSize()
        self.totalcostinfo.setVisible(False)

        self.stacked = QtWidgets.QStackedWidget(self)
        self.stacked.addWidget(first)
        self.stacked.addWidget(second)
        self.stacked.setCurrentIndex(0)
        self.stacked.setGeometry(0, 0, 700, 500)

        self.stacked.currentChanged.connect(self.page_changed)

        self.historyBut = QtWidgets.QPushButton(self)
        self.historyBut.setGeometry(550, 450, 50, 50)
        self.historyBut.setText("Items \n History")
        self.historyBut.adjustSize()
        self.historyBut.clicked.connect(self.on_historyBut_clicked)

        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(30, 30, 740, 400)
        self.table.setVisible(False)
        self.table.setColumnCount(5)
        self.table.setColumnWidth(0, 170)
        self.table.setColumnWidth(3, 250)
        self.table.setColumnWidth(4, 77)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.show()
        winsound.PlaySound("Lobby.wav", winsound.SND_LOOP + winsound.SND_ASYNC)

    def page_changed(self):
        data = self.cur.execute("SELECT * FROM history").fetchall()
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Date&Time"))
        self.table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Item"))
        self.table.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Rarity"))
        self.table.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("Mods"))
        self.table.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem("Total Cost"))
        for i in data:
            rows = self.table.rowCount()
            self.table.setRowCount(rows + 1)
            self.table.setItem(rows, 0, QtWidgets.QTableWidgetItem((i[0])))
            self.table.setItem(rows, 1, QtWidgets.QTableWidgetItem(i[1]))
            self.table.setItem(rows, 2, QtWidgets.QTableWidgetItem(i[2]))
            self.table.setItem(rows, 3, QtWidgets.QTableWidgetItem(i[3]))
            self.table.setItem(rows, 4, QtWidgets.QTableWidgetItem(str(i[4])))

        sum = 0
        data = self.cur.execute("SELECT cost FROM history").fetchall()
        for i in data:
            sum += i[0]

        self.totalcostinfo.setText(f"Заработанная сумма с продажи всех предметов: {sum} золотых")
        self.totalcostinfo.adjustSize()


    def on_historyBut_clicked(self):
        if self.stacked.currentIndex() == 0:
            self.stacked.setCurrentIndex(1)
            self.historyBut.setText("Return")
            self.table.setVisible(True)
            self.totalcostinfo.setVisible(True)
        elif self.stacked.currentIndex() == 1:
            self.stacked.setCurrentIndex(0)
            self.historyBut.setText("Items \n History")
            self.table.setVisible(False)
            self.totalcostinfo.setVisible(False)
        else:
            pass

class HistoryWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dark & Darker Helper")
        self.setWindowIcon(QtGui.QIcon("./icon.jpg"))
        self.setGeometry(100,100, 475, 500)
        self.setFixedSize(570,500)

        self.show()

class MainWindow(QtWidgets.QWidget):
    def __init__(self, login):
        super().__init__()
        self.setWindowTitle("Dark & Darker Helper")
        self.setWindowIcon(QtGui.QIcon("./icon.jpg"))
        self.setGeometry(100,100, 475, 500)
        self.setFixedSize(800,500)

        self.con = sqlite3.connect("DarkAndDarkerItemList.db")
        self.cur = self.con.cursor()

        self.padding = 100

        self.itemIcon = QtWidgets.QLabel(self)
        self.itemIcon.setGeometry(50, 100, 10, 10)

        self.sortByType = QtWidgets.QComboBox(self)
        self.sortByType.setGeometry(190 + self.padding, 70, 200, 22)

        self.sortBySubtype = QtWidgets.QComboBox(self)
        self.sortBySubtype.setGeometry(190 + self.padding,130,200,22)

        self.chooseRarity = QtWidgets.QComboBox(self)
        self.chooseRarity.setGeometry(190 + self.padding, 250, 200, 22)


        self.firstEnchantment = QtWidgets.QComboBox(self)
        self.firstEnchantment.setGeometry(25 + self.padding, 310, 170, 22)

        self.secondEnchantment = QtWidgets.QComboBox(self)
        self.secondEnchantment.setGeometry(200 + self.padding, 310, 170, 22)

        self.thirdEnchantment = QtWidgets.QComboBox(self)
        self.thirdEnchantment.setGeometry(375 + self.padding, 310, 170, 22)

        self.helloUser = QtWidgets.QLabel(self)
        self.helloUser.setGeometry(220 + self.padding, 30, 100, 20)
        self.helloUser.setText("Здравствуй, {0}!".format(login))
        self.helloUser.adjustSize()

        self.calcButton = QtWidgets.QPushButton(self)
        self.calcButton.setGeometry(230 + self.padding, 350, 100, 100)
        self.calcButton.clicked.connect(self.on_calcButton_clicked)
        self.calcButton.setText("Calculate")

        self.firstEnchantment.close()
        self.secondEnchantment.close()
        self.thirdEnchantment.close()

        self.chooseItem = QtWidgets.QComboBox(self)
        self.chooseItem.setGeometry(190 + self.padding,190,200,22)
        self.chooseItem.currentTextChanged.connect(self.on_chooseItem_changed)

        sqlQueryInit = self.cur.execute("SELECT statName FROM stats").fetchall()

        for item in sqlQueryInit:
            self.firstEnchantment.addItem(*item)
            self.secondEnchantment.addItem(*item)
            self.thirdEnchantment.addItem(*item)

        self.sortByType.addItems(["Choose type of an item","Weapon", "Armor"])
        self.sortByType.currentTextChanged.connect(self.on_sortByType_changed)

        self.sortBySubtype.addItem("Choose")
        self.sortBySubtype.currentTextChanged.connect(self.on_sortBySubtype_changed)

        self.chooseItem = QtWidgets.QComboBox(self)
        self.chooseItem.setGeometry(190 + self.padding,190,200,22)
        self.chooseItem.currentTextChanged.connect(self.on_chooseItem_changed)
        self.chooseItem.addItem("Choose")

        self.chooseRarity.addItems(["Choose","Common", "Uncommon", "Rare", "Epic"])
        self.chooseRarity.currentTextChanged.connect(self.on_chooseRarity_changed)

        self.label = QtWidgets.QLabel(self)
        self.label.setText("Стоимость предмета равна: ")
        self.label.setGeometry(210 + self.padding, 460, 100, 100)
        self.label.adjustSize()

        self.calcButton.setEnabled(False)
        self.show()

    def on_sortByType_changed(self, value):
        if value == "Armor":
            for i in range(1, self.sortBySubtype.count()+1):
                self.sortBySubtype.removeItem(1)
            self.sortBySubtype.addItems(["Boots", "Pants"])
        elif value == "Weapon":
            for i in range(1, self.sortBySubtype.count()+1):
                self.sortBySubtype.removeItem(1)
            self.sortBySubtype.addItems(["Axe","Bow","Crossbow","Dagger","Mace", "Magic", "Polearm", "Shield", "Sword"])

    def on_sortBySubtype_changed(self,value):
        if value != "Choose":
            sqlQuery = "SELECT Name FROM " + self.sortByType.currentText() +  " WHERE Type = ?"
            for i in range(1, self.chooseItem.count()+1):
                self.chooseItem.removeItem(1)
            for item in self.cur.execute(sqlQuery,([value])).fetchall():
                self.chooseItem.addItem(*item)
        else:
            for i in range(1, self.chooseItem.count()+1):
                self.chooseItem.removeItem(1)

    def switchCalcButton(self):
        if self.chooseItem.currentText() != "Choose" and self.chooseRarity.currentText() != "Choose":
            self.calcButton.setEnabled(True)
        else:
            self.calcButton.setEnabled(False)

    def on_chooseItem_changed(self):
        self.switchCalcButton()
        if self.chooseItem.currentText() != "Choose":
            self.itemIcon.setVisible(True)
            icon = self.cur.execute("SELECT image FROM " + self.sortByType.currentText() + " WHERE Name = ?",(self.chooseItem.currentText(),)).fetchone()
            if icon is not None:
                im = Image.open(io.BytesIO(icon[0]))
                imageIcon = QtGui.QImage(im.toqimage())
                self.itemIcon.setPixmap(QtGui.QPixmap(imageIcon))
                self.itemIcon.adjustSize()
        else:
            self.itemIcon.setVisible(False)




    def on_chooseRarity_changed(self, value):
        self.switchCalcButton()
        if value == "Uncommon":
            self.secondEnchantment.setCurrentIndex(0)
            self.thirdEnchantment.setCurrentIndex(0)
            self.firstEnchantment.setVisible(True)
            self.secondEnchantment.setVisible(False)
            self.thirdEnchantment.setVisible(False)
        elif value == "Rare":
            self.thirdEnchantment.setCurrentIndex(0)
            self.firstEnchantment.setVisible(True)
            self.secondEnchantment.setVisible(True)
            self.thirdEnchantment.setVisible(False)
        elif value == "Epic":
            self.firstEnchantment.setVisible(True)
            self.secondEnchantment.setVisible(True)
            self.thirdEnchantment.setVisible(True)
        else:
            self.firstEnchantment.setCurrentIndex(0)
            self.secondEnchantment.setCurrentIndex(0)
            self.thirdEnchantment.setCurrentIndex(0)
            self.firstEnchantment.setVisible(False)
            self.secondEnchantment.setVisible(False)
            self.thirdEnchantment.setVisible(False)

    def on_calcButton_clicked(self):

        bestClassId = self.cur.execute("SELECT Classes FROM " + self.sortByType.currentText() + " WHERE Name = '" + self.chooseItem.currentText()+"'").fetchone()
        print(bestClassId)

        listClassId = [int(i) for i in bestClassId[0].split(", ")]
        print(listClassId)

        SQLClassQuery = "SELECT ClassPopularity FROM classes WHERE ClassID = ?"
        for i in range(len(listClassId)-1):
            SQLClassQuery += " OR ?"

        classModPrep = max(self.cur.execute(SQLClassQuery, (listClassId)).fetchall())
        classMod = 1.0 + float(classModPrep[0])

        SQLEnchantQuery = "SELECT statValue FROM stats WHERE statName = ?"

        enchantModsPrep = []
        enchantModsPrep.append(self.cur.execute(SQLEnchantQuery, (self.firstEnchantment.currentText(),)).fetchone())
        enchantModsPrep.append(self.cur.execute(SQLEnchantQuery, (self.secondEnchantment.currentText(),)).fetchone())
        enchantModsPrep.append(self.cur.execute(SQLEnchantQuery, (self.thirdEnchantment.currentText(),)).fetchone())

        enchantMods = 0
        for i in enchantModsPrep:
            #print(i)
            enchantMods += i[0]
            #print(enchantMods)

        #print(enchantMods)

        #print(classMod)

        if self.chooseRarity.currentText() == "Epic":
            rarityMod = 150
        elif self.chooseRarity.currentText() == "Rare":
            rarityMod = 70
        elif self.chooseRarity.currentText() == "Uncommon":
            rarityMod = 50
        elif self.chooseRarity.currentText() == "Common":
            rarityMod = 30

        totalCost = math.ceil((enchantMods + rarityMod)*classMod)
        self.label.setText("Стоимость предмета равна: {0} золотых".format(totalCost))
        self.label.adjustSize()

        enchants = ""
        if self.firstEnchantment.currentText() != "NoStat":
            enchants += self.firstEnchantment.currentText() + " "

        if self.secondEnchantment.currentText() != "NoStat":
            enchants += self.secondEnchantment.currentText() + " "

        if self.thirdEnchantment.currentText() != "NoStat":
            enchants += self.thirdEnchantment.currentText() + " "

        self.cur.execute(f"""INSERT INTO history (date_time, item_name, rarity, mods, cost) VALUES ('{datetime.datetime.now()}', '{self.chooseItem.currentText()}', '{self.chooseRarity.currentText()}', '{enchants}', '{totalCost}')""")
        self.con.commit()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = Start()
    sys.exit(app.exec())