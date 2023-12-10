from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLabel, QFormLayout, QLineEdit, QPushButton, QMessageBox

from utils.validation_utils import validate_start_date_and_today, validate_date_end, validate_date


class DateForm(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar el formulario
        self.setWindowTitle("Exam Date Generator App")
        self.setWindowIcon(QIcon('images/files.ico'))
        self.setGeometry(400, 400, 600, 350)
        layout = QFormLayout()
        self.setLayout(layout)

        self.start_date_edit = QLineEdit(self)
        self.end_date_edit = QLineEdit(self)

        layout.addRow(QLabel("Fecha de inicio (dd/mm/yy):"), self.start_date_edit)
        self.generate_start_buttom = QPushButton("Validar")
        self.generate_start_buttom.setFixedSize(60, 20)
        layout.addWidget(self.generate_start_buttom)
        self.generate_start_buttom.clicked.connect(self.validate_date_one)

        layout.addRow(QLabel("Fecha de fin (dd/mm/yy):"), self.end_date_edit)
        self.generate_end_buttom = QPushButton("Validar")
        self.generate_end_buttom.setFixedSize(60, 20)
        layout.addWidget(self.generate_end_buttom)
        self.generate_end_buttom.clicked.connect(self.validate_date_two)

        self.generate_button = QPushButton("Generar", self)
        layout.addWidget(self.generate_button)
        self.generate_button.clicked.connect(self.generate_period)

    def validate_date_one(self):
        date = self.start_date_edit.text()
        buttom = self.generate_start_buttom
        try:
            validate_date(date)
            if validate_start_date_and_today(date):
                icon = QIcon("images/check.png")
                buttom.setIcon(icon)
                return True
            else:
                raise Exception
        except:
            QMessageBox.warning(self, "Error", "Invalid date")

    def validate_date_two(self):
        end_date = self.end_date_edit.text()
        start_date = self.start_date_edit.text()
        buttom = self.generate_end_buttom
        try:
            validate_date(end_date)
            if validate_date_end(end_date, start_date):
                icon = QIcon("images/check.png")
                buttom.setIcon(icon)
                return True
            else:
                raise Exception
        except:
            QMessageBox.warning(self, "Error", "Invalid date")

    def generate_period(self):
        start_date = self.start_date_edit.text()
        end_date = self.end_date_edit.text()
        if self.validate_date_one() and self.validate_date_two():
            period = {"start_date": start_date, "end_date": end_date}
            print(period)

