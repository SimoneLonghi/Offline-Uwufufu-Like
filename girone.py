from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import QUrl, Qt

from hud import set_hud, SetContainer
from file_handler import Participant

if TYPE_CHECKING:
    from tournament import Tournament

class Girone(QWidget):
    def __init__( self, partecipanti: list[Participant], parent_torneo: "Tournament", girone_num: int ) -> None:
        super().__init__()
        self.partecipanti = partecipanti[:]
        self.parent_torneo = parent_torneo
        self.girone_num = girone_num
        self.index = 1
        self.current_champion: Participant = partecipanti[0]

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.left_container = SetContainer()
        self.layout.addWidget(self.left_container)

        self.right_container = SetContainer()
        self.layout.addWidget(self.right_container)

        self.loser_container = self.left_container

        set_hud(self)

        self.loser_url = QUrl()

        #self.load_current_match()

    def load_next_girone(self, partecipanti: list[Participant], girone_num: int) -> None:
        self.partecipanti = partecipanti[:]
        self.girone_num = girone_num
        self.index = 1
        self.current_champion = partecipanti[0]
        self.loser_container = self.left_container
        self.gironeLabel.setText(f"GIRONE {self.girone_num}")
        self.gironeLabel.adjustSize()
        self.load_current_match()

    def load_current_match(self) -> None:
        if self.index >= len(self.partecipanti):
            self.parent_torneo.girone_finished(self.current_champion)
            return
        
        self.match_counter.setText(f"{self.index} di {len(self.partecipanti) - 1}")
        
        if self.index == 1:
            #self.right_url.setUrl(self.current_champion[1])
            self.right_container.view.load(QUrl(self.current_champion[1]))
            self.right_container.player = self.current_champion

        challenger = self.partecipanti[self.index]
        self.loser_url.setUrl(challenger[1])
        self.loser_container.view.load(self.loser_url)
        self.loser_container.player = challenger
        
    def choose_left(self) -> None:
        self.index += 1
        #self.left_url.clear()
        self.loser_url.clear()
        self.current_champion = self.left_container.player
        self.loser_container = self.right_container
        self.load_current_match()

    def choose_right(self) -> None:
        self.current_champion = self.right_container.player
        self.index += 1
        self.loser_url.clear()
        #self.right_url.clear()
        self.loser_container = self.left_container
        self.load_current_match()
    
    def handle_exit(self) -> None:
        if self.parent_torneo:
            self.parent_torneo.save_state_and_exit()
        else:
            self.close()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        x_width = self.width()
        self.exit_btn.move( x_width - self.exit_btn.width() - 10, 10)
        round_label = getattr(self, "roundLabel", None)
        if round_label is not None:
            round_label.move((x_width - round_label.width()) // 2, 10)
            girone_y = round_label.height() + 30
        else:
            girone_y = 10
        self.gironeLabel.move((x_width - self.gironeLabel.width()) // 2, girone_y)
        self.match_counter.move( ( x_width - self.match_counter.width() ) // 2, self.height() - self.match_counter.height() - 10 )

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_D:
            self.choose_right()
        if event.key() == Qt.Key.Key_A:
            self.choose_left()

    def __del__(self):
        print("Girone distrutto dal GC!")
