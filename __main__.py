from pathlib import Path
import sys

from pypdf import PdfReader, PdfWriter, errors
from PyQt6.QtWidgets import QApplication, QMainWindow,QFileDialog, QMessageBox
from interface import Ui_MainWindow

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        # Load the UI file
        self.setupUi(self)
        
        self.browse.clicked.connect(self.browse_file)
        self.encrypt.clicked.connect(self.encrypt_pdf)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            self.filepath.setText(file_path)
    
    def encrypt_pdf(self):
        path = Path(self.filepath.text())
        reader = PdfReader(path)
        writer = PdfWriter()

        try:
            writer.append_pages_from_reader(reader)
            if not self.password.text():
                raise ValueError("Password cannot be empty.")
            writer.encrypt(self.password.text())
            with open(path.with_stem(path.stem + "_encrypted"), "wb") as out_file:
                writer.write(out_file)
            QMessageBox.information(self, "Success", "File encrypted successfully!")
        
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except errors.FileNotDecryptedError:
            QMessageBox.warning(self, "Error", "File already encrypted!")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())