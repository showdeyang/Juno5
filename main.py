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
from MyWidgets import ScrolledWindow
import configWidget

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
        #################################################
        #Menu bar
        menu = tk.Menu(self.master, tearoff=False, relief='raised')
        self.master.config(menu=menu)
        
        #SETTINGS MENU
        settingsMenu = tk.Menu(menu, tearoff=False, relief='raised')
        settingsMenu.add_command(label="创建工艺", command=self.createNewModel)
        settingsMenu.add_command(label="删除工艺", command=self.removeModel)
        settingsMenu.add_separator()
        settingsMenu.add_command(label="创建指标", command=self.createFeature)
        settingsMenu.add_command(label="删除指标", command=self.removeFeature)
        menu.add_cascade(label="设置", menu=settingsMenu)
        
        #ABOUT MENU
        aboutMenu = tk.Menu(menu, tearoff=False, relief='raised')
        aboutMenu.add_command(label="Juno简介", command=self.clickAbout)
        aboutMenu.add_command(label="帮助")
        menu.add_cascade(label="关于", menu=aboutMenu)
        
        ##############################################
        self.modelName = None
        self.features = json.loads(open(path / 'config'/'features.json','r').read())
        self.treatments = json.loads(open(path / 'config'/ 'treatments.json','r').read())
        
        self.header = tk.Frame(self.master)
        self.header.pack(side='top', fill='x')
        
        emptyFrame = tk.Frame(self.header, height=10)
        emptyFrame.pack(side='top')
        
        self.row1 = tk.Frame(self.header)
        self.row1.pack(side='top', fill='x', expand=True)
        
        emptyFrame = tk.Frame(self.header, height=10)
        emptyFrame.pack(side='top')
  
        self.row2 = tk.Frame(self.header)
        self.row2.pack(side='top', fill='x', expand=True)
        
        self.about = tk.Label(self.row1,text='JunoAI', font=(font, 15))
        self.about.pack()
        
        self.topBar = tk.Frame(self.row2, relief='flat', bd=0)
        self.topBar.pack(side='left', expand=True, fill='x')
        
        self.cb = tk.Frame(self.row2)
        self.cb.pack(side='right',fill='both', expand=True)
        
        self.combokey = tk.Label(self.cb, text='当前污水处理工艺：')
        self.combokey.pack(side='left')
        
        self.combo = ttk.Combobox(self.cb, values=['请选择模型'] + self.treatments)
        self.combo.pack(side='left')
        self.combo.current(0)
        #self.combo.bind("<<ComboboxSelected>>", self.loadModel)
        
        emptyFrame = tk.Frame(self.header, height=20)
        emptyFrame.pack(side='bottom')

        self.notebook = ttk.Notebook(self.master, width=1000, height=700)
        self.notebook.pack(side='top')#,fill='both'
        
#        self.configWidget = tk.Frame(self.master)
#        self.configWidget.pack(side='top')
        
        
        self.statusBar = tk.Frame(master=self.master, relief='sunken', bd=1)
        self.statusBar.pack(side='bottom', fill='x')
        
        self.status = tk.Label(master=self.statusBar, text='请选择模型')
        self.status.pack(side='left')
        
        self.configFrame = tk.Frame(self.notebook)
        self.configFrame.pack(side='top')
        
        self.configWidget = configWidget.Window(self.configFrame, statusLabel=self.status, modelCombobox=self.combo)
        self.configWidget.pack(side='top')
        self.notebook.add(self.configFrame, text='定义与配置')
        
        
        self.trainingWidget = tk.Frame(self.master)
        self.trainingWidget.pack(side='top')
        self.notebook.add(self.trainingWidget, text='数据建模')
        
        self.applicationWidget = tk.Frame(self.master)
        self.applicationWidget.pack(side='top')
        self.notebook.add(self.applicationWidget, text='进出水预测（应用）')
        
        self.dataWidget = tk.Frame(self.master)
        self.dataWidget.pack(side='top')
        self.notebook.add(self.dataWidget, text='历史数据')
        
