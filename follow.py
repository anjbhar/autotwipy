from PySide2.QtCore import QThread, SIGNAL
import random
import time
import tweepy
import util


class FollowThread(QThread):

    def __init__(self, bot, item, limit, mode):
        QThread.__init__(self)
        self.api = bot.api
        self.item = item
        self.limit = limit
        self.mode = mode
        self.me = self.api.me()

    def __del__(self):
        self.wait()

    def run(self):
        if self.mode == 1:
            self.follow_users_from_retweeters(self.item, self.limit)
        elif self.mode == 2:
            self.follow_users_from_handle(self.item, self.limit)
        self.emit(SIGNAL('finished()'))

    def follow_users_from_retweeters(self, link, limit):
        id_tweet = link.split("/")[-1]
        count = 0
        try:
            retweeters = self.api.retweeters(id_tweet)
        except tweepy.RateLimitError:
            print("sleeping on rate limit")
            self.emit(SIGNAL('post_follow(QString)'), "bad")
            self.sleep(15 * 60)
            self.follow_users_from_retweeters(link, limit)
        strcount = str(len(retweeters))
        msg = strcount
        self.emit(SIGNAL('setup_prog(QString)'), msg)
        for u in retweeters:
            user = self.api.get_user(u)
            if count == limit:
                time.sleep(26500)
                count = 0
            t = util.get_time()
            b = self.check_follow(self.me.id, u)
            if b is True:
                message = f"{t} following user: {user.screen_name}"
                self.api.create_friendship(u)
                self.emit(SIGNAL('post_follow(QString)'), message)
                self.sleep(random.randint(1, 720))
            else:
                message = f"{t} friendship already exists: {user.screen_name}"
                self.emit(SIGNAL('post_follow(QString)'), message)
                self.sleep(5)
        return

    def follow_users_from_handle(self, handle, limit):
        try:
            lst = self.api.followers(handle)
        except tweepy.RateLimitError:
            print("sleeping on rate limit")
            self.emit(SIGNAL('post_follow(QString)'), "bad")
            self.sleep(15 * 60)
        count = 0
        msg = str(len(lst))
        self.emit(SIGNAL('setup_prog(QString)'), msg)
        for user in lst:
            if count == limit:
                self.sleep(26500)
                count = 0
            b = self.check_follow(self.me.id, user.id)
            t = util.get_time()
            if b is True:
                self.api.create_friendship(user)
                self.emit(SIGNAL('post_follow(QString)'), message)
                self.sleep(random.randint(1, 720))
            else:
                message = f"{t} friendship already exists: {user.screen_name}"
                self.emit(SIGNAL('post_follow(QString)'), message)
                self.sleep(5)
        return

    def getAllFollowers(self, screen_name):
        followers = self.limit_handled(tweepy.Cursor(self.api.followers, screen_name=screen_name).items())
        temp = []
        for user in followers:
            temp.append(user)

        return temp

    def limit_handled(self, cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                print("sleeping on rate limit")
                self.emit(SIGNAL('post_follow(QString)'), "bad")
                self.sleep(15 * 60)
            except StopIteration:
                print("wild")

    def check_follow(self, id_source, id_target):
        status = self.api.show_friendship(source_id=id_source, target_id=id_target)
        if status[0] is False and status[1] is True:
            return False
        if status[0] is True:
            return False
        elif status[0] is False:
            return True
