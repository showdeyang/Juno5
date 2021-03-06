# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
#from PIL import ImageTk, Image
#import win32api
#import glob
import platform
import os
#import random
import json
from functools import partial
#from tksheet import Sheet
#from tkintertable import TableCanvas, TableModel
from MyWidgets import ScrolledWindow
import dataWidget

path = Path('./')
APP_TITLE = '最优运行条件配置'
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
            
            self.combokey = tk.Label(self.cb, text='污水处理工艺：')
            self.combokey.pack(side='left')
            
            self.combo = ttk.Combobox(self.cb, values=['请选择工艺'] + self.treatments)
            self.combo.pack(side='left')
            self.combo.current(0)
            self.combo.bind("<<ComboboxSelected>>", self.loadModel)
        else:
            self.combo = modelCombobox
            self.combo.bind("<<ComboboxSelected>>", self.loadModel)
        
        emptyFrame = tk.Frame(self.master, height=15)
        emptyFrame.pack(side='top')
        
        self.optFrame = tk.Frame(self.master)
        #self.optFrame.pack(side='top',fill='y')
        
        # self.optFrameLabel = ttk.Label(self.optFrame, text='\n最优运行条件配置\n', font=(font, 13))
        # self.optFrameLabel.pack(side='top')
        
        ##################################
        #add buttons here for optimality Frame

        btn = ttk.Button(self.optFrame,text='保存配置', command=self.saveEntries, cursor='hand2')
        btn.pack(side='top')
        
        emptyFrame = tk.Frame(self.optFrame,height=20)
        emptyFrame.pack(side='top')
        
        #Table
        self.optTableFrame = tk.Frame(self.optFrame)
        self.optTableFrame.pack(side='top')
        
        self.optTableSW = ScrolledWindow(self.optTableFrame)
        self.optTableSW.pack(side='top')
        
        
        self.optTable = tk.Frame(self.optTableSW.scrollwindow)
        self.optTable.pack(side='top') #side='top'
        
        
        if not statusLabel:
            self.statusBar = tk.Frame(master=self.master, relief='sunken', bd=1)
            self.statusBar.pack(side='bottom', fill='x')
    
            self.status = tk.Label(master=self.statusBar, text='请选择工艺')
            self.status.pack(side='left')
        else:
            self.status = statusLabel
        
        
        self.optEntries = []
        self.depVarLabels = []
        self.depVars = {feature: [feature] for feature in self.features}
        self.opt = []
        
        
        headers = ['污水指标','最低进水值*','最高进水值*','出水指标所依赖的进水指标']
        width = 10
        for i in range(len(self.features)+1):
            if i == 0:
                row = tk.Frame(self.optTable)
                row.pack(side='top')
                #this is the headers row
                for header in headers:
                    if header != headers[-1]:
                        if header == headers[0]:
                            label = tk.Entry(row,width=width+5, disabledforeground='#fffffe', disabledbackground='steelblue', bd=1, relief='flat')
                        else:
                            label = tk.Entry(row,width=width, disabledforeground='#fffffe', disabledbackground='slategray', bd=1, relief='flat')
                        label.insert(tk.END, header)
                        label.configure(state='disabled')
                        label.pack(side='left')
                    else:
                        frame = tk.Frame(row)
                        frame.pack(side='left')
                        label = tk.Entry(row, disabledforeground='#fffffe', disabledbackground='lightseagreen', width=60, relief='flat', justif='center')
                        
                        label.insert(tk.END, header)
                        label.configure(state='disabled')
                        label.pack(side='left',)
            else:
                feature = self.features[i-1]
                row = tk.Frame(self.optTable, relief='flat', bd=1)
                row.pack(side='top', expand=True)
                
                col1 = tk.Entry(row, width=width+5, bd=0, cursor='arrow')
                col1.insert(tk.END,self.features[i-1])
                col1.configure(state='disabled', disabledforeground='#32322D') #, disabledbackground='aliceblue'
                col1.pack(side='left')
                
                optRow = []  
                #btns = []
                for j in range(2):
                    e = tk.Entry(row, width=width, bg='#fffffe',bd=1, justify='right', relief='groove')
                    e.bind('<KeyRelease>', self.checkUnsaved)
                    e.pack(side='left')
                    optRow.append(e)
                self.optEntries.append(optRow)

                labelFrame = tk.Frame(row,bg='#fefefe',bd=0)
                labelFrame.pack(side='left', expand=True, fill='x')
                label = tk.Entry(labelFrame, justify='center', bg='white', bd=0, relief='flat', cursor='hand2')
                label.insert(tk.END, (', ').join(self.depVars[feature]))
                label.configure(state='disabled', disabledbackground='white', disabledforeground='#32322D', width=60)
                label.pack(side='left', expand=True,fill='x')
                
                label.bind('<Button-1>',partial(self.editDepVars, feature))
                self.depVarLabels.append(label)
                

        #Populate entries with data
        #self.opt = [[random.random(),random.random()] for i in self.features] #Test if entries fillin g works.
        if self.opt:
            for i, row in enumerate(self.opt):
                for j, cellValue in enumerate(row): 
                    self.optEntries[i][j].insert(tk.END, cellValue)
        else:
            ...
            
        
        captionFrame = tk.Frame(self.optTable, width=600)
        captionFrame.pack(side='top',expand=True, fill='x')
        caption = tk.Label(captionFrame, text='\n注：*必填\n', font=(font, 9), justify='left')
        caption.pack(side='left')
        

        

    
    def checkUnsaved(self, event=1):
        self.status.configure(text='')
        opt = []
        for row , feature in zip(self.optEntries, self.features):
            v = []
            for entry in row:
                if entry.get():
                    try:
                        v.append(float(entry.get()))
                    except ValueError:
                        self.status.configure(text='错误：输入栏'+feature+'中必须是数字')
                        return
                else:
                    self.status.configure(text='错误：输入栏'+feature+'中不能为空')
                    
                    return
            #print(opt)
            if v[1] < v[0]:
                self.status.configure(text='错误：输入栏' + feature + '的最高值不能小于最低值')
                
                
                return
            opt.append(v)

        depvarFile = self.modelName + '.depVar.json'
        if os.path.isfile(path / 'models' / self.modelName / depvarFile):
            depvar = json.loads(open(path / 'models' / self.modelName / depvarFile, 'r').read())
        else:
            depvar = {feature: [feature] for feature in self.features}

        print('depvar',depvar)
        print('self depvar', self.depVars)
        print(depvar == self.depVars)
    
        if opt != self.opt or depvar != self.depVars:
            self.status.configure(text='输入正常，未保存')
        else:
            self.status.configure(text='正常')

    def saveEntries(self):
        self.checkUnsaved()
        optDict = {}
        for row , feature in zip(self.optEntries, self.features):
            optDict[feature] = {}
            for entry, key in zip(row, ['min','max']):
                if entry.get():
                    try:
                        optDict[feature][key] = float(entry.get())
                    except ValueError:
                        self.status.configure(text='错误：输入栏'+feature+'中必须是数字')
                        return
                else:
                    self.status.configure(text='错误：输入栏'+feature+'中不能为空')
                    return
            print(optDict)
            if optDict[feature]['max'] < optDict[feature]['min']:
                self.status.configure(text='错误：输入栏' + feature + '的最高值不能小于最低值')
                return
            
        print('opt', optDict)
        print('depVars', self.depVars)
        
        ##############################
        #check entries for validity (float? empty?)
        
        ###############################
        #check if model folder exists, if not, create it.
        if not os.path.isdir( path / 'models'/ self.modelName):
            os.mkdir(path / 'models' / self.modelName)
        #save optDict and depVars in the model folder.
        optFile, depVarFile = self.modelName + '.opt.json', self.modelName + '.depVar.json'
        optFilePath = path / 'models' / self.modelName / optFile
        depVarFilePath = path / 'models' / self.modelName / depVarFile
        
        with open(optFilePath, 'w') as f:
            f.write(json.dumps(optDict))
        
        with open(depVarFilePath,'w') as f:
            f.write(json.dumps(self.depVars))
         
        #show status
        self.status.configure(text='模型保存成功！')
        #very useful to have a status icon indicating whether there are any unsaved changes, if not, prompts for saving before leaving.
        self.update_idletasks()
        
        dataFile = self.modelName + '.data.json'
        if os.path.isfile(path / 'models' / self.modelName / dataFile):
            data = json.loads(open(path / 'models' / self.modelName / dataFile, 'r').read())
            self.data = data
            #retrain model with new depVars definition
            dataWidget.Window.exportData(self,file= 'output.csv')
            dataWidget.Window.importData(self,file= 'output.csv')
            try:
                os.remove(path / 'output' / 'output.csv')
            except FileNotFoundError:
                pass
            self.update_idletasks()
            self.status.configure(text='模型配置变更成功，已重新建模！')
        
        
    def editDepVars(self, fea, event):
        
        editbox = tk.Toplevel()
        editbox.title('编辑指标依赖关系')
        
        label = tk.Label(editbox,text='\n　请勾选 '+fea+' 的依赖变量（可多选）。　\n　为达到最佳训练效果，最好不要勾选超过4个指标。　\n',justify='left')
        label.pack(side='top')

        checkboxes = tk.Frame(editbox)
        checkboxes.pack(side='top',expand=True, fill='x')
        varlist = []
        for feature in self.features:
            var = tk.IntVar()
            if feature in self.depVars[fea]:
                var.set(1)
            cbframe = tk.Frame(checkboxes)
            cbframe.pack(side='top')
            checkbox = ttk.Checkbutton(cbframe, variable=var, text=feature, width=20, onvalue=1, offvalue=0, cursor='hand2')
            checkbox.pack(side='left')
            varlist.append(var)
        
        def genDepVars():
            depVars = []
            for feature, value in zip(self.features, varlist):
                if value.get():
                    depVars.append(feature)
                else:
                    if feature == fea:
                        depVars.append(feature)
            #print(depVars)
            ind = self.features.index(fea)
            self.depVarLabels[ind].configure(state='normal')
            self.depVarLabels[ind].delete(0,tk.END)
            self.depVarLabels[ind].insert(tk.END, (', ').join(depVars))
            self.depVarLabels[ind].configure(state='disabled', disabledbackground='white', disabledforeground='black')

            self.depVars[fea] = depVars
            print(self.depVars)
            self.checkUnsaved()
            editbox.destroy()
            return depVars
        
        emptyFrame = tk.Frame(editbox, height=10)
        emptyFrame.pack(side='top')
        
        savebtn = ttk.Button(editbox, text='确定', command=genDepVars)
        savebtn.pack(side='top')
        
        emptyFrame = tk.Frame(editbox, height=10)
        emptyFrame.pack(side='top')
        
    def loadModel(self,event=1):
        #print(self.modelName.get())
        self.features = json.loads(open(path / 'config'/'features.json','r').read())
        if self.combo.get() != '请选择工艺':
            self.optFrame.pack(side='top')
            #self.optTable.focus_set()
            self.modelName = self.combo.get()
            print(self.modelName)
            #self.modelLabel.configure(text=self.modelName)
            self.status.configure(text='正常')
            
            #load the depvars model if it already exists, else it is created on the spot:
            depvarFile = self.modelName + '.depVar.json'
            if os.path.isfile(path / 'models' / self.modelName / depvarFile):
                self.depVars = json.loads(open(path / 'models' / self.modelName / depvarFile,'r').read())
                
                
            else:
                self.depVars = {feature: [feature] for feature in self.features}
                self.status.configure(text='新模型')
                
    
            #if opt model exists, load it
            optFile = self.modelName + '.opt.json'
            self.opt = []
            if os.path.isfile(path / 'models' / self.modelName / optFile):
                self.optDict = json.loads(open(path / 'models' / self.modelName / optFile,'r').read())
                
                for feature in self.optDict:
                    vec = [self.optDict[feature]['min'], self.optDict[feature]['max']]
                    self.opt.append(vec)
            
            #now populating the entries with models on display
            if self.opt:
                for i, row in enumerate(self.opt):
                    for j, cellValue in enumerate(row): 
                        self.optEntries[i][j].delete(0,tk.END)
                        self.optEntries[i][j].insert(tk.END, cellValue)
            else:
                #this is a new model instance
                #clears all previous model entries
                for row in self.optEntries:
                    for cell in row:
                        cell.delete(0,tk.END )
            
            for i, feature in enumerate(self.depVars):
                self.depVarLabels[i].configure(state='normal') #makes this entry editable
                self.depVarLabels[i].delete(0,tk.END) #clears whatever is in it.
                self.depVarLabels[i].insert(tk.END, (', ').join(self.depVars[feature]))
                self.depVarLabels[i].configure(state='disabled', disabledbackground='white', disabledforeground='black') #makes it readable only, and reapplies pallette.        
                    
        else:
            self.modelName = ''
            #self.modelLabel.configure(text='')
            self.optFrame.pack_forget()
            self.status.configure(text='请选择工艺！')
        return

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