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
        else:
            self.follow_users_from_handle(self.item, self.limit)
        self.emit(SIGNAL('finished()'))

    def follow_users_from_retweeters(self, link, limit):
        id_tweet = link.split("/")[-1]
        count = 0
        retweeters = self.api.retweeters(id_tweet)
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
        lst = self.api.followers(handle)

        count = 0
        msg = str(len(lst))
        self.emit(SIGNAL('setup_prog(QString)'), msg)
        for user in lst:
            if count == limit:
                self.sleep(26500)
                count = 0
            b = self.check_follow(self.me.id, user.id)
            if b is True:
                t = util.get_time()
                self.api.create_friendship(user)
                self.emit(SIGNAL('post_follow(QString)'), message)
                self.sleep(random.randint(1, 720))
            else:
                message = f"{t} friendship already exists: {user.screen_name}"
                self.emit(SIGNAL('post_follow(QString)'), message)
                self.sleep(5)
        return

    def limit_handled(self, cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                self.sleep(15 * 60)

    def check_follow(self, id_source, id_target):
        status = self.api.show_friendship(source_id=id_source, target_id=id_target)
        if status[0] is False and status[1] is True:
            return False
        if status[0] is True:
            return False
        elif status[0] is False:
            return True
