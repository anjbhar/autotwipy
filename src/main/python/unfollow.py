import sqlite3

from PySide2.QtCore import QThread, SIGNAL
import random



class UnfollowThread(QThread):

    def __init__(self, bot):
        QThread.__init__(self)
        self.api = bot.api
        self.me = self.api.me()
        self.db = sqlite3.connect('database', check_same_thread=False)

    def __del__(self):
        self.wait()

    def run(self):
        self.unfollow_all()


    def unfollow_all(self):
        followers = []
        cur = self.db.cursor()
        cur.execute("SELECT * FROM followed_users")
        rows = cur.fetchall()
        for row in rows:
            followers.append(row[1])
        for u in followers:
            user = self.api.get_user(u)
            print(user.screen_name)
            id = user.id
            self.api.destroy_friendship(id)
            self.emit(SIGNAL('post_unfol(QString)'), user.screen_name)
            cur.execute("DELETE FROM followed_users WHERE id = id;")
            self.db.commit()
            self.sleep(random.randint(1, 720))
        self.db.close()

