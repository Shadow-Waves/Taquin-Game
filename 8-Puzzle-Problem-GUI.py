from PyQt6.QtGui import QIcon,QAction,QPixmap
from PyQt6.QtWidgets import QLabel,QApplication,QMainWindow,QMenu,QGridLayout,QGroupBox,QInputDialog
from PyQt6.QtCore import Qt,QPropertyAnimation,QEasingCurve,QPoint,QRect
from PyQt6.QtTest import QTest
from sys import argv
from Puzzle import Taquin
from random import choice
from Score import Score

class TaquinGUI(QMainWindow):
    def __init__(self):
        super().__init__()
            
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle("Taquin")
        self.setWindowOpacity(.8)
        self.setFixedSize(400,400)
        self.setStyleSheet("background-color:#C46210;")
        
        self.size_mat = 3
        self.method = "a*"
        self.array = [1,2,3,4,5,6,0,7,8]
        
        self.main_menu = self.menuBar()
        self.main_menu.setStyleSheet("background:grey;color:white;font-size:14px;font-weight:bold;")
        self.size_menu = QMenu("&Size",self)
        self.size_menu.setStyleSheet("background-color:#9C2542;color:#00CC99;font-size:15px;font-weight:bold;")
        self.thbth = QAction(QIcon("3.png"),"3 x 3",self)
        self.thbth.triggered.connect(self.thbth_func)
        self.tbt = QAction(QIcon("2.png"),"2 x 2",self)
        self.tbt.triggered.connect(self.tbt_func)
        self.size_menu.addActions([self.tbt,self.thbth])
        self.run_menu = QAction("&Play",self)
        self.run_menu.triggered.connect(self.run)
        self.quit_menu = QAction("&Quit",self)
        self.quit_menu.triggered.connect(self.quit_game)
        self.search_menu = QMenu("&Search Algorithms",self)
        self.search_menu.setStyleSheet("background-color:#9C2542;color:#00CC99;font-size:15px;font-weight:bold;")
        self.informed_search = QAction("<<&Informed Search>>",self)
        self.informed_search.setEnabled(False)
        self.a_star = QAction("&A*",self)
        self.a_star.triggered.connect(self.a_star_func)
        self.blind_search = QAction("<<&Blind Search>>",self)
        self.blind_search.setEnabled(False)
        self.breadth_first_search = QAction("BFS",self)
        self.breadth_first_search.triggered.connect(self.bfs_func)
        self.depth_first_search = QAction("DFS",self)
        self.depth_first_search.triggered.connect(self.dfs_func)
        self.search_menu.addActions([self.informed_search,self.a_star])
        self.search_menu.addSeparator()
        self.search_menu.addActions([self.blind_search,self.breadth_first_search,self.depth_first_search])
        self.main_menu.addMenu(self.size_menu)
        self.main_menu.addMenu(self.search_menu)
        self.main_menu.addActions([self.run_menu,self.quit_menu])
        
        self.title = QLabel("Taquin",self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("background-color:transparent;color:red;font-weight:bold;font-size:60px;")
        self.title.resize(200,100)
        self.animation = QPropertyAnimation(self.title,b"pos")
        self.animation.setEasingCurve(choice([QEasingCurve.Type.OutExpo,QEasingCurve.Type.OutBounce,QEasingCurve.Type.OutCubic,QEasingCurve.Type.OutCurve]))
        self.animation.setStartValue(QPoint(*choice([(0,20),(400,20),(400,400),(0,400)])))
        self.animation.setEndValue(QPoint(100, 130))
        self.animation.setDuration(1500)
        self.animation.start()
        
        self.refresh = QLabel(self)
        self.refresh.setGeometry(380,25,20,20)
        self.refresh.setStyleSheet("background-color:transparent;")
        self.refresh.setPixmap(QPixmap("reload.png").scaled(20,20))
        self.refresh.mousePressEvent = self.reload
        
        self.show()
        
    def a_star_func(self):
        self.method = "a*"
        
    def bfs_func(self):
        self.method = "bfs"
    
    def dfs_func(self):
        self.method = "dfs"
        
    def run(self):
        try:
            self.size_menu.setEnabled(False)
            self.run_menu.setEnabled(False)
            self.search_menu.setEnabled(False)
            self.refresh.hide()
            self.title.hide()
            self.gbox = QGroupBox(self)
            self.glayout = QGridLayout(self)
            self.glayout.setGeometry(QRect(0,0,400,400))
            if self.method == "a*":
                iteration,grid = Taquin(self.array,self.size_mat).A_star()
                grid = [i[0] for i in grid]
            elif self.method == "bfs":
                iteration,grid = Taquin(self.array,self.size_mat).BFS()
            else:
                iteration,grid = Taquin(self.array,self.size_mat).DFS()
                grid.reverse()
            self.score = Score(self,f"Your Solution With '{self.method.upper()}' Is Found\nWithin {iteration} Iteration(s).",self.x(),self.y())
            for element in grid:
                QTest.qWait(1000)
                for i in range(self.size_mat):
                    for j in range(self.size_mat):
                        x = QLabel()
                        x.setPixmap(QPixmap(f"{element[i][j]}.png").scaled(100,100))
                        self.glayout.addWidget(x,i,j,1,1,Qt.AlignmentFlag.AlignCenter)
                        self.gbox.setLayout(self.glayout)
                        self.setCentralWidget(self.gbox)
        except:
            self.score = Score(self,f"The Algorithm {self.method.upper()}\nDidn't Find The Solution Or It Took Too\nLong Try Another Search Algorithm",self.x(),self.y())
            
    def thbth_func(self):
        self.size_mat = 3
        self.array , _ = QInputDialog.getText(self,"Enter The Matrix Elements","Ex : [1,2,3,4,5,6,7,8,0]\nThe Empty Field Is Considered As 0")
        self.array = self.array.strip().replace("]","").replace("[","").replace("(","").replace(")","").replace(" ","").split(",") if "," in self.array else self.array.strip().replace("]","").replace("[","").replace("(","").replace(")","").split()
        while (len(self.array) != self.size_mat**2) or not all([True if i.isdigit() else False for i in self.array]) or len({int(i) for i in self.array}) != self.size_mat**2 or not all([True if self.array.count(i) == 1 and "0" in self.array else False for i in self.array]) or not Taquin(self.array,3).is_solvable():
            if not _ : break
            self.array , _ = QInputDialog.getText(self,"Enter The Matrix Elements","Ex : [1,2,3,4,5,6,7,8,0]\nThe Empty Field Is Considered As 0")
            self.array = self.array.strip().replace("]","").replace("[","").replace("(","").replace(")","").replace(" ","").split(",") if "," in self.array else self.array.strip().replace("]","").replace("[","").replace("(","").replace(")","").split()
        self.array = [int(i) for i in self.array]
        
    def tbt_func(self):
        self.size_mat = 2
        self.array , _ = QInputDialog.getText(self,"Enter The Matrix Elements","Ex : [1,2,3,0]\nThe Empty Field Is Considered As 0")
        self.array = self.array.strip().replace("]","").replace("[","").replace("(","").replace(")","").replace(" ","").split(",") if "," in self.array else self.array.strip().replace("]","").replace("[","").replace("(","").replace(")","").split()
        while (len(self.array) != self.size_mat**2) or not all([True if i.isdigit() else False for i in self.array]) or len({int(i) for i in self.array}) != self.size_mat**2 or not all([True if self.array.count(i) == 1 and "0" in self.array else False for i in self.array])  or not Taquin(self.array,2).is_solvable():
            if not _ : break
            self.array , _ = QInputDialog.getText(self,"Enter The Matrix Elements","Ex : [1,2,3,4,5,6,7,8,0]\nThe Empty Field Is Considered As 0")
            self.array = self.array.strip().replace("]","").replace("[","").replace("(","").replace(")","").replace(" ","").split(",") if "," in self.array else self.array.strip().replace("]","").replace("[","").replace("(","").replace(")","").split()
        self.array = [int(i) for i in self.array]
        
    def reload(self,e):
        self.animation.setEasingCurve(choice([QEasingCurve.Type.OutExpo,QEasingCurve.Type.OutBounce,QEasingCurve.Type.OutCubic,QEasingCurve.Type.OutCurve]))
        self.animation.setStartValue(QPoint(*choice([(0,20),(400,20),(400,400),(0,400)])))
        self.animation.setEndValue(QPoint(100, 130))
        self.animation.setDuration(1500)
        self.animation.start()
        
    def quit_game(self):
        self.close()
        exit(0) 
        
    def reset(self):
        self.close()
        self.taquin_gui = TaquinGUI()
        
if __name__ == "__main__":
    application = QApplication(argv)
    taquin_gui = TaquinGUI()
    application.exec()