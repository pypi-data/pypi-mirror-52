import numpy as np
import pandas as pd
from enum import Enum
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Dir(Enum):
    NORTH=0
    WEST=1
    SOUTH=2
    EAST=3

def get_peak(img, map, n_smooth=100, axis=0):
    '''
    '''
    from scipy.signal import find_peaks
    import numpy as np
    # compute signal
    ls_mean = img.mean(axis=(not axis)*1) # 0:nrow
    # gaussian smooth signal
    for i in range(n_smooth):
        ls_mean = np.convolve(np.array([1, 2, 4, 2, 1])/10, ls_mean, mode='same')
    peaks, _ = find_peaks(ls_mean)
    if map is not None:
        if len(peaks) > map.shape[axis]:
            while len(peaks) > map.shape[axis]:
                ls_diff = [peaks[i+1]-peaks[i] for i in range(len(peaks)-1)]
                idx_diff = np.argmin(ls_diff)
                idx_kick = idx_diff if (ls_mean[peaks[idx_diff]] < ls_mean[peaks[idx_diff+1]]) else (idx_diff+1)
                peaks = np.delete(peaks, idx_kick)
        elif len(peaks) < map.shape[axis]:
            while len(peaks) < map.shape[axis]:
                ls_diff = [peaks[i+1]-peaks[i] for i in range(len(peaks)-1)]
                idx_diff = np.argmax(ls_diff)
                peak_insert = (peaks[idx_diff]+peaks[idx_diff+1])/2
                peaks = np.sort(np.append(peaks, int(peak_insert)))
    return peaks, ls_mean

def read_jpg(filename):
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = 1e+9
    img = np.array(Image.open(filename)).astype(np.uint8)
    return img

def read_tiff(filename, bands=None, xBSize=5000, yBSize=5000):
    '''import'''
    import gdal
    from tqdm import tqdm_gui
    '''program'''
    ds = gdal.Open(filename)
    gdal.UseExceptions()
    nrow = ds.RasterYSize
    ncol = ds.RasterXSize
    if bands==None:
        bands = range(ds.RasterCount)
    data = np.zeros((nrow, ncol, len(bands)))
    for b in bands:
        band = ds.GetRasterBand(b+1)
        for i in tqdm_gui(range(0, nrow, yBSize), desc="Channel %d/%d"%(b, len(bands)-1), leave=False):
            if i + yBSize < nrow:
                numRows = yBSize
            else:
                numRows = nrow - i
            for j in range(0, ncol, xBSize):
                if j + xBSize < ncol:
                    numCols = xBSize
                else:
                    numCols = ncol - j
                data[i:(i+numRows), j:(j+numCols), b] = band.ReadAsArray(j, i, numCols, numRows)
    return data.astype(np.uint8)

def write_tiff(array, outname):
    driver = gdal.GetDriverByName("GTiff")
    out_info = driver.Create(outname+".tif",
                   array.shape[1], # x
                   array.shape[0], # y
                   array.shape[2], # channels
                   gdal.GDT_Byte)
    for i in range(array.shape[2]):
        out_info.GetRasterBand(i+1).WriteArray(array[:,:,i])

class Panels(Enum):
    INPUT=0
    CROPPER=1
    KMEANER=2
    ANCHOR=3
    OUTPUT=4

