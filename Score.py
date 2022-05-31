from PyQt6.QtWidgets import QMainWindow,QLabel,QPushButton,QVBoxLayout,QGroupBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
class Score(QMainWindow):
    def __init__(self,parent,msg,x,y,*args,**kwargs) -> None:
        super().__init__()
        
        self.setWindowTitle("Score")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(400,200)
        self.setGeometry(x - 400,y + 30,400,200)
        self.setStyleSheet("background-color:black;")
        
        self.parent = parent
        
        self.vbox = QVBoxLayout()
        self.gbox = QGroupBox(self)
        
        self.score_label = QLabel(msg)
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setStyleSheet("background-color:transparent;color:#8FD400;font-weight:bold;font-size:20px;border:1px groove #45A27D;")
        
        self.rematch = QPushButton("Play Again ?",self)
        self.rematch.setStyleSheet("background-color:#A50B5E;color:#214FC6;font-weight:bold;font-size:20px;border:1px groove #FFFF38;border-radius:5px;")
        self.rematch.clicked.connect(self.replay)
        
        self.takeoff = QPushButton("Quit",self)
        self.takeoff.setStyleSheet("background-color:#933709;color:#BD559C;font-weight:bold;font-size:20px;border:1px groove #A0E6FF;border-radius:5px;")
        self.takeoff.clicked.connect(self.quitted)
        
        self.vbox.addWidget(self.score_label)
        self.vbox.addWidget(self.rematch)
        self.vbox.addWidget(self.takeoff)
        
        self.gbox.setLayout(self.vbox)
        
        self.setCentralWidget(self.gbox)
        
        self.show()
    
    def replay(self):
        self.close()
        self.parent.reset()
        
    def quitted(self):
        self.parent.close()
        self.close()
        exit(0)
        