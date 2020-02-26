from PySide2.QtCore import QThread
import sqlite3

class ScheduleThread(QThread):

    def __init__(self, bot):
        QThread.__init__(self)
        self.api = bot.api
        self.me = self.api.me()
        self.db = sqlite3.connect('database', check_same_thread=False)

    def __del__(self):
        self.wait()

    def run(self):
        pass