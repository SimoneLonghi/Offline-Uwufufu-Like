from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from girone import Girone
from file_handler import ( Participant, TournamentData, Winner, get_stato_path, load_stato, save_stato,save_vincitori )

if TYPE_CHECKING:
    from offline_uwufufu_like import AppController


class Tournament(QWidget):
    def __init__(self, controller: "AppController", tournament_data: TournamentData) -> None:
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.controller = controller
        self.gironi = tournament_data["groups"]
        self.round = tournament_data["round_name"]
        self.gironi_keys = sorted(self.gironi)
        self.current_girone_index = 0
        self.vincitori: list[Winner] = []

        load_stato(self)

        self.setWindowTitle("Torneo con più Gironi")
        #self.setStyleSheet("background: red;")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        girone_num = self.gironi_keys[self.current_girone_index]
        self.current_girone = Girone(self.gironi[girone_num], self, girone_num)
        
        self.main_layout.addWidget(self.current_girone)
        self.current_girone.show()
        
        self.start_next_girone()

    def start_next_girone(self) -> None:
        if self.current_girone_index >= len(self.gironi_keys):
            self.current_girone.deleteLater()
            self.current_girone = None 
            self.start_next_tournament()
            return

        girone_num = self.gironi_keys[self.current_girone_index]
        self.current_girone.load_next_girone(self.gironi[girone_num], girone_num)

    def girone_finished(self, vincitore: Participant) -> None:
        self.vincitori.append((self.gironi_keys[self.current_girone_index], vincitore))

        self.current_girone_index += 1
        save_stato(self)
        self.start_next_girone()

    def clear_saved_state(self) -> None:
        path = get_stato_path(self.controller.state_filename)
        if path.exists():
            try:
                path.unlink()
            except OSError as e:
                print(f"Errore eliminando {path}: {e}")

    def start_next_tournament(self) -> None:
        file_vincitori = save_vincitori(self)
        self.clear_saved_state()
        vincitore = self.vincitori[0][1][0] if len(self.vincitori) == 1 else None
        self.controller.load_next_tournament(file_vincitori, vincitore)
        
    def save_state_and_exit(self) -> None:
        save_stato(self)
        QApplication.instance().quit()

    def __del__(self):
        print("Torneo distrutto dal GC!")
