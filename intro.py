import os
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import ( QApplication, QFileDialog, QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget )

from file_handler import get_tournament_name_from_workbook, load_file_gironi
from hud import ExitButton

if TYPE_CHECKING:
    from offline_uwufufu_like import AppController

class IntroScreen(QWidget):
    def __init__(self, controller: "AppController") -> None:
        super().__init__()
        self.controller = controller
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.setWindowTitle("Benvenuto")

        layout = QVBoxLayout()

        # Layout orizzontale per il bottone exit in alto a destra
        top_layout = QHBoxLayout()
        top_layout.addStretch()           # spinge il bottone a destra
        exit_btn = ExitButton(self, self.exit_window)
        top_layout.addWidget(exit_btn)
        layout.addLayout(top_layout)  # aggiunge il layout orizzontale in cima

        label = QLabel("Benvenuto nel torneo!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"font-size: {self.width() // 10}px; font-weight: bold;")
        layout.addWidget(label)

        label_spiegazione = QLabel((
                                "- Carica il file con i gironi (il file caricato non verrà modificato)\n"
                                "- Puoi scegliere tramite i tasti posti sopra o tramite i tasti A e D\n"
                                "- Puoi smettere in qualsiasi momento, i progressi verranno salvati e alla riapertura ricomincerai da dove hai interrotto!\n"
                                ))
        label_spiegazione.setWordWrap(True)
        label_spiegazione.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label_spiegazione.setStyleSheet(f"font-size: {self.width() // 14}px;")
        layout.addWidget(label_spiegazione, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_load_file = QPushButton("Carica file gironi")
        self.btn_load_file.setFixedSize( (self.width()*10) // 15, self.height() // 3)
        self.btn_load_file.setStyleSheet(f"font-size: {self.width() // 14}px;")
        self.btn_load_file.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.btn_load_file, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def exit_window(self) -> None:
        QApplication.instance().quit()

    def open_file_dialog(self) -> None:
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Excel files (*.xlsx)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                filepath = selected_files[0]
                workbook_name = os.path.splitext(os.path.basename(filepath))[0]
                self.controller.filename = get_tournament_name_from_workbook(workbook_name)
                self.controller.state_filename = workbook_name
                gironi = load_file_gironi(filepath)
                if gironi is None:
                    QMessageBox.warning(self, "Errore", "Nessun girone trovato o file vuoto.")
                    return
                self.controller.show_tournament(gironi)
                self.close()

    def __del__(self):
        print("Intro distrutta dal GC!")
