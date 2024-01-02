import os
import sys
from datetime import datetime

import pandas as pd
from pandas import DataFrame
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QWidget,
)

from services.exam_call import ExamCall
from utils.common.validation_utils import (
    validate_date,
    validate_date_end,
    validate_start_date_and_today,
)


class DateForm(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar el formulario
        self.setWindowTitle("Exam Date Generator App")
        self.setWindowIcon(QIcon("images/files.ico"))
        self.setGeometry(400, 400, 600, 350)
        layout = QFormLayout()
        self.setLayout(layout)

        self.start_date_edit_fist_call = QLineEdit(self)
        self.end_date_edit_fist_call = QLineEdit(self)
        self.start_date_edit_second_call = QLineEdit(self)
        self.end_date_edit_second_call = QLineEdit(self)
        self.career_name = QLineEdit()

        # CAREER NAME
        layout.addRow(QLabel("Ingrese el nombre de la carrera:"), self.career_name)

        # FIRST CALL
        self.title_first = QLabel("PRIMER LLAMADO", self)
        self.title_first.setStyleSheet(
            """font-weight: bold;
               margin: 2px;
               font-size: 20px;
            """
        )
        layout.addWidget(self.title_first)
        layout.addRow(
            QLabel("Fecha de inicio (dd/mm/yy):"), self.start_date_edit_fist_call
        )
        self.generate_start_buttom_first = QPushButton("Validar")
        self.generate_start_buttom_first.setFixedSize(60, 20)
        layout.addWidget(self.generate_start_buttom_first)
        self.generate_start_buttom_first.clicked.connect(
            self.validate_date_one_for_first_period
        )

        layout.addRow(QLabel("Fecha de fin (dd/mm/yy):"), self.end_date_edit_fist_call)
        self.generate_end_buttom_first = QPushButton("Validar")
        self.generate_end_buttom_first.setFixedSize(60, 20)
        layout.addWidget(self.generate_end_buttom_first)
        self.generate_end_buttom_first.clicked.connect(
            self.validate_date_two_first_period
        )

        # SECOND CALL
        self.title_second = QLabel("SEGUNDO LLAMADO", self)
        self.title_second.setStyleSheet(
            """font-weight: bold;
               margin: 2px;
               font-size: 20px;
            """
        )
        layout.addWidget(self.title_second)
        layout.addRow(
            QLabel("Fecha de inicio (dd/mm/yy):"), self.start_date_edit_second_call
        )
        self.generate_start_buttom_second = QPushButton("Validar")
        self.generate_start_buttom_second.setFixedSize(60, 20)
        layout.addWidget(self.generate_start_buttom_second)
        self.generate_start_buttom_second.clicked.connect(
            self.validate_date_one_for_second_period
        )

        layout.addRow(
            QLabel("Fecha de fin (dd/mm/yy):"), self.end_date_edit_second_call
        )
        self.generate_end_buttom_second = QPushButton("Validar")
        self.generate_end_buttom_second.setFixedSize(60, 20)
        layout.addWidget(self.generate_end_buttom_second)
        self.generate_end_buttom_second.clicked.connect(
            self.validate_date_two_second_period
        )

        self.generate_button = QPushButton("Generar", self)
        layout.addWidget(self.generate_button)
        self.generate_button.clicked.connect(self.generate_period)

    def validate_date_one_for_second_period(self) -> bool:
        """
        Validate that the date is in the correct format
        :return: bool
        """
        start_date_first = datetime.strptime(
            self.start_date_edit_fist_call.text(), "%d/%m/%y"
        )
        end_date_first = datetime.strptime(
            self.end_date_edit_fist_call.text(), "%d/%m/%y"
        )
        start_date = self.start_date_edit_second_call.text()
        buttom = self.generate_start_buttom_second
        try:
            validate_date(start_date)
            end_date = datetime.strptime(start_date, "%d/%m/%y")
            if end_date > start_date_first and end_date > end_date_first:
                icon = QIcon("images/check.png")
                buttom.setIcon(icon)
                return True
            else:
                raise Exception
        except:
            QMessageBox.warning(self, "Error", "Invalid date")

    def validate_date_two_second_period(self) -> bool:
        """
        Validate that the date is in the correct format
        :return: bool
        """
        end_date = self.end_date_edit_second_call.text()
        start_date = self.start_date_edit_second_call.text()
        buttom = self.generate_end_buttom_second
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

    def validate_date_one_for_first_period(self) -> bool:
        """
        Validate that the date is in the correct format
        :return: bool
        """
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
        """
        Validate that the date is in the correct format
        :return: bool
        """
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
        """
        Import the file and return it as a DataFrame
        :return: DataFrame / None
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Importar Excel", ".", "Archivos Excel (*.xlsx *.xls)"
        )
        if file_path:
            data = pd.read_excel(file_path)
            return data
        else:
            return None

    def generate_period(self) -> None:
        """
        Generate the exam calls and generate the message boxes
        :return: None
        """
        start_date_first_period = self.start_date_edit_fist_call.text()
        end_date_first_period = self.end_date_edit_fist_call.text()
        start_date_second_period = self.start_date_edit_second_call.text()
        end_date_second_period = self.end_date_edit_second_call.text()
        career_name = self.career_name.text()
        if (
            self.validate_date_one_for_first_period()
            and self.validate_date_one_for_second_period()
            and self.validate_date_two_first_period()
            and self.validate_date_two_second_period()
        ):
            df = self.import_excel()
            period = {
                "start_date_first_period": start_date_first_period,
                "end_date_first_period": end_date_first_period,
                "start_date_second_period": start_date_second_period,
                "end_date_second_period": end_date_second_period,
                "career_name": career_name,
            }

            call = ExamCall(df, period)
            try:
                self.get_output(call)
                message_box = QMessageBox()
                message_box.setWindowIcon(QIcon("images/files.ico"))
                message_box.setText("Mesas generadas con exito")
                message_box.accept()
                message_box.exec()
            except:
                QMessageBox.setWindowIcon(QIcon("images/files.ico"))
                QMessageBox.warning(self, "Error", "Error generando mesas")
            finally:
                sys.exit()

    def get_output(self, call: ExamCall) -> None:
        """
        Convert Dataframes to Excel and export it to a folder on Desktop
        :param call: ExamCall
        :return:
        """
        path_desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

        os.makedirs(f"{path_desktop}/mesas", exist_ok=True)

        call.create_second_call()
        call.first_year_result.to_excel(f"{path_desktop}/mesas/mesas_primer_año.xlsx")
        call.second_year_result.to_excel(f"{path_desktop}/mesas/mesas_segundo_año.xlsx")
        call.third_year_result.to_excel(f"{path_desktop}/mesas/mesas_tercer_año.xlsx")
        call.fourth_year_result.to_excel(f"{path_desktop}/mesas/mesas_cuarto_año.xlsx")
        call.fifth_year_result.to_excel(f"{path_desktop}/mesas/mesas_quinto_año.xlsx")
