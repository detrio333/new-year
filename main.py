import os
import random
import sys
import time
from datetime import datetime
import schedule

from PyQt5.QtCore import pyqtSignal, QThread, Qt, QUrl
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel

waiting_phrases = ("Обожди маленечко", "Всему своё время", "Рано ещё", "Приготовлениям время, а ...")


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Worker(QThread):
    show_congratulation_signal = pyqtSignal()
    change_phrase_signal = pyqtSignal()

    def __init__(self):
        super(Worker, self).__init__()

    # def show_congratulation(self):
    #     self.show_congratulation_signal.emit()

    def change_phrase(self):
        self.change_phrase_signal.emit()

    def run(self):
        # schedule.every(10).seconds.do(self.show_congratulation)
        schedule.every(2).seconds.do(self.change_phrase)

        while True:
            schedule.run_pending()
            time.sleep(1)

            dt = datetime.now()
            if dt > datetime(2020, 12, 31, 12):
                self.show_congratulation_signal.emit()
                break


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        pixmap = QPixmap(resource_path("2.jpg"))
        self.setFixedSize(pixmap.width(), pixmap.height())

        self.worker = Worker()
        self.worker.start()

        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())

        self.label_text = QLabel(self)
        self.label_text.setText("Рано ещё")
        self.label_text.setFont(QFont('SansSerif', 30))
        self.label_text.move(50, int(pixmap.height() * 0.75))
        self.label_text.resize(1000, 60)
        self.label_text.setAlignment(Qt.AlignLeft)

        self.worker.show_congratulation_signal.connect(self._show_picture)
        self.worker.change_phrase_signal.connect(self._change_phrase)
        self.worker.start()

    def _change_phrase(self):
        random_int = random.randint(0, len(waiting_phrases) - 1)
        phrase = waiting_phrases[random_int]
        self.label_text.setText(phrase)

    def _show_picture(self):
        def change_picture():
            self.label_text.setText("Пароль: 321")
            pixmap = QPixmap(resource_path("1.jpg"))
            self.label.setPixmap(pixmap)

        def play_music():
            playlist = QMediaPlaylist(self)
            url = QUrl.fromLocalFile(resource_path("Wham! - Last Christmas.mp3"))
            playlist.addMedia(QMediaContent(url))
            playlist.setPlaybackMode(QMediaPlaylist.Loop)

            player = QMediaPlayer(self)
            player.setPlaylist(playlist)
            player.play()

        change_picture()
        play_music()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Открытка")
    app.setWindowIcon(QIcon(resource_path("icon.ico")))

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
