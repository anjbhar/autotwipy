import tweepy
import random
import time


class twibot:

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
            me = self.api.me()
        except:
            raise("Error")

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
        for user in retweeters:
            if count == limit:
                self.app.logger.appendPlainText("Sleeping...")
                time.sleep(26500)
                count = 0
            print("following", user)
            mes = str(f"following: {user}")
            self.app.logger.appendPlainText(mes)
            self.api.create_friendship(user)
            time.sleep(random.randint(1,720))
        self.app.t1 == None

    def follow_users_from_handle(self, handle, limit):
        lst = self.api.followers(handle)

        count = 0
        self.app.logger.appendPlainText(f"following followers of {handle}")
        for user in lst:
            if count == limit:
                self.app.logger.appendPlainText("Sleeping...")
                time.sleep(26500)
                count = 0
            mes = str(f"following: {user}")
            self.app.logger.appendPlainText(mes)
            self.api.create_friendship(user)
            time.sleep(random.randint(1, 720))
        self.app.t1 == None

