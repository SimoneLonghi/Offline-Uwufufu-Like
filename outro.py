from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class OutroScreen(QWidget):
    def __init__(self, winner_name: str) -> None:
        super().__init__()
        self.winner_name = winner_name
        self.setWindowTitle("Torneo")

        layout = QVBoxLayout(self)
        title = QLabel("Vincitore del torneo")
        title.setStyleSheet(f"font-size: {self.width() // 10}px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        winner_label = QLabel(self.winner_name)
        winner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        winner_label.setStyleSheet(f"font-size: {self.width() // 14}px;")
        layout.addWidget(winner_label, alignment=Qt.AlignmentFlag.AlignCenter)

        close_button = QPushButton("Chiudi")
        close_button.setFixedSize(self.width() // 2, self.height() // 4)
        close_button.setStyleSheet(f"font-size: {self.width() // 14}px;")
        close_button.clicked.connect(lambda: QApplication.instance().quit())
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)
