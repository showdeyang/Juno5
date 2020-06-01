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
from tkintertable import TableCanvas, TableModel
path = Path('./')
APP_TITLE = '工艺建模'
APP_ICON = (path / 'assets' / 'juneng.png').absolute()
if platform.system() == 'Windows':
    font = '微软雅黑'
else:
    font = 'Lucida Grande'

def alwaysActiveStyle(widget):
    widget.config(state="active")
    widget.bind("<Leave>", lambda e: "break")
    
class Window(ttk.Frame):
 
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        #####################################
        #Main Layout
        self.master = master
        
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack()
        
        
        self.configWidget = tk.Frame(self.master)
        self.configWidget.pack(side='top')
        self.notebook.add(self.configWidget, text='定义与配置')
        
        self.trainingWidget = tk.Frame(self.master)
        self.trainingWidget.pack(side='top')
        self.notebook.add(self.trainingWidget, text='数据建模')
        
        self.applicationWidget = tk.Frame(self.master)
        self.applicationWidget.pack(side='top')
        self.notebook.add(self.applicationWidget, text='进出水预测（应用）')
        
        self.dataWidget = tk.Frame(self.master)
        self.dataWidget.pack(side='top')
        self.notebook.add(self.dataWidget, text='历史数据')
        
        self.topBar = tk.Frame(self.configWidget, relief='flat', bd=1)
        self.topBar.pack(side='top', fill='x')
        
        self.body = tk.Frame(self.configWidget)
        self.body.pack(side='top', fill='both')
        
        self.statusBar = tk.Frame(master=self.master, relief='sunken', bd=1)
        self.statusBar.pack(side='bottom', fill='x')
        self.status = tk.Label(master=self.statusBar, text='请选择模型')
        self.status.pack(side='left')
        
        ########################################################################
        #Topbar layout
        self.createModelButton = ttk.Button(self.topBar, text='添加新工艺', command=self.createNewModel)
        self.createModelButton.pack(side='left')
        
        self.removeModelButton = ttk.Button(self.topBar, text='删除工艺', command=self.removeModel)
        self.removeModelButton.pack(side='left')
        
        self.createFeatureButton = ttk.Button(self.topBar, text='添加指标', command=self.createFeature)
        self.createFeatureButton.pack(side='left')
        
        self.removeFeatureButton = ttk.Button(self.topBar, text='删除指标', command=self.removeFeature)
        self.removeFeatureButton.pack(side='left')

        #self.modelName = tk.StringVar(self.master)
        self.modelName = None

        self.features = json.loads(open(path / 'config'/'features.json','r').read())
        self.treatments = json.loads(open(path / 'config'/ 'treatments.json','r').read())
        

        
        self.cb = tk.Frame(self.topBar)
        self.cb.pack(side='left',expand=True)
        
        self.combokey = tk.Label(self.cb, text='当前工艺：')
        self.combokey.pack(side='left')
        
        self.combo = ttk.Combobox(self.cb, values=['请选择模型'] + self.treatments)
        self.combo.pack(side='left')
        self.combo.current(0)
        self.combo.bind("<<ComboboxSelected>>", self.loadModel)
        
        # self.modelOptions = ttk.OptionMenu(self.cb, self.modelName, '请选择模型', *self.treatments, command=self.loadModel)
        # self.modelOptions.configure(width=max([len(e) for e in self.treatments])+5)
        # alwaysActiveStyle(self.modelOptions)
        
        # self.modelOptions.pack(side='left')
        
        ###################################################################
        #Body Layout
        self.box = tk.Frame(self.body)
        self.box.pack(side='top', fill='x', expand=True)
        
        row1 = tk.Frame(self.body)
        row1.pack(side='top', fill='x', expand=True)
        self.about = tk.Label(row1,text='Juno AI 污水处理工艺建模', justify='left', font=(font, 15))
        self.about.pack(side='left')
        
        row2 = tk.Frame(self.body)
        row2.pack(side='top', fill='x', expand=True)
        self.modelTitle = tk.Label(row2,text=self.modelName, font=(font, 20))
        self.modelTitle.pack(side='left')
        
        ############################################################
        #Optimality Widget
        self.optFrame = tk.Frame(self.body)
        self.optFrame.pack(side='top', expand=False, fill='both')
        
        self.optFrameLabel = ttk.Label(self.optFrame, text='最优运行条件配置', font=(font, 13))
        self.optFrameLabel.pack(side='top')
        
        self.optTable = ttk.Frame(self.optFrame)
        self.optTable.pack(side='top')
        
        optEntries = []
        depVarBtns = []
        headers = ['污水特征','最低值*','最高值*','依赖特征']
        width = 20
        for i in range(len(self.features)+1):
            if i == 0:
                row = tk.Frame(self.optTable)
                row.pack(side='top', fill='x', expand=True)
                #this is the headers row
                for header in headers:
                    if header != headers[-1]:
                        label = tk.Label(row, text=header, width=width, fg='white', bg='seagreen')
                        label.pack(side='left')
                    else:
                        frame = tk.Frame(row, bg='cornflowerblue')
                        frame.pack(side='left', expand=True, fill='x')
                        label = tk.Label(frame, text=header, width=width, fg='white', bg='cornflowerblue')
                        label.pack()
            else:
                row = tk.Frame(self.optTable, bd=1)
                row.pack(side='top')
                
                label = tk.Label(row, text=self.features[i-1], width=width)
                label.pack(side='left')
                
                optRow = []
                btns = []
                for j in range(2):
                    e = tk.Entry(row, width=width, relief='groove', bg='#fefefe',bd=1, justify='right')
                    e.pack(side='left')
                    optRow.append(e)
                
                for feature in self.features:
                        btn = tk.Button(row, text=feature, font=(font, 7), relief='flat', bg='white', fg='dark grey', width=10, bd=1, cursor='hand2')

                        btn.configure(command=partial(self.selectBtn, btn))
                        btn.pack(side='left')
                        btn.clicked = False
                        if self.features.index(feature)+1 == i:
                            btn.configure(bg='tomato', fg='white')
                            btn.clicked = True
                        btns.append(btn)
                    
                optEntries.append(optRow)
                depVarBtns.append(btns)
