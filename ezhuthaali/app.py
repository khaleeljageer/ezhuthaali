import logging
import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication

from ezhuthaali.core.progress import ProgressStore
from ezhuthaali.core.levels import LevelRepository
from ezhuthaali.ui.main_window import MainWindow


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def run() -> None:
    configure_logging()
    app = QApplication(sys.argv)

    levels = LevelRepository()
    progress_store = ProgressStore()

    window = MainWindow(levels=levels, progress_store=progress_store)
    screen = QGuiApplication.primaryScreen()
    if screen is not None:
        geometry = screen.availableGeometry()
        window.setGeometry(geometry)
    window.show()

    sys.exit(app.exec())