#        for i in range(len(self.notebook.tabs())):
#            self.notebook.tab(i,state='disabled')
        self.body = tk.Frame(self.configWidget)
        self.body.pack(side='top', fill='both')
    
    def createNewModel(self, event=7):
        win1 = tk.Toplevel()
        win1.wm_title("添加新工艺")
        win1.geometry('300x100')
        win1.wm_attributes("-topmost", 1)
        emptyFrame = tk.Frame(win1, height=10)
        emptyFrame.pack(side='top')
        self.win1entry = ttk.Entry(win1)
        self.win1entry.insert(0,'新工艺名称')
        self.win1entry.pack(side='top')
        
        emptyFrame = tk.Frame(win1, height=10)
        emptyFrame.pack(side='top')
        
        button = ttk.Button(win1,text='添加', command=self.registerNewModel)
        button.pack()
        
        emptyFrame = tk.Frame(win1, height=10)
        emptyFrame.pack(side='top')
        
        self.win1Label = tk.Label(win1,text='')
        self.win1Label.pack(side='bottom')
        
    def registerNewModel(self, event=8):
        modelname = self.win1entry.get()
        with open(path / 'config'/ 'treatments.json','r') as f:
            treatments = json.loads(f.read())
            
        if modelname not in treatments:
            treatments.append(modelname)
        else:
            self.win1Label.configure(text='错误：模型' + modelname + '已经存在！')
            return
        
        with open(path / 'config' / 'treatments.json','w') as f:
            f.write(json.dumps(treatments))
        self.win1Label.configure(text='添加' + modelname + '模型成功!')
        self.treatments = json.loads(open(path / 'config'/ 'treatments.json','r').read())
        self.combo.configure(values=['请选择模型'] + self.treatments)
        
    def removeModel(self,event=9):
        self.win2 = tk.Toplevel()
        self.win2.wm_title("删除工艺")
        self.win2.geometry('300x100')
        self.win2.wm_attributes("-topmost", 1)
        
        self.treatments = json.loads(open(path / 'config'/ 'treatments.json','r').read())
        
        emptyFrame = tk.Frame(self.win2, height=10)
        emptyFrame.pack(side='top')
        
        self.win2option = ttk.Combobox(self.win2, values=['请选择模型'] + self.treatments)
        self.win2option.pack(side='top')
        self.win2option.current(0)
        
        emptyFrame = tk.Frame(self.win2, height=10)
        emptyFrame.pack(side='top')
        
        button = ttk.Button(self.win2,text='删除', command=self.deleteModel)
        button.pack(side='top')
        
        emptyFrame = tk.Frame(self.win2, height=10)
        emptyFrame.pack(side='top')
        self.win2Label = tk.Label(self.win2,text='注意：工艺以及相关模型删除后无法恢复！')
        self.win2Label.pack(side='bottom')
        
    def deleteModel(self,event=10):
        modelname = self.win2option.get()
        
        #print(modelname)
        with open(path / 'config'/'treatments.json','r') as f:
            treatments = json.loads(f.read())
        
        if modelname not in treatments:
            return
        
        treatments.remove(modelname)
        
        with open(path /'config'/ 'treatments.json','w') as f:
            f.write(json.dumps(treatments))
        
        print('treatments list updated!')
        if os.path.isdir(path / 'models'/ modelname):
            os.removedirs(path /'models' / modelname)
            
            print('model data removed!')
        self.win2Label.configure(text='模型' + modelname + '已被删除！')
        self.treatments = json.loads(open(path / 'config'/'treatments.json','r').read())
        self.win2option.configure(values=['请选择模型'] + self.treatments)
        self.win2option.current(0)
        self.combo.configure(values=['请选择模型'] + self.treatments)
        
    def createFeature(self,event=11):
        win3 = tk.Toplevel()
        win3.wm_title("添加新指标")
        win3.geometry('300x150')
        win3.wm_attributes("-topmost", 1)
        
        emptyFrame = tk.Frame(win3, height=10)
        emptyFrame.pack()
        
        self.win3entry = ttk.Entry(win3)
        self.win3entry.insert(0,'新指标名称')
        self.win3entry.pack()
        
        emptyFrame = tk.Frame(win3, height=10)
        emptyFrame.pack()
        
        button = ttk.Button(win3,text='添加', command=self.addFeature)
        button.pack()
        
        emptyFrame = tk.Frame(win3, height=10)
        emptyFrame.pack()
        self.win3Label = tk.Label(win3,text='输入新指标名称')
        self.win3Label.pack(side='bottom')
        
    def addFeature(self,event=12):
        self.features = json.loads(open(path / 'config'/ 'features.json','r').read())
        newFeature = self.win3entry.get()
        if newFeature in self.features:
            self.win3Label.configure(text='错误：指标' + newFeature + '已经存在！')
            return
        self.features.append(newFeature)
        with open(path / 'config'/'features.json','w') as f:
            f.write(json.dumps(self.features))
        print('features added!')
        self.win3Label.configure(text='指标' + newFeature + '已被添加！\n须重启软件后新指标才生效．')
        
    def removeFeature(self,event=13):
        self.win4 = tk.Toplevel()
        self.win4.wm_title("删除指标")
        self.win4.geometry('300x150')
        self.win4.wm_attributes("-topmost", 1)
        
        self.features = json.loads(open(path / 'config'/ 'features.json','r').read())
        
        emptyFrame = tk.Frame(self.win4, height=10)
        emptyFrame.pack()
        
        self.win4option = ttk.Combobox(self.win4, values=['请选择指标'] + self.features)
        self.win4option.pack(side='top')
        self.win4option.current(0)
        
        emptyFrame = tk.Frame(self.win4, height=10)
        emptyFrame.pack()
        
        button = ttk.Button(self.win4,text='删除', command=self.deleteFeature)
        button.pack(side='top')
        
        emptyFrame = tk.Frame(self.win4, height=10)
        emptyFrame.pack()
        
        self.win4Label = tk.Label(self.win4,text='注意：删除指标后须在软件重启后才能生效．\n那些以旧的指标建立的工艺模型可能会无法使用！')
        self.win4Label.pack(side='bottom')
        
        
    def deleteFeature(self, event=14):
        self.features = json.loads(open(path / 'config'/'features.json','r').read())
        featureName = self.win4option.get()
        if featureName not in self.features:
            return
        self.features.remove(featureName)
        with open(path / 'config'/'features.json','w') as f:
            f.write(json.dumps(self.features))
            
        print('feature removed')
        self.win4Label.configure(text='指标' + featureName + '已被删除！\n须重启软件使指标变更生效！')
        self.win4option.configure(values=['请选择模型'] + self.features)
        self.win4option.current(0)
        
