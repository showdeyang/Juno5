# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from PIL import ImageTk, Image
import random
import glob
import platform

path = Path('./')
APP_TITLE = '福利图库'

if platform.system() == 'Windows':
    font = '微软雅黑'
else:
    font = 'Lucida Grande'
    
class Window(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        ##Easter Egg
        self.maxwidth = 1500
        self.maxheight = 800

        pics = glob.glob(str(path / 'assets' / 'res'/ '*'))
        #pics = glob.glob('D:\\Restricted\\miscp\\*')
        pic = random.choice(pics)
        imgpath = pic
        img = Image.open(imgpath)
        ratio = min(self.maxwidth/img.size[0], self.maxheight/img.size[1])
        #wpercent = (basewidth/float(img.size[0]))
        #hsize = int((float(img.size[1])*float(wpercent)))
        imgWidth, imgHeight = int(img.size[0]*ratio), int(img.size[1]*ratio)
        #print(imgWidth, imgHeight)
        img = img.resize((imgWidth, imgHeight), Image.ANTIALIAS)
    
        self.canvas = tk.Canvas(self.master, height=self.maxheight, width=self.maxwidth) 
        self.img = ImageTk.PhotoImage(img)  
        self.canvas.create_image(int((self.maxwidth-imgWidth)/2),int((self.maxheight-imgHeight)/2),anchor='nw',image=self.img)  
        self.canvas.pack(expand=True) 
        self.canvas.bind('<Right>',self.changePicByKey)
        self.canvas.focus_set()
        button = ttk.Button(self.master, text='换一张福利图', command=self.changePic)
        button.pack(side='bottom')
        
    def changePicByKey(self, event):
        self.changePic()
        #print('triggered')
    
    def changePic(self):
    #        maxwidth = 700
    #        maxheight = 700
        #pics = glob.glob('D:\\Restricted\\miscp\\*')
        #print(len(pics))
        pics = glob.glob(str(path / 'assets' / 'res'/ '*'))
        pic = random.choice(pics)
        imgpath = pic
        img = Image.open(imgpath)
        ratio = min(self.maxwidth/img.size[0], self.maxheight/img.size[1])
        #wpercent = (basewidth/float(img.size[0]))
        #hsize = int((float(img.size[1])*float(wpercent)))
        imgWidth, imgHeight = int(img.size[0]*ratio), int(img.size[1]*ratio)
        #print(imgWidth, imgHeight)
        img = img.resize((imgWidth, imgHeight), Image.ANTIALIAS)
    
        self.img = ImageTk.PhotoImage(img)  
        self.canvas.create_image(int((self.maxwidth-imgWidth)/2),int((self.maxheight-imgHeight)/2),anchor='nw',image=self.img)  
        self.canvas.focus_set()
        
if __name__ == "__main__":
    root = tk.Tk()
    
    app = Window(root)
#    if platform.system() == 'Windows':
#        root.wm_state("zoomed")
#    else:
#        root.wm_attributes('-zoomed',1)
    root.tk_setPalette(background='#000000', foreground='#32322D')
    #set window title
    root.wm_title(APP_TITLE)
    root.geometry('1550x850')
    #show window
    root.mainloop()