#        How to insert data
#        optEntries[5][0].insert(tk.END,'Booty芝芝')
#        optEntries[3][1].insert(tk.END,'月音瞳')
        
        captionFrame = tk.Frame(self.optFrame)
        captionFrame.pack(side='top', fill='x')
        caption = tk.Label(self.optTable, text='\n注：*必填', font=(font, 9))
        caption.pack(side='left')
        

        ##################################
        #add buttons here for optimality Frame
        #######################################################################
        #training widget
        self.trainingTitle = tk.Label(self.trainingWidget, text='训练数据')
        self.trainingTitle.pack(side='top')
        #training table, input and output
        #graph
        #buttons
        
        #################################################
        #application
        self.applicationTitle = tk.Label(self.applicationWidget, text='实际应用')
        self.applicationTitle.pack(side='top')
        #input output table
        #buttons
        
        ###############################################
        #data widget
        self.dataTitle = tk.Label(self.dataWidget, text='历史数据 在此游览')
        self.dataTitle.pack(side='top')
        #show data table
        #buttons
        
        #福利
        maxwidth = 1000
        maxheight = 1000
        button = ttk.Button(self.dataWidget, text='换一张福利图', command=self.changePic)
        button.pack(side='top')
        pics = glob.glob(str(path / 'assets' / 'res'/ '*'))
        pic = random.choice(pics)
        imgpath = pic
        img = Image.open(imgpath)
        ratio = min(maxwidth/img.size[0], maxheight/img.size[1])
        #wpercent = (basewidth/float(img.size[0]))
        #hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((int(img.size[0]*ratio),int(img.size[1]*ratio)), Image.ANTIALIAS)
        
        self.canvas = tk.Canvas(self.dataWidget, height=1000, width=1000) 
        self.img = ImageTk.PhotoImage(img)  
        self.canvas.create_image(0,0,anchor='nw',image=self.img)  
        self.canvas.pack(expand=True) 
        
    def changePic(self):
        maxwidth = 1000
        maxheight = 1000
        button = ttk.Button(self.dataWidget, text='换一张福利图', command=self.changePic)
        button.pack(side='top')
        pics = glob.glob(str(path / 'assets' / 'res'/ '*'))
        pic = random.choice(pics)
        imgpath = pic
        img = Image.open(imgpath)
        ratio = min(maxwidth/img.size[0], maxheight/img.size[1])
        #wpercent = (basewidth/float(img.size[0]))
        #hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((int(img.size[0]*ratio),int(img.size[1]*ratio)), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img)  
        self.canvas.create_image(0,0, anchor='nw', image=self.img)  
        
    def selectBtn(self, btn):
        if not btn.clicked:
            btn.configure(bg='tomato', fg='white')
            btn.clicked = True
        else:
            btn.configure(bg='white', fg='dark grey')
            btn.clicked = False

        
    def createNewModel(self):
        return
    
    def removeModel(self):
        return
    
    def createFeature(self):
        return
    
    def removeFeature(self):
        return
    
    def loadModel(self,event=1):
        #print(self.modelName.get())
        if self.combo.get() != '请选择模型':
            self.modelName = self.combo.get()
            print(self.modelName)
            self.modelTitle.configure(text=self.modelName)
        else:
            self.modelName = ''
            self.modelTitle.configure(text=self.modelName)
        return
    
    def cell_select(self, response):
        print (self.sheet.get_selected_cells())
        print (self.sheet.get_cell_data(*list(self.sheet.get_selected_cells())[0]))
        
        

    
if __name__ == "__main__":
    root = tk.Tk()
    #root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=APP_ICON))
#    s = ttk.Style(root)
#    s.theme_use('clam')
    #s.configure('raised.TMenubutton', borderwidth=1, state='disabled')

    #s=ttk.Style()
    #s.configure('W.TButton',font=("Microsoft YaHei",10))
    # s.theme_use('vista')
    s = ttk.Style()
    s.configure('TNotebook.Tab', width=20, padding=(5, 5))
    s.configure('TNotebook', tabmargins = (2, 10, 0, 0))

    app = Window(root)
    if platform.system() == 'Windows':
        root.wm_state("zoomed")
    else:
        root.wm_attributes('-zoomed',1)
    root.tk_setPalette(background='#F2F1F0', foreground='#32322D')
    #set window title
    root.wm_title(APP_TITLE)
    root.geometry('900x850')
    #show window
    root.mainloop()