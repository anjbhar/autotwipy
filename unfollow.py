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

    def __del__(self):
        self.wait()

    def run(self):
        self.unfollow_all()


    def unfollow_all(self):
        try:
            followers = self.read_file()
            for u in followers:
                user = self.api.get_user(u)
                print(user.screen_name)
                # self.api.destroy_friendship(follower.id)
                # self.sleep(random.randint(1, 720))
                self.emit(SIGNAL('post_unfol(QString)'), user.screen_name)
        except:
            print("bad")
            self.sleep(60)
            self.unfollow_all()


    def read_file(self):
        users = []
        try:
            with open('user.csv') as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:
                    users.append(row[0])
            return users
        except:
            return None
