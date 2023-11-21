import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Updatawidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.status_bar = self.statusBar()
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.update_action)
        self.label = [self.label_3, self.label_4, self.label_5, self.label_6, self.label_7, self.label_8]
        self.lineEdit_list_name = [self.lineEdit, self.lineEdit_4, self.lineEdit_2, self.lineEdit_5,
                                   self.lineEdit_6, self.lineEdit_7, self.lineEdit_3]
        self.select_data()
        self.update_action()

    def select_data(self):
        name_table = ['ID', 'название сорта', 'степень обжарки',
                      'молотый/в зернах', 'описание вкуса', 'цена', 'объём']
        for i in range(len(self.label)):
            self.label[i].setText(name_table[i + 1])

    def delete(self):
        self.connection.cursor().execute(f"DELETE from coffee where ID = {int(self.lineEdit.text())}").fetchall()

    def add(self):
        try:
            self.connection.cursor().execute(
                f"""INSERT INTO coffee('sort', 'degree_of_roasting', 'ground_in_grains', 'taste_description', 
                'price', 'volume') VALUES('{self.lineEdit_4.text()}', '{self.lineEdit_2.text()}',
                 '{self.lineEdit_5.text()}', '{self.lineEdit_6.text()}', {float(self.lineEdit_7.text())},
                  {float(self.lineEdit_3.text())})""").fetchall()
        except ValueError:
            pass

    def change(self):
        self.connection.cursor().execute(
            f"""UPDATE coffee SET sort = '{self.lineEdit_4.text()}', 
            degree_of_roasting = '{self.lineEdit_2.text()}',
            ground_in_grains = '{self.lineEdit_5.text()}', taste_description = '{self.lineEdit_6.text()}', 
            price = {float(self.lineEdit_7.text())}, volume = {float(self.lineEdit_3.text())}
            WHERE ID = {int(self.lineEdit.text())}""").fetchall()

    def update_action(self):
        self.status_bar.showMessage('')
        self.pushButton.setText(self.comboBox.currentText())
        for elem in self.lineEdit_list_name:
            elem.setEnabled(True)
        if self.comboBox.currentIndex() == 0:
            self.lineEdit.setEnabled(False)
        elif self.comboBox.currentIndex() == 1:
            try:
                res = list(self.connection.cursor().execute(
                    f"""SELECT * FROM coffee WHERE id = {int(self.lineEdit.text())}"""))
                if not res:
                    raise ValueError
                for i in range(len(res[0])):
                    self.lineEdit_list_name[i].setText(str(res[0][i]))
            except ValueError:
                self.status_bar.showMessage('Неправильный ввод')
        elif self.comboBox.currentIndex() == 2:
            for elem in self.lineEdit_list_name[1:]:
                elem.setEnabled(False)

    def start(self):
        if self.comboBox.currentIndex() == 0:
            self.add()
        elif self.comboBox.currentIndex() == 1:
            self.change()
        else:
            self.delete()
        self.connection.commit()
        self.connection.close()
        self.close()