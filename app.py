import sys
import threading

import tweepy
import csv
import os
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import QLabel, QApplication, QTabWidget, QWidget, QFormLayout, \
    QLineEdit, QPushButton, QPlainTextEdit

from twibot import twibot


class application(QTabWidget):
    bot = 0

    def __init__(self, parent=None):
        super(application, self).__init__(parent)
        self.bot = None
        #tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.resize(640, 400)

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
        self.addTab(self.tab3, "Tab 3")
        # tab set keys
        self.edit_1 = QLineEdit()
        self.edit_2 = QLineEdit()
        self.edit_3 = QLineEdit()
        self.edit_4 = QLineEdit()
        self.result = QLabel()
        self.set_button = QPushButton("Set keys")
        self.handle_info = QLabel()
        self.follower_info = QLabel()
        self.ready_lab = QLabel()

        # tab follow
        self.link_box = QLineEdit()
        self.link_result = QLabel()
        self.follow_button = QPushButton("Follow Retweeters")
        self.handle_box = QLineEdit()
        self.handle_result = QLabel()
        self.follow_button2 = QPushButton("Follow Followers")
        self.cancel_button = QPushButton("Cancel")
        self.logger = QPlainTextEdit()

        #tabs
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.setWindowTitle("Optumize")

        #threads
        self.t1 = None

    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow("Link to tweet", self.link_box)
        layout.addRow(self.link_result)
        layout.addRow(self.follow_button)
        self.follow_button.clicked.connect(self.follow_ret)
        layout.addRow("Handle of user", self.handle_box)
        layout.addRow(self.handle_result)
        layout.addRow(self.follow_button2)
        self.follow_button2.clicked.connect(self.follow_fol)
        layout.addRow(self.cancel_button)
        self.cancel_button.clicked.connect(self.cancel_onclick)
        layout.addRow(self.logger)
        self.logger.setReadOnly(True)
        self.setTabText(0, "Follow")
        self.tab1.setLayout(layout)

    def cancel_onclick(self):
        if self.t1 is None:
            return
        else:
            self.close()
            os._exit(0)


    def follow_ret(self):
        self.link_result.setText("")
        if self.bot is None:
            self.link_result.setText("Configure access keys in set keys tab")
            return
        if self.t1 is not None:
            self.link_result.setText("Please wait on other script or cancel")
            return
        link = self.link_box.text()
        id_tweet = link.split("/")[-1]
        try:
            tweet = self.bot.api.get_status(id_tweet)
            self.t1 = threading.Thread(target=self.bot.follow_users_from_retweeters, args =(link, 30))
            self.t1.start()
        except tweepy.error.TweepError:
            self.link_result.setText("Could not find tweet")

    def follow_fol(self):
        self.handle_result.setText("")
        if self.bot is None:
            self.handle_result.setText("Configure access keys in set keys tab")
            return
        if self.t1 is not None:
            self.handle_result.setText("Please wait on other script or cancel")
        handle = self.handle_box.text()
        if handle == '':
            self.handle_result.setText("Enter a handle above")
            return
        elif handle[0] == '@':
            id_user = handle[1:]
        else:
            id_user = handle
        try:
            man = self.bot.api.get_user(id_user)
            self.t1 = threading.Thread(target=self.bot.follow_users_from_handle, args=(man.screen_name, 30))
            self.t1.start()
        except tweepy.error.TweepError:
            self.handle_result.setText("Could not find user")


    def tab2UI(self):
        layout = QFormLayout()
        layout.addRow("Link to tweet", QLabel())
        layout.addRow(QLabel())
        self.setTabText(1, "Interact")
        self.tab2.setLayout(layout)


    def tab3UI(self):
        layout = QFormLayout()
        layout.addRow("API key", self.edit_1)
        layout.addRow("API key secret", self.edit_2)
        layout.addRow("Auth token", self.edit_3)
        layout.addRow("Auth token secret", self.edit_4)
        self.set_button.clicked.connect(self.set_keys)
        l = self.read_file()
        if l is not None:
            if len(l) == 4:
                self.edit_1.setText(l[0])
                self.edit_2.setText(l[1])
                self.edit_3.setText(l[2])
                self.edit_4.setText(l[3])
                self.set_keys()
        layout.addRow(self.result)
        self.result.setAlignment(Qt.AlignCenter)
        layout.addRow(self.set_button)
        layout.addRow(self.handle_info)
        self.handle_info.setAlignment(Qt.AlignCenter)
        layout.addRow(self.follower_info)
        self.follower_info.setAlignment(Qt.AlignCenter)
        layout.addRow(self.ready_lab)
        self.ready_lab.setAlignment(Qt.AlignCenter)
        self.setTabText(2, "Set keys")
        self.tab3.setLayout(layout)

    def set_keys(self):
        self.set_button.setEnabled(False)
        one = self.edit_1.text()
        two = self.edit_2.text()
        three = self.edit_3.text()
        four = self.edit_4.text()
        try:
            self.bot = twibot(one, two, three, four, self)
            me = self.bot.add_keys(one,two,three,four)
            self.handle_info.setText("Handle: @" + me.screen_name)
            self.follower_info.setText("Followers: " + str(me.followers_count))
            self.ready_lab.setText("<font color='green'>Ready!</font>")
            with open('keys.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([one, two, three, four])
        except:
            print("Could not authenticate you")
            self.result.setText("<font color='red'>Could not authenticate you</font>")
        finally:
            self.set_button.setEnabled(True)

    def read_file(self):
        try:
            with open('keys.csv') as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:
                    return row
        except:
            return None


def main():
    app = QApplication(sys.argv)
    ex = application()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()