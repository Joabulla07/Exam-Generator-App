import sys
from PySide6.QtWidgets import QApplication

from model.DateForm import DateForm


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = DateForm()
    form.show()
    sys.exit(app.exec())
