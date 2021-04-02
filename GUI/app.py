import os, sys, pickle, datetime, configparser

import tkinter as tk
from tkinter import font as tf
from PIL import Image, ImageTk

from lotteryUI import lotteryUI


# Semi-Constants
APP_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(APP_PATH)

CONFIG = configparser.ConfigParser()
os.chdir(APP_PATH)
CONFIG.read('config.ini',encoding="utf-8-sig")
# Constants
APP_NAME = CONFIG['APP_CONFIG']['APP_NAME']
APP_SIZE = [int(x) for x in CONFIG['APP_CONFIG']['APP_SIZE'].split('x')]
FOOTER_ICON_FILENAME = CONFIG['APP_CONFIG']['APP_LOGO']

class app:
    def __init__(self):
        self.root = tk.Tk()
        self.TIME_FONT = tf.Font(family="Arial",size=27)
        self.init()
        self.root.mainloop()

    def init(self):
        #Create Window
        self.root.title(APP_NAME)
        self.setGeometry(APP_SIZE[0],APP_SIZE[1])
        self.root.minsize(APP_SIZE[0],APP_SIZE[1])
        #Load Resouces
        self.FOOTER_ICON_IMG = ImageTk.PhotoImage(Image.open(FOOTER_ICON_FILENAME))
        #Create Header
        self.MAIN_FRAME = lotteryUI(master = self.root,CONFIG=CONFIG,DATA_PATH=APP_PATH)
        self.MAIN_FRAME.pack(fill=tk.BOTH,expand=True)
        #Create Footer
        self.FOOTER_FRAME = tk.Frame(master = self.root,bg="#0059b3",height=40)
        self.FOOTER_FRAME.pack(side=tk.BOTTOM,fill=tk.X,expand=False)
        self.FOOTER_ICON = tk.Label(master=self.FOOTER_FRAME,bg=self.FOOTER_FRAME['bg'],image=self.FOOTER_ICON_IMG)
        self.FOOTER_ICON.pack(side=tk.RIGHT,padx=(0,20),expand=False)
        self.FOOTER_TIME = tk.Label(master=self.FOOTER_FRAME,bg=self.FOOTER_FRAME['bg'],text="初始化中",font=self.TIME_FONT)
        self.FOOTER_TIME.pack(side=tk.LEFT,padx=(40,0),pady=(15,25),expand=False)
        self.FOOTER_ICON.bind('<Double-Button-1>',self.setFullScreen)
        self.time_tick()
        self.root.update()
    
    def setGeometry(self,w=APP_SIZE[0],h=APP_SIZE[1],l=None,t=None):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        if l is None:
            l = (screen_width-w)/2
        if t is None:
            t = (screen_height-h)/2
        self.root.geometry('%dx%d+%d+%d'%(w,h,l,t))
    
    def setFullScreen(self,event):
        self.root.attributes('-fullscreen',not self.root.attributes('-fullscreen'))

    def time_tick(self):
        self.FOOTER_TIME.config(text=datetime.datetime.now().strftime("%H %M %S"))
        self.root.update()
        self.FOOTER_TIME.after(500,self.time_tock)
    def time_tock(self):
        self.FOOTER_TIME.config(text=datetime.datetime.now().strftime("%H:%M:%S"))
        self.root.update()
        self.FOOTER_TIME.after(500,self.time_tick)


if __name__ == "__main__":
    app = app()