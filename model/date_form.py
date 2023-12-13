from datetime import datetime

import pandas as pd
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QWidget, QLabel, QFormLayout, QLineEdit, QPushButton, QMessageBox, QFileDialog
from pandas import DataFrame

from services.exam_call import ExamCall
from utils.common.validation_utils import validate_start_date_and_today, validate_date_end, validate_date


class DateForm(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar el formulario
        self.setWindowTitle("Exam Date Generator App")
        self.setWindowIcon(QIcon('images/files.ico'))
        self.setGeometry(400, 400, 600, 350)
        layout = QFormLayout()
        self.setLayout(layout)

        self.start_date_edit_fist_call = QLineEdit(self)
        self.end_date_edit_fist_call = QLineEdit(self)
        self.start_date_edit_recess = QLineEdit(self)
        self.end_date_edit_recess = QLineEdit(self)

        # FIRST CALL
        self.title_first = QLabel("FECHA DEL PERIODO DE MESAS", self)
        self.title_first.setStyleSheet(
            """font-weight: bold;
               margin: 2px;
               font-size: 20px;
            """
        )
        layout.addWidget(self.title_first)
        layout.addRow(QLabel("Fecha de inicio (dd/mm/yy):"), self.start_date_edit_fist_call)
        self.generate_start_buttom_first = QPushButton("Validar")
        self.generate_start_buttom_first.setFixedSize(60, 20)
        layout.addWidget(self.generate_start_buttom_first)
        self.generate_start_buttom_first.clicked.connect(self.validate_date_one_for_first_period)

        layout.addRow(QLabel("Fecha de fin (dd/mm/yy):"), self.end_date_edit_fist_call)
        self.generate_end_buttom_first = QPushButton("Validar")
        self.generate_end_buttom_first.setFixedSize(60, 20)
        layout.addWidget(self.generate_end_buttom_first)
        self.generate_end_buttom_first.clicked.connect(self.validate_date_two_first_period)

        # RECESO
        self.title_recess = QLabel("RECESO Y FECHAS QUE NO SE RINDEN MATERIAS", self)
        self.title_recess.setStyleSheet(
            """font-weight: bold;
               margin: 2px;
               font-size: 20px;
            """
        )
        layout.addWidget(self.title_recess)
        layout.addRow(QLabel("Fecha de inicio (dd/mm/yy):"), self.start_date_edit_recess)
        self.generate_start_buttom_recess = QPushButton("Validar")
        self.generate_start_buttom_recess.setFixedSize(60, 20)
        layout.addWidget(self.generate_start_buttom_recess)
        self.generate_start_buttom_recess.clicked.connect(self.validate_start_recess)

        layout.addRow(QLabel("Fecha de fin (dd/mm/yy):"), self.end_date_edit_recess)
        self.generate_end_buttom_recess = QPushButton("Validar")
        self.generate_end_buttom_recess.setFixedSize(60, 20)
        layout.addWidget(self.generate_end_buttom_recess)
        self.generate_end_buttom_recess.clicked.connect(self.validate_end_recess)

        self.generate_button = QPushButton("Generar", self)
        layout.addWidget(self.generate_button)
        self.generate_button.clicked.connect(self.generate_period)

    def validate_start_recess(self) -> None:
        start_date = self.start_date_edit_recess.text()
        buttom = self.generate_start_buttom_recess
        try:
            validate_date(start_date)
            icon = QIcon("images/check.png")
            buttom.setIcon(icon)
        except:
            QMessageBox.warning(self, "Error", "Invalid format")

    def validate_end_recess(self) -> None:
        end_date = self.end_date_edit_recess.text()
        buttom = self.generate_end_buttom_recess
        try:
            validate_date(end_date)
            icon = QIcon("images/check.png")
            buttom.setIcon(icon)
        except:
            QMessageBox.warning(self, "Error", "Invalid format")

    def validate_date_one_for_first_period(self) -> bool:
        start_date = self.start_date_edit_fist_call.text()
        buttom = self.generate_start_buttom_first
        try:
            validate_date(start_date)
            if validate_start_date_and_today(start_date):
                icon = QIcon("images/check.png")
                buttom.setIcon(icon)
                return True
            else:
                raise Exception
        except:
            QMessageBox.warning(self, "Error", "Invalid date")

    def validate_date_two_first_period(self) -> bool:
        end_date = self.end_date_edit_fist_call.text()
        start_date = self.start_date_edit_fist_call.text()
        buttom = self.generate_end_buttom_first
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

    def import_excel(self) -> DataFrame | None:
        file_path, _ = QFileDialog.getOpenFileName(self, 'Importar Excel', ".", "Archivos Excel (*.xlsx *.xls)")
        if file_path:
            data = pd.read_excel(file_path)
            return data
        else:
            return None

    def generate_period(self):
        start_date_first_period = self.start_date_edit_fist_call.text()
        end_date_first_period = self.end_date_edit_fist_call.text()
        start_recess_date = "None" if not self.start_date_edit_recess.text() else self.start_date_edit_recess.text()
        end_recess_date = "None" if not self.end_date_edit_recess.text() else self.end_date_edit_recess.text()
        if (((self.validate_date_one_for_first_period()
              and self.validate_date_two_first_period()))):
            df = self.import_excel()
            period = {"start_date_first_period": start_date_first_period,
                      "end_date_first_period": end_date_first_period,
                      "start_recess_date": start_recess_date,
                      "end_recess_date": end_recess_date}
            print(period)

            # ToDo: funcion general mesas aca dentro y descargue un csv o exel con los datos

            # call = ExamCall(df, period)
            # first_year_call = call.create_first_year_call_first_period()
