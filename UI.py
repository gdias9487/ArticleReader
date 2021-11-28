from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import sys
import articles

import pygame.mixer

global paused
paused = False



class ScrollLabel(QScrollArea):

    

    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        lay = QVBoxLayout(content)
        self.label = QLabel(content)
        self.font = self.label.font()
        self.font.setFamily("Franklin Gothic Medium")
        self.font.setPointSize(12)
        self.label.setFont(self.font)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)
        lay.addWidget(self.label)
    def setText(self, text):
        self.label.setText(text)
 

class AnotherWindow(QWidget):
    

    def __init__(self, index):
        
        super().__init__()
        layout = QGridLayout()
        self.setGeometry(300, 150, 1280, 720)
        self.setWindowTitle("Article Reader")
        self.converter = QPushButton("Convert", self)
        self.converter.clicked.connect(lambda : self.convert(index))
        self.converter.setGeometry(150,50, 50, 20)
        self.play = QPushButton("Play", self)
        self.play.clicked.connect(lambda : articles.stream(index))
        self.play.setGeometry(150,50, 50, 20)
        self.stop = QPushButton("Stop", self)
        self.stop.clicked.connect(lambda: self.pause(paused))
        self.stop.setGeometry(150,50, 50, 20)
        self.loading = QProgressBar(self)
        self.loading.setGeometry(30, 40, 200, 25)
        self.text1 = QLabel(f"{articles.get_article_title_by_index(index)}")
        self.font = self.text1.font()
        self.content = ScrollLabel(self)
        self.content.setText(articles.get_article_text_by_index(index))
        self.content.setGeometry(150,100,1000,600)
        self.font.setFamily("Bahnschrift")
        self.font.setPointSize(15)
        self.text1.setFont(self.font)
        self.text1.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.text1, 0, 0, 1, 3)
        layout.addWidget(self.play, 2, 1)
        layout.addWidget(self.stop, 2, 2)
        layout.addWidget(self.converter, 2, 0)
        layout.addWidget(self.loading, 3, 0, 1, 3)
        layout.addWidget(self.content, 4, 0, 1, 3)
        self.setLayout(layout)

    def convert(self, index):
        lambda: articles.hear_article(articles.get_article_text_by_index(index),
                                                           str(index))
        for i in range(101):
            time.sleep(0.7)
            self.loading.setValue(i)
        return None

    def pause(self, is_paused):
        global paused
        paused = is_paused

        if paused:
            # Unpause
            pygame.mixer.music.unpause()
            paused = False
        else:
            # Pause
            pygame.mixer.music.pause()
            paused = True
    
    
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = None
        layout = QVBoxLayout()
        self.listwidget = QListWidget(self)
        self.font = self.listwidget.font()
        self.font.setFamily("Franklin Gothic Medium")
        self.font.setPointSize(12)
        self.listwidget.insertItems(0, articles.get_all_articles_title())
        self.listwidget.setGeometry(150,150,1000,500)
        self.listwidget.verticalScrollBar()
        self.listwidget.itemDoubleClicked.connect(lambda: self.openned_article(int(self.listwidget.currentRow())))
        self.listwidget.setFont(self.font)
        self.text1 = QLabel("Welcome to Article Reader!", self)
        self.text2 = QLabel("You can choose one of the above articles and generate an mp3 audio with its content.", self)
        self.font1 = self.text1.font()
        self.font1.setFamily("Bahnschrift")
        self.font1.setPointSize(25)
        self.text1.setFont(self.font1)
        self.font2 = self.text2.font()
        self.font2.setFamily("Bahnschrift")
        self.font2.setPointSize(15)
        self.text2.setFont(self.font2)
        self.text1.setStyleSheet("border: 0px solid black;")
        self.text1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text1.setAlignment(Qt.AlignHCenter)
        self.text1.move(440, 55)
        self.text2.move(340, 105)
        self.text1.adjustSize()
        self.text2.adjustSize()
        layout.addWidget(self.text1)
        layout.addWidget(self.text2)
        layout.addWidget(self.listwidget)
        self.setLayout(layout)
        self.setGeometry(300, 150, 1280, 720)
        self.setWindowTitle("Article Reader")
        self.show()
    
    def openned_article(self, index):
        self.app = AnotherWindow(index)
        self.app.show()

 
app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())