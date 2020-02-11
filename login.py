from PySide2 import QtWidgets, QtGui
from PySide2.QtWidgets import QLineEdit
import sqlite3
from app import application

class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.db = sqlite3.connect('database')
        cursor = self.db.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS account(one TEXT, two TEXT)''')
        self.db.commit()
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)
        l = self.check_acc()
        try:
            self.textName.setText(l[0])
            self.textPass.setText(l[1])
        except:
            pass
        finally:
            self.buttonLogin = QtWidgets.QPushButton('Login', self)
            self.buttonLogin.clicked.connect(self.handleLogin)
            self.setWindowTitle("Optumize")
            self.setWindowIcon(QtGui.QIcon('assets/oo.png'))
            layout = QtWidgets.QFormLayout(self)
            layout.addRow("User", self.textName)
            layout.addRow("Password", self.textPass)
            layout.addWidget(self.buttonLogin)


    def handleLogin(self):
        user = self.textName.text()
        passw = self.textPass.text()
        if (self.textName.text() == 'admin' and
            self.textPass.text() == 'admin'):
            cursor = self.db.cursor()
            cursor.execute('DELETE FROM account;',);
            cursor.execute('''INSERT INTO account(one, two) VALUES(?,?)''', (user, passw))
            self.db.commit()
            self.db.close()
            self.accept()

        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')


    def check_acc(self):
        account = []
        cursor = self.db.cursor()
        try:
            cursor.execute('''SELECT one, two FROM account''')
            all_rows = cursor.fetchall()
            for row in all_rows:
                account.append(row[0])
                account.append(row[1])
            return account
        except:
            return None

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = application()
        window.show()
        sys.exit(app.exec_())