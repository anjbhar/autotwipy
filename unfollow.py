from PySide2.QtCore import QThread, SIGNAL
import random
import time
import tweepy
import util



class UnfollowThread(QThread):

    def __init__(self, bot):
        QThread.__init__(self)
        self.api = bot.api
        self.me = self.api.me()

    def __del__(self):
        self.wait()

    def run(self):
        pass


    def unfollow_all(self):
        for follower in self.limit_handled(tweepy.Cursor(self.api.followers).items()):
            self.api.destroy_friendship(follower.id)
            self.sleep(random.randint(1, 720))

    def limit_handled(self, cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                self.sleep(15 * 60)