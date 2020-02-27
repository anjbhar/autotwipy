from PySide2.QtCore import QThread
import sqlite3

class ScheduleThread(QThread):

    def __init__(self, bot, content, datetime):
        QThread.__init__(self)
        self.api = bot.api
        self.me = self.api.me()
        self.db = sqlite3.connect('database', check_same_thread=False)
        cursor = self.db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS scheduled(content TEXT, datetime TEXT)''')
        self.db.commit()
        self.tweet_list = []

    def __del__(self):
        self.wait()

    def run(self):
        pass


    def start_scheduler(self):
        pass