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
import treatmentEffect as te
import fewShotsLearning as fsl
import wastewater as ww
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
    def __init__(self, 
                 master=None, 
                 modelName=None, 
                 statusLabel=None, 
                 modelCombobox=None):

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
            
            self.combo = ttk.Combobox(self.cb, 
                                      values = ['请选择模型'] + self.treatments)
            self.combo.pack(side='left')
            self.combo.current(0)
            self.combo.bind("<<ComboboxSelected>>", self.loadModel)
        else:
            self.combo = modelCombobox
            self.combo.bind("<<ComboboxSelected>>", self.loadModel)
        
        self.body = tk.Frame(self.master)
        #self.body.pack(side='top')
        
        self.titleLabel = ttk.Label(self.body, 
                                    text='\n'+APP_TITLE+'\n', 
                                    font=(font, 13))
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
                e = tk.Entry(frame, 
                             disabledforeground='#fffffe', 
                             disabledbackground='darkslategray', 
                             relief='flat', 
                             width=self.widths[j]+3,
                             bd=1)
                e.insert(tk.END, header)
                e.configure(state='disabled')
                e.pack(side='left')
            else:

                e = tk.Entry(row,
                             disabledforeground='#fffffe', 
                             disabledbackground='slategray', 
                             bd=1, relief='flat', 
                             width=self.widths[j], 
                             justify='center')
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
                    checkBtn = ttk.Checkbutton(frame, 
                                               variable=var, 
                                               text=feature, width=width, 
                                               onvalue=1, offvalue=0, 
                                               cursor='hand2')
                    checkBtn.pack()
                    entryRow.append(var)
                else:
                    e = tk.Entry(row, 
                                 disabledforeground='black', 
                                 disabledbackground='mistyrose', 
                                 relief='flat', 
                                 width=width, 
                                 cursor='arrow', 
                                 justify='right')
                    e.pack(side='left')
                    #e.insert(tk.END,'haha')
                    e.configure(state='disabled')
                    entryRow.append(e)
                    
                    if self.headers[j] in ['输入进水','专家反馈']:
                        e.configure(state='normal', 
                                    relief='flat', 
                                    fg='darkslategray', 
                                    bg='#fffffe', 
                                    cursor='xterm')
                    if self.headers[j] == '专家反馈':
                        #bind keyup event to compute error
                        e.bind('<KeyRelease>', self.calcError)
            self.entries.append(entryRow)

        
        ##########################################
        #BUTTONS
        emptyFrame = tk.Frame(self.LEFT, height=20)
        emptyFrame.pack(side='top')
        
        self.buttons = tk.Frame(self.LEFT)
        self.buttons.pack(side='top', fill='x')
        
        self.autoFillBtn = ttk.Button(self.buttons, 
                                      text='随机填充', 
                                      command=self.autoFill)
        self.autoFillBtn.pack(side='left')
        
        self.clearBtn = ttk.Button(self.buttons, 
                                   text='清空输入', 
                                   command=self.clearEntries)
        self.clearBtn.pack(side='left')
        
        self.predictBtn = ttk.Button(self.buttons, 
                                     text='预测出水', 
                                     command=self.predict)
        self.predictBtn.pack(side='left')
        
        self.trainBtn = ttk.Button(self.buttons, 
                                   text='提交反馈', 
                                   command=self.train)
        self.trainBtn.pack(side='left')
        
        if not statusLabel:
            self.statusBar = tk.Frame(master=self.master, 
                                      relief='sunken', 
                                      bd=1)
            self.statusBar.pack(side='bottom', fill='x')
    
            self.status = tk.Label(master=self.statusBar, 
                                   text='请选择模型')
            self.status.pack(side='left')
            
        else:
            self.status = statusLabel
    
        #########################################
        #Right Panel
        emptyFrame = tk.Frame(self.body, width=20)
        emptyFrame.pack(side='left')
        self.RIGHT = tk.Frame(self.body, width=500, height=500, bg='white' )
        self.RIGHT.pack(side='right', fill='both', expand=True)
        
        
        descBox = tk.Frame(self.RIGHT, bg='white')
        descBox.pack(side='top', fill='x', expand=True)
        self.roundLabel = tk.Label(self.RIGHT, text='训练回合：0', bg='white', font=('monospace'), justify='left')
        self.roundLabel.pack(side='top', fill='x')
        
        self.errorLabel = tk.Label(self.RIGHT, text='预测误差：0%', bg='white', font=('monospace'))
        self.errorLabel.pack(side='top')

    ########################################################    
        #Training Image Graph
        self.maxwidth = 400
        self.maxheight = 400
        
        self.canvas = tk.Canvas(self.RIGHT, height=self.maxheight, width=self.maxwidth, bg='white') 
        #self.img = ImageTk.PhotoImage(img)  
        #self.canvas.create_image(int((self.maxwidth-imgWidth)/2),int((self.maxheight-imgHeight)/2),anchor='nw',image=self.img)  
        self.canvas.pack(expand=True) 
        
    ####################################################
    def loadModel(self, event=1):
        self.modelName = self.combo.get()
        if self.modelName == '请选择模型':
            self.modelName = None
            self.status.configure(text='请选择模型！')
            self.body.pack_forget()
            return
        else:
            #check if model has been trained. If yes, load the model's past training history (to show historical errors graph on the right panel). If no, load a default image.
            if not os.path.isdir(path / 'models'/ self.modelName):
                self.status.configure(text='错误：该模型的最优运行条件还未被定义！')
                self.body.pack_forget()
                return
            
            elif not glob.glob(str((path / 'models'/ self.modelName /'*.model' ).absolute())):
                #model is not yet trained. Load up the opt file.
                self.opt = te.loadOpt(self.modelName)
                self.status.configure(text='最优运行条件已被加载。初次训练模型')
                self.body.pack(side='top')
                
                
                return
            
            else:
                #model has been trained before. Load up the historical error graph.
                #TO DO
                self.opt = te.loadOpt(self.modelName)
                self.status.configure(text='最优运行条件已被加载。模型曾经被训练过。')
                self.body.pack(side='top')
                
                #load past training data. TD.
                ...
            
            
                
                
            self.body.pack(side='top')
        
        
        
        ...
        
    def autoFill(self, event=11):
        x = ww.wastewater()
        x.generateFromOpt(self.opt)
        print(x.water)
        #insert generated water into table
        for i, feature in enumerate(self.features):
            value = x.water[feature]
            cell = self.entries[i][1]
            cellFixed = self.entries[i][0].get()
            if not cellFixed:
                cell.delete(0,tk.END)
                cell.insert(tk.END,round(value,1))

        ...
    
    def clearEntries(self, event=1):
        for i, feature in enumerate(self.features):
            cell = self.entries[i][1]
            cellFixed = self.entries[i][0]
            cell.delete(0,tk.END)
            cellFixed.set(0)
        ...
        
    def predict(self, event=1):
        #read input as x, then y = predict(x, modelname)
        x = {}
        for i, feature in enumerate(self.features):
            cellvalue = self.entries[i][1].get()
            try:
                x[feature] = float(cellvalue)
            except ValueError:
                self.status.configure(text='错误：' + feature + '输入必须是数字，不能为空')
                return
            
            #resetting cellFixed to 0
            cellFixed = self.entries[i][0]
            cellFixed.set(0)
        
        Ypred = fsl.predict(x, self.modelName)
        print('predicted',Ypred)
        
        #output value to table
        for i, feature in enumerate(self.features):
            cell = self.entries[i][2]
            cell.configure(state='normal')
            cell.delete(0, tk.END)
            cell.insert(tk.END, round(Ypred[feature],1))
            cell.configure(state='disabled')
            
            #############
            #feedback column
            cell = self.entries[i][3]
            cell.delete(0,tk.END)
            cell.insert(tk.END, round(Ypred[feature],1))
            
        ...
    
    def calcError(self, event=1):
        yactual, ypred = [],[]
        for i, feature in enumerate(self.features):
            cell = self.entries[i][3]
            yactual.append(float(cell.get()))
            
            cell = self.entries[i][2]
            ypred.append(float(cell.get()))
        error = fsl.computeError(ypred, yactual)
        print('error', error)
        
        #output error back into table
        for i, feature in enumerate(self.features):
            cell = self.entries[i][4]
            cell.configure(state='normal')
            cell.delete(0,tk.END)
            cell.insert(0,round(error[i],2))
            cell.configure(state='disabled')
        
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