#    def loadModel(self,event=1):
#        #print(self.modelName.get())
#        self.features = json.loads(open(path / 'config'/'features.json','r').read())
#        if self.combo.get() != '请选择模型':
#            self.modelName = self.combo.get()
#            print(self.modelName)
#            for i in range(len(self.notebook.tabs())):
#                self.notebook.tab(i,state='normal')
#                
#            
#            self.status.configure(text='请选择进入模块')
#            
#            #load the depvars model if it already exists, else it is created on the spot:
#            depvarFile = self.modelName + '.depVar.json'
#            if os.path.isfile(path / 'models' / self.modelName / depvarFile):
#                self.depVars = json.loads(open(path / 'models' / self.modelName / depvarFile,'r').read())
#                self.saved = True
#                self.savedBox.configure(bg='lime green')
#            else:
#                self.depVars = {feature: [feature] for feature in self.features}
#                self.saved = False
#                self.savedBox.configure(bg='red')
#    
#            #if opt model exists, load it
#            optFile = self.modelName + '.opt.json'
#            self.opt = []
#            if os.path.isfile(path / 'models' / self.modelName / optFile):
#                self.optDict = json.loads(open(path / 'models' / self.modelName / optFile,'r').read())
#                
#                for feature in self.optDict:
#                    vec = [self.optDict[feature]['min'], self.optDict[feature]['max']]
#                    self.opt.append(vec)
#            
#            #now populating the entries with models on display
#            if self.opt:
#                for i, row in enumerate(self.opt):
#                    for j, cellValue in enumerate(row): 
#                        self.optEntries[i][j].delete(0,tk.END)
#                        self.optEntries[i][j].insert(tk.END, cellValue)
#            else:
#                #this is a new model instance
#                #clears all previous model entries
#                for row in self.optEntries:
#                    for cell in row:
#                        cell.delete(0,tk.END )
#            
#            for i, feature in enumerate(self.depVars):
#                self.depVarLabels[i].configure(state='normal') #makes this entry editable
#                self.depVarLabels[i].delete(0,tk.END) #clears whatever is in it.
#                self.depVarLabels[i].insert(tk.END, (', ').join(self.depVars[feature]))
#                self.depVarLabels[i].configure(state='disabled', disabledbackground='white', disabledforeground='black') #makes it readable only, and reapplies pallette.        
#                    
#        else:
#            self.modelName = ''
#            self.about.configure(text='Juno AI 污水处理工艺建模：'+self.modelName)
#            for i in range(len(self.notebook.tabs())):
#                self.notebook.tab(i,state='disabled')
#            self.status.configure(text='请选择工艺！')
#        return
    
    def clickAbout(self):
        ABOUT_TEXT = """\nJuno是一款污水处理仿真系统，由浙江巨能环境工程有限公司所属污水处理专家、人工智能专家和数学家共同打造。里面有大量的机器学习建模算法，从污水处理专家提供的数据中自动学习，采用了先进的强化学习、仿真技术和进化算法，来解决现实的污水处理问题。"""
                        
        DISCLAIMER = """
        开发人员：郭慧、邹德扬"""
                        
        VERSION= """
        版本：5.1.3\n
        """
        
        toplevel = tk.Toplevel() #relief = flat, groove, raised, ridge, solid, or sunken
        toplevel.wm_title('关于Juno')
        toplevel.geometry("300x600")
        canvas = tk.Label(toplevel, text='\n')
        canvas.pack()
        
        #place image
        load = Image.open(path /'assets'/ "logo.png")
        h = load.size[1]
        w = load.size[0]
        load = load.resize((250, int(250*h/w)))
        render = ImageTk.PhotoImage(load)
        
        img = tk.Label(toplevel, image=render)
        img.image = render
        img.pack()
        
        label1 = tk.Label(toplevel, text=ABOUT_TEXT, wraplength=250)
        label1.pack()
        label2 = tk.Label(toplevel, text=DISCLAIMER, wraplength=250)
        label2.pack()
        label3 = tk.Label(toplevel, text=VERSION, wraplength=250)
        label3.pack()
        
if __name__ == "__main__":
    root = tk.Tk()
    #root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=APP_ICON))
    #s = ttk.Style(root)
    #s.theme_use('clam')
    #s.configure('raised.TMenubutton', borderwidth=1, state='disabled')

    #s=ttk.Style()
    #s.configure('W.TButton',font=("Microsoft YaHei",10))
    # s.theme_use('vista')
    s = ttk.Style()
    s.configure('TNotebook.Tab', width=15, padding=(5, 5))
    s.configure('TNotebook', tabmargins = (0, 0, 0, 0))

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


