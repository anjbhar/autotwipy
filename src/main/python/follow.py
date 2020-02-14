from PySide2.QtCore import QThread, SIGNAL
import random
import time
import tweepy
import util
import csv
import sqlite3

from tweepy import TweepError


class FollowThread(QThread):

    def __init__(self, bot, item, limit, mode, max):
        QThread.__init__(self)
        self.api = bot.api
        self.item = item
        self.limit = limit
        self.mode = mode
        self.max = max
        self.me = self.api.me()
        self.db = sqlite3.connect('database', check_same_thread=False)
        cursor = self.db.cursor()
        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS followed_users(id TEXT, screen_name TEXT)''')
        self.db.commit()
        self.to_follow = []

    def __del__(self):
        self.wait()

    def run(self):
        if self.mode == 1:
            self.follow_users_from_retweeters(self.item, self.limit)
        elif self.mode == 2:
            self.follow_users_from_handle(self.item, self.limit, self.max)
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
                cursor = self.db.cursor()
                cursor.execute('''INSERT INTO followed_users(id, screen_name) VALUES(?,?)''', (user.id, user.screen_name))
                self.db.commit()
                self.api.create_friendship(u)

                self.emit(SIGNAL('post_follow(QString)'), message)
                self.sleep(random.randint(1, 720))
            else:
                message = f"{t} friendship already exists: {user.screen_name}"
                self.emit(SIGNAL('post_follow(QString)'), message)
                self.sleep(5)
        return

    def follow_users_from_handle(self, handle, limit, max):
        try:
            lst = self.getAllFollowers(handle,max)
        except tweepy.RateLimitError:
            print("sleeping on rate limit")
            self.emit(SIGNAL('post_follow(QString)'), "bad")
            self.sleep(15 * 60)
        count = 0
        msg = str(len(lst))
        print(len(lst))
        self.emit(SIGNAL('setup_prog(QString)'), msg)
        for user in lst:
            if count == limit:
                self.sleep(26500)
                count = 0
            b = self.check_follow(self.me.id, user.id)
            t = util.get_time()
            if b is True:
                cursor = self.db.cursor()
                cursor.execute('''INSERT INTO followed_users(id, screen_name) VALUES(?,?)''',
                               (user.id, user.screen_name))
                self.db.commit()
                try:
                    self.api.create_friendship(user.id)
                    message= f"{t} following user: {user.screen_name}"
                    self.emit(SIGNAL('post_follow(QString)'), message)
                    self.sleep(random.randint(1, 720))
                except TweepError:
                    pass
            else:
                message = f"{t} friendship already exists: {user.screen_name}"
                self.emit(SIGNAL('post_follow(QString)'), message)
                self.sleep(5)
        return

    def getAllFollowers(self, screen_name, max):
        followers = self.limit_handled(tweepy.Cursor(self.api.followers, screen_name=screen_name).items())
        count = 0
        temp = []
        for user in followers:
            if count == max:
                return temp
            print(user.screen_name)
            count+=1
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
                print("stopiteration")
                return

    def check_follow(self, id_source, id_target):
        status = self.api.show_friendship(source_id=id_source, target_id=id_target)
        print(status[0].following, status[0].followed_by)
        if status[0].following is False and status[0].followed_by is True:
            return False
        elif status[0].following is True:
            return False
        elif status[0].following is False:
            return True
