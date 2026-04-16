from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QSizePolicy
import sys
from PyQt6.QtCore import Qt

from cluster import VM, Rack

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CVMPS")
        self.setStyleSheet("background-color: lightblue;")
        self.resize(800,800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
                border: 2px solid #ffffff;
            }
        """
        start_btn = QPushButton (f"Start Builder")
        start_btn.setMinimumSize(150,40)
        start_btn.setMaximumSize(300,60)
        start_btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
        )
        start_btn.setStyleSheet(button_style)
        start_btn.clicked.connect(self.button_clicked)
        layout.addWidget(start_btn,alignment=Qt.AlignmentFlag.AlignCenter)

        continue_btn = QPushButton (f"Continue Build")
        continue_btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
        )
        continue_btn.setStyleSheet(button_style)
        continue_btn.clicked.connect(self.button_clicked)
        continue_btn.setMinimumSize(150,40)
        continue_btn.setMaximumSize(300,60)
        layout.addWidget(continue_btn,alignment=Qt.AlignmentFlag.AlignCenter)

        load_btn = QPushButton (f"Load Build")
        load_btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
        )
        load_btn.setStyleSheet(button_style)
        load_btn.clicked.connect(self.button_clicked)
        load_btn.setMinimumSize(150,40)
        load_btn.setMaximumSize(300,60)
        layout.addWidget(load_btn,alignment=Qt.AlignmentFlag.AlignCenter)

        options_btn = QPushButton (f"Options")
        options_btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
        )
        options_btn.setStyleSheet(button_style)
        options_btn.clicked.connect(self.button_clicked)
        options_btn.setMinimumSize(150,40)
        options_btn.setMaximumSize(300,60)
        layout.addWidget(options_btn,alignment=Qt.AlignmentFlag.AlignCenter)

        quit_btn = QPushButton (f"Quit")
        quit_btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
        )
        quit_btn.setStyleSheet(button_style)
        quit_btn.clicked.connect(self.button_clicked)
        quit_btn.setMinimumSize(150,40)
        quit_btn.setMaximumSize(300,60)
        layout.addWidget(quit_btn,alignment=Qt.AlignmentFlag.AlignCenter)
    def button_clicked(self):
        print("You clicked!")


def main():
   # app = QApplication(sys.argv)
   # window = MainWindow()
   # window.show()
   # sys.exit(app.exec())
   test_1 = VM("test_1","wowo","critical",0.8,0.7,0.9,10,100000,0.8)
   print(test_1)
if __name__ == "__main__":
    main()