class Widget_Img(QWidget):
    '''
    Will keep imgRaw, imgVis and imgQmap
    '''
    def __init__(self, img):
        super().__init__()
        '''attr'''
        self.img_raw = img
        self.img_vis = img[:,:,:3].copy()
    def make_rgb_img(self, img):
        h, w = img.shape[0], img.shape[1]
        qImg = QImage(img.astype(np.uint8), w, h, w*3, QImage.Format_RGB888)
        self.qimg = QPixmap(qImg)
    def make_bin_img(self, img):
        h, w = img.shape[0], img.shape[1]
        qImg = QImage(img.astype(np.uint8), w, h, w*1, QImage.Format_Indexed8)
        qImg.setColor(0, qRgb(0, 0, 0))
        qImg.setColor(1, qRgb(241, 225, 29))
        self.qimg = QPixmap(qImg)
    def make_idx8_img(self, img, k):
        colormap = [qRgb(228,26,28),
                    qRgb(55,126,184),
                    qRgb(77,175,74),
                    qRgb(152,78,163),
                    qRgb(255,127,0),
                    qRgb(255,255,51),
                    qRgb(166,86,40),
                    qRgb(247,129,191),
                    qRgb(153,153,153)]
        h, w = img.shape[0], img.shape[1]
        qImg = QImage(img.astype(np.uint8), w, h, w*1, QImage.Format_Indexed8)
        for i in range(k):
            qImg.setColor(i, colormap[i])
        self.qimg = QPixmap(qImg)
    def make_gray_img(self, img):
        h, w = img.shape[0], img.shape[1]
        qImg = QImage(img.astype(np.uint8), w, h, w*1, QImage.Format_Grayscale8)
        self.qimg = QPixmap(qImg)
    def paintImage(self, painter):
        painter.setRenderHint(QPainter.Antialiasing, True)
        self.size_img = self.qimg.size().scaled(self.rect().size(), Qt.KeepAspectRatio)
        if self.size_img.width()==self.width():
            self.is_fit_width = True
            self.pt_st_img = int((self.height()-self.size_img.height())/2)
            painter.drawPixmap(0, self.pt_st_img, self.size_img.width(), self.size_img.height(), self.qimg)
        elif self.size_img.height()==self.height():
            self.is_fit_width = False
            self.pt_st_img = int((self.width()-self.size_img.width())/2)
            painter.drawPixmap(self.pt_st_img, 0, self.size_img.width(), self.size_img.height(), self.qimg)

def magnifying_glass(widget, pos, area=200, zoom=4):
    size = int(area/zoom)
    pixmap = widget.grab(QRect(QPoint(pos.x()-int(size/2), pos.y()-int(size/2)), QSize(size, size)))
    try:
        rate_screen = size/pixmap.width()
        pixmap = pixmap.scaled(int(area/rate_screen), int(area/rate_screen))
        painter = QPainter(pixmap)
        'Rect'
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(Qt.black)
        painter.setPen(pen)
        # define rect
        rect = QRect(QPoint(0,0), pixmap.size()*rate_screen)
        # draw rect
        painter.drawRect(rect)
        '''Cursor'''
        pen.setWidth(3)
        pen.setColor(Qt.red)
        painter.setPen(pen)
        size_m = 10
        # define lines
        line1 = QLine(QPoint(size_m, 0), QPoint(-size_m, 0))
        line2 = QLine(QPoint(0, size_m), QPoint(0, -size_m))
        line1.translate(pixmap.rect().center()*rate_screen-QPoint(0,0))
        line2.translate(pixmap.rect().center()*rate_screen-QPoint(0,0))
        # draw lines
        painter.drawLine(line1)
        painter.drawLine(line2)
        '''finish'''
        painter.end()
        cursor = QCursor(pixmap)
        widget.setCursor(cursor)
    except:
        '''not in a valid region'''

def save_img(qimg, path):
    w, h = qimg.width(), qimg.height()
    file = QFile(path+".jpg");
    file.open(QIODevice.WriteOnly);
    qimg.save(file, "JPG");

def draw_cross(x, y, painter, size_mark=2):
    l1_st_x, l1_st_y = x-size_mark, y-size_mark
    l1_ed_x, l1_ed_y = x+size_mark, y+size_mark
    l2_st_x, l2_st_y = x-size_mark, y+size_mark
    l2_ed_x, l2_ed_y = x+size_mark, y-size_mark
    painter.drawLine(l1_st_x, l1_st_y, l1_ed_x, l1_ed_y)
    painter.drawLine(l2_st_x, l2_st_y, l2_ed_x, l2_ed_y)

def draw_triangle(x, y, dir, painter, range=7, peak=30):
    path = QPainterPath()
    path.moveTo(x, y)
    if dir=='North':
        path.lineTo(x-range, y+peak)
        path.lineTo(x+range, y+peak)
    elif dir=='South':
        path.lineTo(x-range, y-peak)
        path.lineTo(x+range, y-peak)
    elif dir=='West':
        path.lineTo(x+peak, y-range)
        path.lineTo(x+peak, y+range)
    elif dir=='East':
        path.lineTo(x-peak, y-range)
        path.lineTo(x-peak, y+range)
    path.lineTo(x, y)
    painter.drawPath(path)
