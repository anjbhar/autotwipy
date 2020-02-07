import sys

import tweepy
import csv
import os
import apiconnector
from PySide2 import QtGui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import QLabel, QApplication, QTabWidget, QWidget, QFormLayout, \
    QLineEdit, QPushButton, QPlainTextEdit, QComboBox, QSpinBox, QHBoxLayout, QProgressBar, QMessageBox

from follow import FollowThread


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
        self.h_box_key = QHBoxLayout()
        self.change_key_b = QPushButton("Edit keys")
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
        self.box_label = QLabel("Link to tweet")
        self.combo_label = QLabel("Mode")
        self.spin_label = QLabel("Limit before sleep")
        self.prog_bar = QProgressBar()
        self.combo_box = QComboBox()
        self.h_box = QHBoxLayout()
        self.spin_box = QSpinBox()
        self.link_box = QLineEdit()
        self.link_result = QLabel()
        self.follow_button = QPushButton("Follow Retweeters")
        self.cancel_button = QPushButton("Cancel")
        self.logger = QPlainTextEdit()

        #tab unfollow
        self.unfollow_button = QPushButton("Unfollow All")
        self.unf_logger = QPlainTextEdit()
        self.unfollow_cancel = QPushButton("Cancel")
        self.unf_confirm = QMessageBox()


        #tabs
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.setWindowTitle("Optumize")
        self.setWindowIcon(QtGui.QIcon('assets/oo.png'))

        #threads
        self.follow_thread = None

    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow(self.h_box)
        self.h_box.addWidget(self.combo_label)
        self.combo_label.setAlignment(Qt.AlignRight)
        self.h_box.addWidget(self.combo_box)
        self.combo_box.addItem("Follow Retweeters")
        self.combo_box.addItem("Follow Followers")
        self.combo_box.currentIndexChanged.connect(self.selection_change)

        self.h_box.addWidget(self.spin_label)
        self.spin_label.setAlignment(Qt.AlignRight)
        self.h_box.addWidget(self.spin_box)
        self.spin_box.setMinimum(1)
        self.spin_box.setValue(30)

        layout.addRow(self.box_label, self.link_box)
        self.link_result.setAlignment(Qt.AlignCenter)
        layout.addRow(self.link_result)
        layout.addRow(self.follow_button)
        self.follow_button.clicked.connect(self.follow_ret)

        layout.addRow(self.cancel_button)
        self.cancel_button.clicked.connect(self.cancel_onclick)
        layout.addRow(self.logger)

        self.logger.setReadOnly(True)
        layout.addRow(self.prog_bar)
        self.prog_bar.setAlignment(Qt.AlignCenter)
        self.setTabText(0, "Follow")
        self.tab1.setLayout(layout)

    def selection_change(self, i):
        if i == 0:
            self.box_label.setText("Link to tweet")
            self.follow_button.setText("Follow Retweeters")
            self.link_result.setText("")
            self.follow_button.clicked.connect(self.follow_ret)
        else:
            self.box_label.setText("Handle of user")
            self.follow_button.setText("Follow Followers")
            self.link_result.setText("")
            self.follow_button.clicked.connect(self.follow_fol)

    def cancel_onclick(self):
        if self.follow_thread is None:
            pass
        elif self.follow_thread.isRunning():
            self.logger.appendPlainText("Cancelled script")
            self.follow_thread.terminate()
            self.follow_thread = None

    def follow_ret(self):
        self.prog_bar.setValue(0)
        self.follow_button.setEnabled(False)
        self.link_result.setText("")
        self.logger.clear()
        limit = self.spin_box.value()
        if self.bot is None:
            self.link_result.setText("<font color='red'>Configure access keys in set keys tab</font>")
            return
        if self.follow_thread is not None:
            self.link_result.setText("<font color='red'>Please wait on other script or cancel</font>")
            return
        link = self.link_box.text()
        id_tweet = link.split("/")[-1]
        try:
            tweet = self.bot.api.get_status(id_tweet)

            self.logger.appendPlainText(f"following retweeters from link: {link}...")
            self.follow_thread = FollowThread(self.bot, id_tweet, limit, 1)
            self.follow_thread.start()
            self.connect(self.follow_thread, SIGNAL("finished()"), self.done)
            self.connect(self.follow_thread, SIGNAL("setup_prog(QString)"), self.setup_prog)
            self.connect(self.follow_thread, SIGNAL("post_follow(QString)"), self.post_follow)
        except tweepy.error.TweepError:
            self.follow_button.setEnabled(True)
            self.link_result.setText("<font color='red'>Could not find tweet</font>")


    def setup_prog(self, msg):
        self.prog_bar.setMaximum(int(msg))


    def follow_fol(self):
        self.prog_bar.setValue(0)
        self.follow_button.setEnabled(False)
        self.link_result.setText("")
        self.logger.clear()
        limit = self.spin_box.value()
        if self.bot is None:
            self.link_result.setText("<font color='red'>Configure access keys in set keys tab</font>")
            return
        if self.follow_thread is not None:
            self.link_result.setText("<font color='red'>Please wait on other script or cancel</font>")
        handle = self.link_box.text()
        if handle == '':
            self.link_result.setText("<font color='red'>Enter a handle above</font>")
            return
        elif handle[0] == '@':
            id_user = handle[1:]
        else:
            id_user = handle
        try:
            man = self.bot.api.get_user(id_user)
            self.logger.appendPlainText(f"following followers of {man.screen_name}...")
            self.follow_thread = FollowThread(self.bot, id_user, limit, 2)
            self.connect(self.follow_thread, SIGNAL("finished()"), self.done)
            self.connect(self.follow_thread, SIGNAL("setup_prog(QString)"), self.setup_prog)
            self.connect(self.follow_thread, SIGNAL("post_follow(QString)"), self.post_follow)
        except tweepy.error.TweepError:
            self.follow_button.setEnabled(True)
            self.link_result.setText("<font color='red'>Could not find user</font>")

    def post_follow(self, message):
        self.logger.appendPlainText(message)
        self.prog_bar.setValue(self.prog_bar.value()+1)

    def done(self):
        self.follow_thread = None
        self.follow_button.setEnabled(True)

    def tab2UI(self):
        layout = QFormLayout()
        layout.addRow(self.unfollow_button)
        layout.addRow(self.unfollow_cancel)
        self.unfollow_button.clicked.connect(self.unfollow_fol)
        self.unfollow_cancel.clicked.connect(self.unfollow_can)
        layout.addWidget(self.unf_logger)
        self.setTabText(1, "Unfollow")
        self.tab2.setLayout(layout)

    def unfollow_fol(self):
        pass

    def unfollow_can(self):
        pass

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
        layout.addRow(self.h_box_key)
        self.h_box_key.addWidget(self.change_key_b)
        self.h_box_key.addWidget(self.set_button)
        self.change_key_b.clicked.connect(self.change_keys)
        layout.addRow(self.handle_info)
        self.handle_info.setAlignment(Qt.AlignCenter)
        layout.addRow(self.follower_info)
        self.follower_info.setAlignment(Qt.AlignCenter)
        layout.addRow(self.ready_lab)
        self.ready_lab.setAlignment(Qt.AlignCenter)
        self.setTabText(2, "Settings")
        self.tab3.setLayout(layout)

    def change_keys(self):
        self.set_button.setEnabled(True)

    def set_keys(self):
        self.set_button.setEnabled(False)
        self.result.setText("")
        one = self.edit_1.text()
        two = self.edit_2.text()
        three = self.edit_3.text()
        four = self.edit_4.text()
        try:
            self.bot = apiconnector.ApiConnector(one, two, three, four)
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