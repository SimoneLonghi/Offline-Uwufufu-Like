# python -m PyInstaller --noconsole --onefile offline_uwufufu_like.py

import sys
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import QApplication, QMessageBox, QWidget

from intro import IntroScreen
from tournament import Tournament
from outro import OutroScreen
from file_handler import ( TournamentData, get_tournament_name_from_workbook, load_file_gironi_by_name )


class AppController:
    def __init__(self) -> None:
        self.current_window: Optional[QWidget] = None
        self.filename: str = ""
        self.state_filename: str = ""

    def show_intro(self) -> None:
        self.current_window = IntroScreen(self)
        self.current_window.showFullScreen()

    def show_tournament(self, tournament_data: TournamentData) -> None:
        #self.close_current_window()
        self.current_window = Tournament(self, tournament_data)
        self.current_window.showFullScreen()

    def show_outro(self, winner_name: str) -> None:
        self.close_current_window()
        self.current_window = OutroScreen(winner_name)
        self.current_window.showFullScreen()

    def load_next_tournament( self, next_tournament_round: str, winner_name: Optional[str] = None ) -> None:
        if next_tournament_round.startswith("VINCITORE"):
            if winner_name is None:
                raise ValueError("Il nome del vincitore finale non è stato fornito")
            self.show_outro(winner_name)
        else:
            tournament_data = load_file_gironi_by_name(next_tournament_round)
            if tournament_data is None:
                QMessageBox.warning( self.current_window, "Errore", f"Impossibile caricare il turno {next_tournament_round}." )
                return

            self.close_current_window()
            workbook_name = Path(next_tournament_round).stem
            self.filename = get_tournament_name_from_workbook(workbook_name)
            self.state_filename = workbook_name

            self.current_window = Tournament(self, tournament_data)
            self.current_window.showFullScreen()

    def close_current_window(self) -> None:
        if self.current_window is not None:
            self.current_window.close()
            self.current_window = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # e.g. 'windows11', 'windowsvista', 'Windows', 'Fusion'

    controller = AppController()
    controller.show_intro()
    
    sys.exit(app.exec())
