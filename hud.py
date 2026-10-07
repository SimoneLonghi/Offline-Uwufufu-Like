from typing import TYPE_CHECKING, Callable

from PyQt6.QtWidgets import QPushButton, QLabel, QWidget, QHBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor

if TYPE_CHECKING:
    from girone import Girone


def set_hud(widget: "Girone") -> None:
    # Elementi UI modulari
    if widget.parent_torneo.round:
        widget.roundLabel = TitleLabel(widget, f"{widget.parent_torneo.round}")
    widget.gironeLabel = TitleLabel(widget, f"GIRONE {widget.girone_num}")
    widget.match_counter = TitleLabel(widget, f"1 di {len(widget.partecipanti) - 1}")
    widget.exit_btn = ExitButton(widget, widget.handle_exit)
    ChoiceButton(widget.left_container, "Scelta", widget.choose_left, "left_button")
    ChoiceButton(widget.right_container, "Scelta", widget.choose_right, "right_button")

class SetContainer(QWidget):
    def __init__(self) -> None:
        super().__init__()
        #self.setStyleSheet("background: black; position: relative;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.view = QWebEngineView()
        layout.addWidget(self.view)

        self.setLayout(layout)

class ExitButton(QPushButton):
    def __init__(self, parent_widget: QWidget, on_click: Callable[[], None]) -> None:
        super().__init__("✕", parent_widget)
        self.setObjectName("exit_button")
        self.setToolTip("Esci")
        self.setFixedSize(parent_widget.width() // 14, parent_widget.width() // 14)
        self.setStyleSheet(f"""
            background-color: red;
            color: white;
        """)
        #self.setContentsMargins(0, 0, 0, 0)     
        self.clicked.connect(on_click)
        self.raise_()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor("white"))
        pen.setWidth(self.width() // 10)  # Spessore della X
        painter.setPen(pen)

        margin = self.width() // 4  # Margine interno per la X

        # Disegna la X centrata e proporzionata
        painter.drawLine(margin, margin, self.width() - margin, self.height() - margin)
        painter.drawLine(self.width() - margin, margin, margin, self.height() - margin)
        
class TitleLabel(QLabel):
    def __init__(self, parent_widget: QWidget, text: str) -> None:
        super().__init__(text, parent_widget)
        self.setObjectName("match_counter_label")
        #self.setFixedSize(parent_widget.width() // 14, parent_widget.width() // 14)
        self.setStyleSheet(f"""
            color: white;
            font-size: {parent_widget.width() // 14}px;
            font-weight: bold;
            background-color: rgba(0, 0, 0, 0.9);
            padding: {parent_widget.width() // 20}px {parent_widget.width() // 8}px;
        """)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.adjustSize()
        self.raise_()

class ChoiceButton(QPushButton):
    def __init__( self, parent_container: QWidget, text: str, on_click: Callable[[], None], name: str ) -> None:
        super().__init__(text, parent_container)

        self.setObjectName(name)
        self.setStyleSheet(f"""
            font-size: {parent_container.width() // 18}px;
            padding: {parent_container.width() // 30}px {parent_container.width() // 8}px;
        """)
        self.adjustSize()
        self.clicked.connect(on_click)

        self.parent().resizeEvent = self.center_in_parent

    def center_in_parent(self, event):
        cont_width = self.parent().width()
        btn_width = self.width()
        x = (cont_width - btn_width) // 2
        self.move(x, 10)  # y=10 fisso
        event.accept()
