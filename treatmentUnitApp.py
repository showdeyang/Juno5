# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
import win32api
import sys, os
import json
from tksheet import Sheet

path = Path('./')
APP_TITLE = '工艺建模'
APP_ICON = str(path / 'assets' / 'logo.ico')

def alwaysActiveStyle(widget):
    widget.config(state="active")
    widget.bind("<Leave>", lambda e: "break")
    
class Window(ttk.Frame):
 
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        #####################################
        #Main Layout
        self.master = master
        self.topBar = tk.Frame(self.master, relief='raised', bd=1)
        self.topBar.pack(side='top', fill='x')
        
        self.body = tk.Frame(self.master)
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
        self.box.pack(side='top')
        
        self.about = tk.Label(self.box,text='Juno AI 污水处理工艺建模', justify='left')
        self.about.pack(side='top')
        
        self.modelTitle = tk.Label(self.box,text=self.modelName, justify='left')
        self.modelTitle.pack(side='top')
        
        self.Button = ttk.Button(self.box,text='分析数据')
        self.Button.pack(side='bottom')
        
        
        
        self.sheet = Sheet(self.box, data = [[1,2,3,4,5], [1,2,3]], headers = self.treatments,row_index = self.features, theme='light',set_all_heights_and_widths = True, total_rows = 7, header_height = "3", total_columns=9, height=500, width=1500)
        self.sheet.set_all_cell_sizes_to_text()
        self.sheet.enable_bindings("enable_all")
        self.sheet.pack(side='bottom')
        self.sheet.extra_bindings([("cell_select", self.cell_select)])
        
        
        
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
    root.iconbitmap(APP_ICON)
    #s = ttk.Style(root)
    #s.theme_use('clam')
    #s.configure('raised.TMenubutton', borderwidth=1, state='disabled')

    #s=ttk.Style()
    #s.configure('W.TButton',font=("Microsoft YaHei",10))
    # s.theme_use('vista')
    app = Window(root)
    root.wm_state("zoomed")
    #set window title
    root.wm_title(APP_TITLE)
    root.geometry('900x350')
    #show window
    root.mainloop()