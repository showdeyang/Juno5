# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from PIL import ImageTk, Image
#import win32api
import glob
import platform
import sys, os
import random
import json
from functools import partial
#from tksheet import Sheet
#from tkintertable import TableCanvas, TableModel
#from MyWidgets import ScrolledWindow

path = Path('./')
APP_TITLE = '专家数据建模'
APP_ICON = (path / 'assets' / 'juneng.png').absolute()
if platform.system() == 'Windows':
    font = '微软雅黑'
else:
    font = 'Lucida Grande'

class Window(tk.Frame):
    def __init__(self, master=None, modelName=None, statusLabel=None, modelCombobox=None):

        tk.Frame.__init__(self, master)
        
        self.master = master
        
        emptyFrame = tk.Frame(self.master, height=15)
        emptyFrame.pack(side='top')
        
        self.modelName = modelName
        self.features = json.loads(open(path / 'config'/'features.json','r').read())
        self.treatments = json.loads(open(path / 'config'/ 'treatments.json','r').read())
        
        if not modelCombobox:
            self.row = tk.Frame(self.master)
            self.row.pack(side='top')
            
            self.cb = tk.Frame(self.row)
            self.cb.pack(side='top')
            
            self.combokey = tk.Label(self.cb, text='当前污水处理工艺：')
            self.combokey.pack(side='left')
            
            self.combo = ttk.Combobox(self.cb, values=['请选择模型'] + self.treatments)
            self.combo.pack(side='left')
            self.combo.current(0)
            self.combo.bind("<<ComboboxSelected>>", self.loadModel)
        else:
            self.combo = modelCombobox
            self.combo.bind("<<ComboboxSelected>>", self.loadModel)
        
        self.body = tk.Frame(self.master)
        #self.body.pack(side='top')
        
        self.titleLabel = ttk.Label(self.body, text='\n'+APP_TITLE+'\n', font=(font, 13))
        self.titleLabel.pack(side='top')
        
        ###########################
        #TABLE
        self.LEFT = tk.Frame(self.body)
        self.LEFT.pack(side='left')
        
        self.table = tk.Frame(self.LEFT)
        self.table.pack(side='top')
        
        self.data = None
        self.entries = []
        
        self.headers = ['污水指标','输入进水','机器预测出水','专家反馈','误差（%）']
        self.widths = (20,15,15,15,10)
        row = tk.Frame(self.table)
        row.pack(side='top')
        for j, header in enumerate(self.headers):
            if j == 0:
                frame = tk.Frame(row)
                frame.configure(width=self.widths[j])
                frame.pack(side='left')
                e = tk.Entry(frame, disabledforeground='#fffffe', disabledbackground='darkslategray', relief='flat', width=self.widths[j]+3, bd=1)
                e.insert(tk.END, header)
                e.configure(state='disabled')
                e.pack(side='left')
            else:

                e = tk.Entry(row, disabledforeground='#fffffe', disabledbackground='slategray', bd=1, relief='flat', width=self.widths[j], justify='center')
                e.insert(tk.END, header)
                e.configure(state='disabled')
                e.pack(side='left')
            
            if header in ['输入进水','专家反馈']:
                #change color to indicate editable.
                e.configure(disabledbackground='lightslategray')
            
        #self.fixedVars = []
        for i, feature in enumerate(self.features):
            row = tk.Frame(self.table)
            row.pack(side='top')
            entryRow = []
            for j, width in enumerate(self.widths):
                if j == 0:
                    frame = tk.Frame(row, width=width)
                    frame.pack(side='left')
                    var = tk.IntVar()
                    #self.fixedVars.append(var)
                    checkBtn = ttk.Checkbutton(frame, variable=var, text=feature, width=width, onvalue=1, offvalue=0, cursor='hand2')
                    checkBtn.pack()
                    entryRow.append(var)
                else:
                    e = tk.Entry(row, disabledforeground='black', disabledbackground='mistyrose', relief='flat', width=width, cursor='arrow', justify='right')
                    e.pack(side='left')
                    e.insert(tk.END,'haha')
                    e.configure(state='disabled')
                    entryRow.append(e)
                    
                    if self.headers[j] in ['输入进水','专家反馈']:
                        e.configure(state='normal', relief='flat', fg='darkslategray', bg='#fffffe', cursor='xterm')
            self.entries.append(entryRow)

        
        ##########################################
        #BUTTONS
        emptyFrame = tk.Frame(self.LEFT, height=20)
        emptyFrame.pack(side='top')
        
        self.buttons = tk.Frame(self.LEFT)
        self.buttons.pack(side='top', fill='x')
        
        self.autoFillBtn = ttk.Button(self.buttons, text='随机填充', command=self.autoFill)
        self.autoFillBtn.pack(side='left')
        
        self.clearBtn = ttk.Button(self.buttons, text='清空输入', command=self.clearEntries)
        self.clearBtn.pack(side='left')
        
        self.predictBtn = ttk.Button(self.buttons, text='预测出水', command=self.predict)
        self.predictBtn.pack(side='left')
        
        self.trainBtn = ttk.Button(self.buttons, text='提交反馈', command=self.train)
        self.trainBtn.pack(side='left')
        
        if not statusLabel:
            self.statusBar = tk.Frame(master=self.master, relief='sunken', bd=1)
            self.statusBar.pack(side='bottom', fill='x')
    
            self.status = tk.Label(master=self.statusBar, text='请选择模型')
            self.status.pack(side='left')
            
        else:
            self.status = statusLabel
    
        #########################################
        #Training Graph Image
        
        self.RIGHT = tk.Frame(self.body)
        self.RIGHT.pack(side='right', fill='both', expand=True)
    ########################################################    
    #     ##Easter Egg
        self.maxwidth = 450
        self.maxheight = 450
        #self.dataWidget.bind('<Button-1>',self.changePicByKey)
        #self.dataWidget.focus_set()

        pics = glob.glob(str(path / 'assets' / 'res'/ '*'))
        pic = random.choice(pics)
        imgpath = pic
        img = Image.open(imgpath)
        ratio = min(self.maxwidth/img.size[0], self.maxheight/img.size[1])
        #wpercent = (basewidth/float(img.size[0]))
        #hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((int(img.size[0]*ratio),int(img.size[1]*ratio)), Image.ANTIALIAS)
    
        self.canvas = tk.Canvas(self.RIGHT, height=self.maxheight, width=self.maxwidth) 
        self.img = ImageTk.PhotoImage(img)  
        self.canvas.create_image(0,0,anchor='nw',image=self.img)  
        self.canvas.pack(expand=True) 
        self.canvas.bind('<Right>',self.changePicByKey)
        
        button = ttk.Button(self.RIGHT, text='换一张福利图', command=self.changePic)
        button.pack(side='bottom')
        
    def changePicByKey(self, event):
        self.changePic()
        #print('triggered')
    
    def changePic(self):
    #        maxwidth = 700
    #        maxheight = 700
        pics = glob.glob('D:\\Restricted\\miscp\\*')
        #print(len(pics))
        #pics = glob.glob(str(path / 'assets' / 'res'/ '*'))
        pic = random.choice(pics)
        imgpath = pic
        img = Image.open(imgpath)
        ratio = min(self.maxwidth/img.size[0], self.maxheight/img.size[1])
        #wpercent = (basewidth/float(img.size[0]))
        #hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((int(img.size[0]*ratio),int(img.size[1]*ratio)), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img)  
        self.canvas.create_image(0,0, anchor='nw', image=self.img)  
        self.canvas.focus_set()
    ####################################################
    def loadModel(self, event=1):
        self.modelName = self.combo.get()
        if self.modelName == '请选择模型':
            self.modelName = None
            self.status.configure(text='请选择模型！')
            self.body.pack_forget()
            return
        else:
            self.body.pack(side='top')
        
        
        
        ...
        
    def autoFill(self, event=11):
        ...
    
    def clearEntries(self, event=1):
        ...
        
    def predict(self, event=1):
        ...
    
    def train(self, event=1):
        ...
            
if __name__ == "__main__":
    root = tk.Tk()
    
    app = Window(root)
#    if platform.system() == 'Windows':
#        root.wm_state("zoomed")
#    else:
#        root.wm_attributes('-zoomed',1)
    root.tk_setPalette(background='#F2F1F0', foreground='#32322D')
    #set window title
    root.wm_title(APP_TITLE)
    root.geometry('1000x850')
    #show window
    root.mainloop()