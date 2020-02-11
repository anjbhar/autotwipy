import time

import tweepy


class ApiConnector:

    def __init__(self, one, two, three, four):
        self.consumer_key = one
        self.consumer_secret = two
        self.access_token = three
        self.access_token_secret = four
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)
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

