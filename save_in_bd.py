import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PyQt6 import QtGui

class Save(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('username.ui', self)
        title = ''
        self.setWindowTitle(title)
        name = self.QTextEdit.toPlainText()
        con = sqlite3.connect('abstract.db')
        cursor = con.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        NAME TEXT,
        SCORE INTEGER
        )
        ''')
        cursor.execute('INSERT INTO Users (NAME, SCORE) VALUES (?, ?)', (name, final_score))
        con.commit()
        con.close()