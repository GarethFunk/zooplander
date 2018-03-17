#from scipy.ndimage import imread
#import cv2
#im = cv2.imread("..\W12.gif")
#print(im)
#import matplotlib.image as mpimg
#
#img = mpimg.imread('..\W12.gif')
##print(imread('..\W12.gif'))
import numpy as np
from PIL import Image

img = Image.open('..\W12.gif')
try:
    data = np.asarray( img, dtype='uint8' )
except SystemError:
    data = np.asarray( img.getdata(), dtype='uint8' )