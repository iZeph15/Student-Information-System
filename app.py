#Author: Van Zeus Gagarin

import sys
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate, QTime, Qt

class StudentForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Information System")

        self.setStyleSheet("""
            QWidget {
                background-color: #F0F0F0;
                font-size: 14px;
            }
            
            QLabel {
                font-weight: bold;
            }
            
            QLineEdit {
                padding: 6px;
                border: 1px solid #AAA;
                border-radius: 4px;
                background-color: #FFF;
            }
            
            QPushButton {
                padding: 8px;
                border-radius: 4px;
                background-color: #007BFF;
                color: #FFF;
            }
            
            QTextEdit {
                padding: 6px;
                border: 1px solid #AAA;
                border-radius: 4px;
                background-color: #FFF;
            }
        """)

        self.last_name_label = QLabel("Last Name:")
        self.last_name_input = QLineEdit()

        self.first_name_label = QLabel("First Name:")
        self.first_name_input = QLineEdit()

        self.middle_initial_label = QLabel("Middle Initial:")
        self.middle_initial_input = QLineEdit()

        self.id_label = QLabel("ID:")
        self.id_input = QLineEdit()

        self.age_label = QLabel("Age:")
        self.age_input = QLineEdit()

        self.address_label = QLabel("Address:")
        self.address_input = QLineEdit()

        self.course_label = QLabel("Course:")
        self.course_input = QLineEdit()

        self.submit_button = QPushButton("Submit")
        self.submit_button.setIcon(QIcon("submit_icon.png"))
        self.submit_button.clicked.connect(self.submit)

        self.view_button = QPushButton("View Data")
        self.view_button.setIcon(QIcon("view_icon.png"))
        self.view_button.clicked.connect(self.view_data)

        self.clear_button = QPushButton("Clear Data")
        self.clear_button.setIcon(QIcon("clear_icon.png"))
        self.clear_button.clicked.connect(self.clear_data)

        layout = QVBoxLayout()
        layout.addWidget(self.last_name_label)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.first_name_label)
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.middle_initial_label)
        layout.addWidget(self.middle_initial_input)
        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)
        layout.addWidget(self.address_label)
        layout.addWidget(self.address_input)
        layout.addWidget(self.course_label)
        layout.addWidget(self.course_input)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.view_button)
        layout.addWidget(self.clear_button)

        self.setLayout(layout)
        self.view_window = None

    def submit(self):
        last_name = self.last_name_input.text()
        first_name = self.first_name_input.text()
        middle_initial = self.middle_initial_input.text()
        student_id = self.id_input.text()
        age = self.age_input.text()
        address = self.address_input.text()
        course = self.course_input.text()

        if not self.is_valid_name(first_name):
            QMessageBox.warning(self, "Invalid First Name", "First name should not contain numbers.")
            return

        if not self.is_valid_name(middle_initial):
            QMessageBox.warning(self, "Invalid Middle Initial", "Middle initial should not contain numbers.")
            return

        if not self.is_valid_name(last_name):
            QMessageBox.warning(self, "Invalid Last Name", "Last name should not contain numbers.")
            return

        if not age.isdigit() or len(age) != 2:
            QMessageBox.warning(self, "Invalid Age", "Age must be a two-digit number.")
            return

        student_data = [last_name, first_name, middle_initial, student_id, age, address, course]

        headers = ["Last Name", "First Name", "Middle Initial", "ID", "Age", "Address", "Course", "Date Added", "Time Added"]

        date_added = QDate.currentDate().toString(Qt.ISODate)
        time_added = QTime.currentTime().toString(Qt.DefaultLocaleLongDate)

        student_data.extend([date_added, time_added])

        with open('students.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter='|')
            if csvfile.tell() == 0:
                writer.writerow(headers)
            writer.writerow(student_data)

        self.clear_inputs()

        QMessageBox.information(self, "Success", "Successfully Submitted")

    def is_valid_name(self, name):
        return not any(char.isdigit() for char in name)

    def view_data(self):
        headers = ["Last Name", "First Name", "Middle Initial", "ID", "Age", "Address", "Course", "Date Added", "Time Added"]

        with open('students.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            data = list(reader)

        if not self.view_window:
            self.view_window = QWidget()
            self.view_window.setWindowTitle("Student Data")
            self.view_window.setStyleSheet("""
                background-color: #F0F0F0;
                border-radius: 10px;
                padding: 10px;
            """)

            table = QTableWidget()
            table.setColumnCount(len(headers))
            table.setRowCount(len(data))
            table.setHorizontalHeaderLabels(headers)

            for i, row in enumerate(data):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(col)
                    table.setItem(i, j, item)

            layout = QVBoxLayout()
            layout.addWidget(table)
            self.view_window.setLayout(layout)

        else:
            table = self.view_window.layout().itemAt(0).widget()
            table.clearContents()
            table.setRowCount(len(data))
            table.setHorizontalHeaderLabels(headers)

            for i, row in enumerate(data):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(col)
                    table.setItem(i, j, item)

        self.view_window.resize(700, 300)
        self.view_window.show()

    def clear_inputs(self):
        self.last_name_input.clear()
        self.first_name_input.clear()
        self.middle_initial_input.clear()
        self.id_input.clear()
        self.age_input.clear()
        self.address_input.clear()
        self.course_input.clear()

    def clear_data(self):
        confirm = QMessageBox.question(self, "Confirmation", "Are you sure you want to clear all data?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            with open('students.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csvfile.write('')
            QMessageBox.information(self, "Success", "Data cleared successfully.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = StudentForm()
    form.resize(700, 300)
    form.show()
    sys.exit(app.exec_())
