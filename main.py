import sys
from datetime import datetime
from PySide6 import QtWidgets
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QFormLayout, QLineEdit, QPushButton, QMessageBox


class DateForm(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar el formulario
        self.setWindowTitle("Ingresar periodo de fechas")
        self.setGeometry(100, 100, 400, 150)
        layout = QFormLayout()
        self.setLayout(layout)

        # Crear los campos de fecha de inicio y fecha de fin
        self.start_date_edit = QLineEdit(self)
        self.end_date_edit = QLineEdit(self)

        layout.addRow(QLabel("Fecha de inicio (dd/mm/yy):"), self.start_date_edit)
        self.generate_start_buttom = QPushButton("Validar")
        self.generate_start_buttom.setFixedSize(60, 20)  # Ajustar tamaño
        layout.addWidget(self.generate_start_buttom)
        self.generate_start_buttom.clicked.connect(self.validate_date_one)

        layout.addRow(QLabel("Fecha de fin (dd/mm/yy):"), self.end_date_edit)
        self.generate_end_buttom = QPushButton("Validar")
        self.generate_end_buttom.setFixedSize(60, 20)  # Ajustar tamaño
        layout.addWidget(self.generate_end_buttom)
        self.generate_end_buttom.clicked.connect(self.validate_date_two)

        # Crear el botón "Generar"
        self.generate_button = QPushButton("Generar", self)
        layout.addWidget(self.generate_button)
        self.generate_button.clicked.connect(self.generate_period)

    def validation(self, date, buttom):
        icon = QIcon("images/check.png")
        try:
            datetime.strptime(date, '%d/%m/%y')
            buttom.setIcon(icon)
        except Exception as e:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('No seas soquete!! intente nuevamente con el formato dd/mm/yy')
            print(str(e))
            error_dialog.exec()

    def validate_date_one(self):
        date = self.start_date_edit.text()
        buttom = self.generate_start_buttom
        self.validation(date, buttom)

    def validate_date_two(self):
        date = self.end_date_edit.text()
        buttom = self.generate_end_buttom
        self.validation(date, buttom)

    def generate_period(self):
        start_date = self.start_date_edit.text()
        end_date = self.end_date_edit.text()
        period = {"start_date": start_date, "end_date": end_date}
        print(period)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = DateForm()
    form.show()
    sys.exit(app.exec())
