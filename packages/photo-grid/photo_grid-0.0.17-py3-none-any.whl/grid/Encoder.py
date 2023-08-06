import sys, os
import numpy as np
import pandas as pd
import rasterio
from urllib.request import urlopen
import matplotlib.pyplot as plt
# 
os.chdir(os.path.expanduser("~")+"/Dropbox/photo_grid/")

nameImg = "data/Plains 7-11-18 LL crop_modified.tif"
os.listdir('data')
img = rasterio.open(nameImg)

img.name
img.mode
img.count
img.width
img.height
img.dtypes
img.bounds
img.crs
img.indexes

nCh = img.count
npImg = np.zeros((img.height, img.width, img.count), dtype="uint8")
for i in range(img.count):
    npImg[:, :, i] = img.read(i+1)

plt.imshow(npImg)

npImg.astype(np.uint8).mean()

npImg.mean()

plt.imshow(npImg.astype(np.uint8)[3000:4000, 3000:4000, :])
