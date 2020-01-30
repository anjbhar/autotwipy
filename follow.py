import tweepy
import random
import time
from datetime import datetime


class follow:

    def __init__(self, one, two, three, four, app):
        self.consumer_key = one
        self.consumer_secret = two
        self.access_token = three
        self.access_token_secret = four
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)
        self.app = app
        try:
            self.me = self.api.me()
        except:
            raise ("Error")

    def add_keys(self, one, two, three, four):
        self.consumer_key = one
        self.consumer_secret = two
        self.access_token = three
        self.access_token_secret = four
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)
        me = self.api.me()
        return me

    def follow_users_from_retweeters(self, link, limit):
        id_tweet = link.split("/")[-1]
        retweeters = self.api.retweeters(id_tweet)
        count = 0
        self.app.logger.appendPlainText(f"Following retweeters of {link}")
        for u in retweeters:
            user = self.api.get_user(u)
            if count == limit:
                self.app.logger.appendPlainText("Sleeping...")
                time.sleep(26500)
                count = 0
            b = self.check_follow(self.me.id, u)
            if b is True:
                t = self.get_time()
                mes = str(f"{t}: following {user.screen_name}")
                self.app.logger.appendPlainText(mes)
                self.api.create_friendship(u)
                time.sleep(random.randint(1, 720))
            else:
                self.app.logger.appendPlainText(f"friendship already exists with {user.screen_name}")

        self.app.t1 == None
        self.app.follow_button.setEnabled(True)

    def follow_users_from_handle(self, handle, limit):
        lst = self.api.followers(handle)

        count = 0
        self.app.logger.appendPlainText(f"following followers of {handle}")
        for user in lst:
            if count == limit:
                self.app.logger.appendPlainText("Sleeping...")
                time.sleep(26500)
                count = 0
            b = self.check_follow(self.me.id, user.id)
            if b is True:
                t = self.get_time()
                mes = str(f"{t}: following: {user.screen_name}")
                self.app.logger.appendPlainText(mes)
                self.api.create_friendship(user)
                time.sleep(random.randint(1, 720))
            else:
                self.app.logger.appendPlainText(f"friendship already exists with {user.screen_name}")

        self.app.t1 == None
        self.app.follow_button2.setEnabled(True)

    def get_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def check_follow(self, id_source, id_target):
        status = self.api.show_friendship(source_id=id_source, target_id=id_target)
        if status[0] is False and status[1] is True:
            return False
        if status[0] is True:
            return False
        elif status[0] is False:
            return True
