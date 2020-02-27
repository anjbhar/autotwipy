from PySide2.QtCore import QThread
import sqlite3

class ScheduleThread(QThread):

    def __init__(self, bot):
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
        print("running")
        self.start_scheduler()


    def start_scheduler(self):
        count = 0
        while(self.tweet_list != 0):
            next = self.tweet_list[count]
            if (next[1] == 0):
                pass

    def add_tweet(self, content, datetime):
        print("added")
        if self.tweet_list == []:
            self.tweet_list.append([content, datetime])
        else:
            for i in range (len(self.tweet_list)):
                if (self.tweet_list(i)[1] >= datetime):
                    self.tweet_list.insert(i, [content, datetime])
        return True
