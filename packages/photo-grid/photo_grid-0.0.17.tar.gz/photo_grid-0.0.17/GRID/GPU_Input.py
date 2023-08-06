import numpy as np
import pandas as pd
import io
import urllib.request
from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Panel_Input(QWidget):
    def __init__(self):
        super().__init__()
        # QGroupBox{border-radius:px}
        '''attr'''
        # user define
        self.gr_user = QGroupBox("User's Input")
        self.lo_user = QGridLayout()
        self.lb_img = QLabel()
        self.lb_map = QLabel()
        self.fd_img = QLineEdit()
        self.fd_map = QLineEdit()
        self.bt_img = QPushButton()
        self.bt_map = QPushButton()
        # demo
        self.gr_demo = QGroupBox("Demo")
        self.lo_demo = QVBoxLayout()
        self.lb_demo = QLabel("Will use sample files to demo the program")
        # self
        self.layout = QVBoxLayout()
        '''initialize UI'''
        self.initUI()
    def initUI(self):
        '''user'''
        # GUI components
        self.gr_user.setCheckable(True)
        self.gr_user.setChecked(False)
        self.gr_user.clicked.connect(lambda: self.toggle(self.gr_user))
        self.lb_img.setText("Image (.tif, .jpg, .png):")
        self.lb_map.setText("Map (.csv, .txt)(OPTIONAL):")
        font = self.fd_img.font()
        font.setPointSize(25)
        fm = QFontMetrics(font)
        self.fd_img.setFixedHeight(fm.height())
        self.fd_map.setFixedHeight(fm.height())
        self.bt_img.setText("Browse")
        self.bt_img.clicked.connect(self.assign_PathImg)
        self.bt_map.setText("Browse")
        self.bt_map.clicked.connect(self.assign_PathMap)
        # layout
        self.lo_user.addWidget(self.lb_img, 0, 0)
        self.lo_user.addWidget(self.fd_img, 0, 1)
        self.lo_user.addWidget(self.bt_img, 0, 2)
        self.lo_user.addWidget(self.lb_map, 1, 0)
        self.lo_user.addWidget(self.fd_map, 1, 1)
        self.lo_user.addWidget(self.bt_map, 1, 2)
        self.gr_user.setLayout(self.lo_user)
        '''demo'''
        # GUI components
        self.gr_demo.setCheckable(True)
        self.gr_demo.setChecked(True)
        self.gr_demo.clicked.connect(lambda: self.toggle(self.gr_demo))
        # layout
        self.lo_demo.addWidget(self.lb_demo)
        self.gr_demo.setLayout(self.lo_demo)
        '''layout'''
        self.layout.setContentsMargins(400, 50, 400, 50)
        self.layout.addWidget(self.gr_user)
        self.layout.addWidget(self.gr_demo)
        '''finalize'''
        self.setLayout(self.layout)
        self.show()
    def toggle(self, groupbox):
        if (groupbox.title()=="Demo"):
            self.gr_user.setChecked(not self.gr_user.isChecked())
        elif (groupbox.title()!="Demo"):
            self.gr_demo.setChecked(not self.gr_demo.isChecked())
    def assign_PathImg(self):
        fileter = "Images (*.tif *.jpg *.jpeg *.png)"
        path = QFileDialog().getOpenFileName(self, "", "", fileter)[0]
        self.fd_img.setText(path)
    def assign_PathMap(self):
        fileter = "Map (*.csv *.txt)"
        path = QFileDialog().getOpenFileName(self, "", "", fileter)[0]
        self.fd_map.setText(path)
    def get_img(self):
        if self.gr_user.isChecked():
            import rasterio
            # user input
            ras = rasterio.open(self.fd_img.text())
            nCh = ras.count
            if nCh<3:
                img_np = np.zeros((ras.height, ras.width, 3), dtype="uint8")
                for i in range(3):
                    img_np[:,:,i] = ras.read(1)
            else:
                img_np = np.zeros((ras.height, ras.width, nCh), dtype="uint8")
                for i in range(nCh):
                    img_np[:,:,i] = ras.read(i+1)
            img = img_np.astype(np.uint8)
            # map
            try:
                map = pd.read_csv(self.fd_map.text(), header=None)
            except:
                map = None
        else:
            # demo
            path_map = "http://www.zzlab.net/James_Demo/seg_map.csv"
            path_img = "http://www.zzlab.net/James_Demo/seg_img.jpg"
            map = pd.read_csv(path_map, header=None)
            with urllib.request.urlopen(path_img) as url:
                file = io.BytesIO(url.read())
                img = np.array(Image.open(file))
            # demo 2
            # img = read_jpg("/Users/jameschen/Dropbox/James Chen/GRID/Modeling/Rhombus.jpg")
            # map = pd.read_csv("/Users/jameschen/Dropbox/James Chen/GRID/Modeling/Rhombus_Solution.csv", header=None)
        return img, map
