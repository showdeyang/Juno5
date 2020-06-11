# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from pathlib import Path
#from PIL import ImageTk, Image
#import win32api
import glob
import platform
import os
import random
import json
from functools import partial
import treatmentEffect as te
import fewShotsLearning as fsl
import wastewater as ww
#import numpy as np
#import matplotlib.pyplot as plt
import csv
import time

path = Path('./')
APP_TITLE = '历史数据'
APP_ICON = (path / 'assets' / 'juneng.png').absolute()

if platform.system() == 'Windows':
    font = '微软雅黑'
    newline = ''
    encoding = 'gbk'
else:
    font = 'Lucida Grande'
    newline = '\n'
    encoding = 'utf-8'
    
class Window(tk.Frame):
    def __init__(self, 
                 master=None, 
                 modelName=None, 
                 statusLabel=None, 
                 modelCombobox=None):

        tk.Frame.__init__(self, master)
        
        if not os.path.isdir(path / 'output'):
            os.mkdir(path / 'output')
        
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
        
        previewFrame = tk.Frame(self.body)
        previewFrame.pack(side='top')
        previewLabel = tk.Label(previewFrame, text='数据预览')
        previewLabel.grid(row=0,column=0, sticky='nsew')
        #print(previewFrame)
        self.previewPane = tk.Text(previewFrame, width=100, height=20, bg='#fffffe')
        self.previewPane.insert(tk.END,'正在加载数据...')
        self.previewPane.configure(state='disabled')
        self.previewPane.grid(row=1, column=0, sticky='nsew')
        
        vsb = ttk.Scrollbar(previewFrame, command=self.previewPane.yview)
        vsb.grid(row=1, column=1, sticky='nsew')
        
        self.previewPane.configure(yscrollcommand=vsb.set)
        
        emptyFrame = tk.Frame(self.body, height=20)
        emptyFrame.pack(side='top')
        
        buttons = tk.Frame(self.body)
        buttons.pack(side='top')
        
        exportBtn = ttk.Button(buttons, text='导出CSV', command=self.exportData)
        exportBtn.pack(side='left')
        
        importBtn = ttk.Button(buttons, text='导入CSV', command=self.importData)
        importBtn.pack(side='left')
        
        emptyFrame = tk.Frame(self.body, height=20)
        emptyFrame.pack(side='top')
        
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
        
        ###########################
        
    def loadModel(self, event=1):
        
        self.modelName = self.combo.get()
        if self.modelName == '请选择模型':
            self.modelName = None
            self.status.configure(text='请选择模型！')
            self.body.pack_forget()
            return
        else:
            #check if model data exists. If yes, show buttons for data operations.
            dataFile = self.modelName + '.data.json'
            if not os.path.isdir(path / 'models' / self.modelName):
                self.status.configure(text='错误：模型未被定义！')
                self.body.pack_forget()
                return
            
            elif not glob.glob(str((path / 'models' / self.modelName / '*.model').absolute())):
                self.status.configure(text='错误：模型虽已被定义，但未被训练！所以没有产生数据')
                self.body.pack_forget()
                return
            
            elif not os.path.isfile(path / 'models' / self.modelName / dataFile):
                self.status.configure(text='错误：模型虽已被定义和训练，但是数据缺失！')
                self.body.pack_forget()
                return
            
            self.body.pack(side='top')
            self.status.configure(text='正常')
            
            preview = json.loads(open(path / 'models' / self.modelName / dataFile, 'r').read())
            self.data = preview
            self.previewPane.configure(state='normal')
            self.previewPane.delete(1.0, tk.END)
            self.previewPane.insert(tk.END, preview)
            self.previewPane.configure(state='disabled')
        ...
        
    def exportData(self, event=1):
        timestamp = ('').join(str(time.time()).split('.'))
        
        X = self.data['X']
        Y = self.data['Y']
        
        rows = []
        rows.append(['id','输入输出类'] + list(X[0].keys()))
        for i, x in enumerate(X):
            row1 = [i+1, '进水'] + list(x.values())
            row2 = [i+1, '出水'] + list(Y[i].values())
            rows.append(row1)
            rows.append(row2)
            
        #print(rows)
         
        file = self.modelName + timestamp + '.csv'
        csvwriter = csv.writer(open(path / 'output' / file, 'w', encoding=encoding, newline=newline), dialect='excel')
        csvwriter.writerows(rows)
        self.status.configure(text='成功！已导出数据到 output 文件夹里！')
        ...
        
    def importData(self, event=1):
        #file dialog to accept file.
        filename =  filedialog.askopenfilename(initialdir = path,title = "选择导入表格文件",filetypes = (("CSV表格","*.csv"),("所有文件","*.*")))
        print(filename) 
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