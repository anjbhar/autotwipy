import sqlite3

from PySide2.QtCore import QThread, SIGNAL
import random
import time
import tweepy
import util
import csv



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
            # self.api.destroy_friendship(follower.id)
            # self.sleep(random.randint(1, 720))
            self.emit(SIGNAL('post_unfol(QString)'), user.screen_name)

