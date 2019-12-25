from PIL import ImageGrab 
from ctypes import *
import time
import winsound
#import win32api
#import win32con
#import win32gui

IMAGE_START_INDEX = 1
IMAGE_DIR = "3"
IMAGE_x = 194
IMAGE_y = 0
IMAGE_width  = 760
IMAGE_height = 760


#def mouse_click(x=None,y=None):
#	if not x is None and not y is None:
#		windll.user32.SetCursorPos(x, y)
#		time.sleep(0.05)
#	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
#	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
#	time.sleep(0.05)


def grabImage(dir, index):
	img = ImageGrab.grab((IMAGE_x,IMAGE_y,IMAGE_x+IMAGE_width,IMAGE_y+IMAGE_height))
	if img != None:
		img.save(dir+"\\"+"%04d"%index+'.jpg')
	winsound.PlaySound('Camera.wav', winsound.SND_FILENAME)

def grab1d2d():
	index = IMAGE_START_INDEX
	while(index <= 2500):
		print (index)
		grabImage(IMAGE_DIR, index)
		#mouse_click(1571,707)
		time.sleep(1.5)
		index += 1
time.sleep(5)
grab1d2d()
