import sys
import re
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt
from ui import Ui_mainWindow
from json import load, dump


class JsonManger(QtWidgets.QMainWindow):
    def __init__(self):
        super(JsonManger, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        cs_group = QtWidgets.QButtonGroup(self)
        cs_group.addButton(self.ui.radioButton)
        cs_group.addButton(self.ui.radioButton_2)

        self.setWindowTitle("JSON Manger")
        self.set_header()
        self.ui.pushButton_4.clicked.connect(self.load_data_from_file)
        self.ui.comboBox.activated.connect(self.person_selected)
        self.ui.pushButton_2.clicked.connect(self.save_data)
        self.ui.pushButton_3.clicked.connect(self.delete_person)
        self.ui.pushButton.clicked.connect(self.add_new_person)
        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
        self.setFixedSize(self.size())

    def set_header(self):
        header = self.ui.tableWidget.horizontalHeader()
        dict_keys = ["name", "birthday", "height", "weight", "car", "languages"]

        self.ui.tableWidget.setColumnCount(len(dict_keys))
        self.ui.tableWidget.setHorizontalHeaderLabels(dict_keys)

    def load_data_from_file(self):
        data = QFileDialog.getOpenFileName(self, "Open file", "./")

        with open(data[0], "r") as f:
            data = load(f)

        self.ui.tableWidget.setRowCount(len(data))
        self.ui.tableWidget.setColumnCount(len(data[0]))

        # self.ui.tableWidget.setHorizontalHeaderLabels(data[0].keys())

        for i in range(len(data)):
            counter = 0
            for j in data[i].keys():
                if j == "languages":
                    self.ui.tableWidget.setItem(
                        i, counter, QtWidgets.QTableWidgetItem(", ".join(data[i][j]))
                    )
                else:
                    self.ui.tableWidget.setItem(
                        i, counter, QtWidgets.QTableWidgetItem(str(data[i][j]))
                    )

                counter += 1

            self.ui.comboBox.addItem(data[i]["name"])

        self.fill_data(self.ui.comboBox.currentIndex())

    def save_to_json(self):
        data = []

        for i in range(self.ui.tableWidget.rowCount()):
            row = {}
            for j in range(self.ui.tableWidget.columnCount()):
                if self.ui.tableWidget.item(i, j).text().isdigit():
                    row[self.ui.tableWidget.horizontalHeaderItem(j).text()] = int(
                        self.ui.tableWidget.item(i, j).text()
                    )
                elif re.match(
                    r"^-?\d+(?:\.\d+)$", self.ui.tableWidget.item(i, j).text()
                ):
                    row[self.ui.tableWidget.horizontalHeaderItem(j).text()] = float(
                        self.ui.tableWidget.item(i, j).text()
                    )
                elif self.ui.tableWidget.horizontalHeaderItem(j).text() == "languages":
                    row[self.ui.tableWidget.horizontalHeaderItem(j).text()] = (
                        self.ui.tableWidget.item(i, j).text().split(", ")
                    )
                elif self.ui.tableWidget.item(i, j).text() == "True":
                    row[self.ui.tableWidget.horizontalHeaderItem(j).text()] = True

                elif self.ui.tableWidget.item(i, j).text() == "False":
                    row[self.ui.tableWidget.horizontalHeaderItem(j).text()] = False

                else:
                    row[
                        self.ui.tableWidget.horizontalHeaderItem(j).text()
                    ] = self.ui.tableWidget.item(i, j).text()

            data.append(row)

        with open("data.json", "w") as f:
            dump(data, f)

        return data

    def find_person(self):
        name = self.ui.comboBox.currentText()

        matching_items = self.ui.tableWidget.findItems(name, Qt.MatchFlag.MatchExactly)

        for item in matching_items:
            self.ui.tableWidget.selectRow(item.row())

        if matching_items:
            item = matching_items[0]
            self.ui.tableWidget.setCurrentItem(item)

            return item.row()

    def clear_checkboxes(self):
        self.ui.checkBox.setChecked(False)
        self.ui.checkBox_2.setChecked(False)
        self.ui.checkBox_3.setChecked(False)
        self.ui.checkBox_4.setChecked(False)

    def fill_data(self, selected_person=None):
        self.ui.lineEdit.setText(self.ui.comboBox.currentText())

        qdate = QtCore.QDate.fromString(
            self.ui.tableWidget.item(selected_person, 1).text(), "dd.MM.yyyy"
        )

        self.ui.dateEdit.setDate(qdate)

        self.ui.lineEdit_2.setText(self.ui.tableWidget.item(selected_person, 2).text())
        self.ui.lineEdit_3.setText(self.ui.tableWidget.item(selected_person, 3).text())

        if self.ui.tableWidget.item(selected_person, 4).text() == "True":
            self.ui.radioButton.setChecked(True)
        else:
            self.ui.radioButton_2.setChecked(True)

        languages = self.ui.tableWidget.item(selected_person, 5).text().split(", ")

        for i in languages:
            if i == "Python":
                self.ui.checkBox.setChecked(True)
            elif i == "C++":
                self.ui.checkBox_2.setChecked(True)
            elif i == "GoLang":
                self.ui.checkBox_3.setChecked(True)
            elif i == "Solidity":
                self.ui.checkBox_4.setChecked(True)

    def person_selected(self):
        selected_person = self.find_person()
        self.clear_checkboxes()
        self.fill_data(selected_person)

    def check_for_empty_fields(self):
        if self.ui.lineEdit.text() == "":
            return True
        elif self.ui.lineEdit_2.text() == "":
            return True
        elif self.ui.lineEdit_3.text() == "":
            return True
        elif self.ui.dateEdit.text() == "":
            return True
        else:
            return False

    def save_data(self):
        if self.check_for_empty_fields():
            return

        index = self.ui.comboBox.currentIndex()

        self.ui.tableWidget.item(index, 0).setText(self.ui.lineEdit.text())
        self.ui.tableWidget.item(index, 1).setText(
            ".".join(self.ui.dateEdit.text().split("/"))
        )
        self.ui.tableWidget.item(index, 2).setText(self.ui.lineEdit_2.text())
        self.ui.tableWidget.item(index, 3).setText(self.ui.lineEdit_3.text())

        if self.ui.radioButton.isChecked():
            self.ui.tableWidget.item(index, 4).setText("True")
        else:
            self.ui.tableWidget.item(index, 4).setText("False")

        languages = []
        if self.ui.checkBox.isChecked():
            languages.append("Python")
        if self.ui.checkBox_2.isChecked():
            languages.append("C++")
        if self.ui.checkBox_3.isChecked():
            languages.append("GoLang")
        if self.ui.checkBox_4.isChecked():
            languages.append("Solidity")

        self.ui.tableWidget.item(index, 5).setText(", ".join(languages))

        self.ui.comboBox.insertItem(index, self.ui.lineEdit.text())
        self.ui.comboBox.setCurrentIndex(index)
        self.ui.comboBox.removeItem(index + 1)
        self.save_to_json()

    def clear_fields(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()

        self.ui.checkBox.setChecked(False)
        self.ui.checkBox_2.setChecked(False)
        self.ui.checkBox_3.setChecked(False)
        self.ui.checkBox_4.setChecked(False)

        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())

        self.ui.radioButton.setChecked(False)
        self.ui.radioButton_2.setChecked(False)

    def delete_person(self):
        if self.ui.comboBox.currentIndex() == -1:
            self.clear_fields()
            return

        selected_person = self.find_person()

        self.ui.tableWidget.removeRow(selected_person)
        self.ui.comboBox.removeItem(selected_person)

        self.clear_checkboxes()
        self.save_to_json()

        if self.ui.comboBox.count() > 0:
            self.fill_data(self.ui.comboBox.currentIndex())
        else:
            self.clear_fields()
            return

    def add_new_person(self):
        if self.check_for_empty_fields():
            return
        if self.ui.comboBox.findText(self.ui.lineEdit.text()) != -1:
            return

        data = []

        data.append(self.ui.lineEdit.text())
        data.append(".".join(self.ui.dateEdit.text().split("/")))
        data.append(self.ui.lineEdit_2.text())
        data.append(self.ui.lineEdit_3.text())

        if self.ui.radioButton.isChecked():
            data.append("True")
        else:
            data.append("False")

        languages = []

        if self.ui.checkBox.isChecked():
            languages.append("Python")
        if self.ui.checkBox_2.isChecked():
            languages.append("C++")
        if self.ui.checkBox_3.isChecked():
            languages.append("GoLang")
        if self.ui.checkBox_4.isChecked():
            languages.append("Solidity")

        data.append(", ".join(languages))

        self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
        self.ui.tableWidget.setItem(
            self.ui.tableWidget.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(data[0])
        )
        self.ui.tableWidget.setItem(
            self.ui.tableWidget.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(data[1])
        )
        self.ui.tableWidget.setItem(
            self.ui.tableWidget.rowCount() - 1, 2, QtWidgets.QTableWidgetItem(data[2])
        )
        self.ui.tableWidget.setItem(
            self.ui.tableWidget.rowCount() - 1, 3, QtWidgets.QTableWidgetItem(data[3])
        )
        self.ui.tableWidget.setItem(
            self.ui.tableWidget.rowCount() - 1, 4, QtWidgets.QTableWidgetItem(data[4])
        )
        self.ui.tableWidget.setItem(
            self.ui.tableWidget.rowCount() - 1, 5, QtWidgets.QTableWidgetItem(data[5])
        )
        self.ui.comboBox.insertItem(self.ui.comboBox.count(), data[0])
        self.ui.comboBox.setCurrentIndex(self.ui.comboBox.count() - 1)

        self.save_to_json()

        print(data)


app = QtWidgets.QApplication([])
application = JsonManger()
application.show()

sys.exit(app.exec())
