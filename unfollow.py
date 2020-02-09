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
        self.unfollow_all()


    def unfollow_all(self):
        count = 0
        try:
            for follower in self.limit_handled(tweepy.Cursor(self.api.followers).items()):
                print(follower.screen_name)
                # self.api.destroy_friendship(follower.id)
                # self.sleep(random.randint(1, 720))
                count+=1
                self.emit(SIGNAL('post_unfol(QString)'), follower.screen_name)
        except:
            print("bad")
        print(count)


    def limit_handled(self, cursor):
        while True:
            try:
                yield cursor.next()
                self.sleep(60)
            except tweepy.RateLimitError:
                self.emit(SIGNAL('post_unfol(QString)'), "bad")
                self.sleep(15 * 60)
            except StopIteration:
                self.sleep(15 * 60)