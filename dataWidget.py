# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from pathlib import Path
#from PIL import ImageTk, Image
#import win32api
import glob
import platform
import os
#import random
import json
from functools import partial
#import treatmentEffect as te
import fewShotsLearning as fsl
#import wastewater as ww
#import numpy as np
import matplotlib.pyplot as plt
import csv
import time
import fewShotsLearning as fsl

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
        
        emptyFrame = tk.Frame(self.master, height=15)
        emptyFrame.pack(side='top')
        
        self.body = tk.Frame(self.master)
        #self.body.pack(side='top')
        
        # self.titleLabel = ttk.Label(self.body, 
        #                             text='\n'+APP_TITLE+'\n', 
        #                             font=(font, 13))
        # self.titleLabel.pack(side='top')
        
        
        buttons = tk.Frame(self.body)
        buttons.pack(side='top')
        
        exportBtn = ttk.Button(buttons, text='导出CSV', command=self.exportData)
        exportBtn.pack(side='left')
        
        importBtn = ttk.Button(buttons, text='导入CSV + 建模', command=self.importData)
        importBtn.pack(side='left')
        
        self.saveBtn = ttk.Button(buttons, text='保存变更', command=self.saveData)
        #self.saveBtn.pack(side='left')
        
        emptyFrame = tk.Frame(self.body, height=20)
        emptyFrame.pack(side='top')
        
        ################################
        
        dataFrame = tk.Frame(self.body)
        dataFrame.pack(side='top',  fill='both')
        
        emptyFrame = tk.Frame(dataFrame, width=20)
        emptyFrame.pack(side='left')
        
        listboxFrame = tk.Frame(dataFrame)
        listboxFrame.pack(side='left')
        
        label = tk.Label(listboxFrame, text='数据记录id')
        label.pack(side='top')
        self.listbox = tk.Listbox(listboxFrame, bg='#fffffe', relief='flat', selectbackground='slategray', selectforeground='#fffffe', highlightthickness=0, height=15) 
        self.listbox.pack(side = tk.LEFT, fill = tk.BOTH) 
        self.listbox.bind('<<ListboxSelect>>', self.selectData)
        scrollbar = tk.Scrollbar(listboxFrame) 
          
        # Adding Scrollbar to the right 
        # side of root window 
        scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH) 
         
        
        # Insert elements into the listbox 
        
              
        # Attaching Listbox to Scrollbar 
        # Since we need to have a vertical  
        # scroll we use yscrollcommand 
        self.listbox.config(yscrollcommand = scrollbar.set) 
          
        # setting scrollbar command parameter  
        # to listbox.yview method its yview because 
        # we need to have a vertical view 
        scrollbar.config(command = self.listbox.yview) 
         
        
        
        self.previewFrame = tk.Frame(dataFrame)
        self.previewFrame.pack(side='left', fill='x',  expand=True)
        #previewFrame.pack(side='left')
        # previewLabel = tk.Label(previewFrame, text='数据预览')
        # previewLabel.pack(side='top')
        

        # self.previewPane = ScrolledText(previewFrame, width=50, height=4, bg='#fffffe', font=(font,10))
        # self.previewPane.pack(side='top')
        # self.previewPane.insert(tk.END,'正在加载数据...')
        # self.previewPane.configure(state=tk.DISABLED)
        
        previewTableFrame = tk.Frame(self.previewFrame)
        previewTableFrame.pack(side='top')
        
        self.previewTableLabel = tk.Label(previewTableFrame, text='\n详细数据：id \n')
        self.previewTableLabel.pack(side='top')
        
        previewTable = tk.Frame(previewTableFrame)
        previewTable.pack(side='top')
        
        headers = ['污水指标','进水','机器预测出水','专家反馈','误差（%）']
        
        #constructing header
        headerRow = tk.Frame(previewTable)
        headerRow.pack(side='top')
        for j, header in enumerate(headers):
            label = tk.Entry(headerRow, disabledforeground='#fffffe', disabledbackground='slategray', width=15)
            label.pack(side='left')
            label.insert(tk.END, header)
            label.configure(state='disabled')
            if j==0:
                label.configure(disabledbackground='darkslategray', width=20)
            elif header in ['进水','专家反馈']:
                label.configure(disabledbackground='lightslategray')
                
        self.rows = []
        self.entries = []
        for i, feature in enumerate(self.features):
            row = tk.Frame(previewTable)
            if i % 2 == 0:
                row.configure(bd=1)
            row.pack(side='top')
            rowEntries = []
            for j, header in enumerate(headers):
                label = tk.Entry(row, disabledforeground='black', disabledbackground='mistyrose', relief='flat', justify='right', cursor='xterm', background='#fffffe', foreground='black', width=15)
                label.pack(side='left')
                label.bind('<KeyRelease>', self.checkUnsaved)
                
                if j==0:
                    label.insert(tk.END, feature)
                    label.configure(justify='left', width=20)
                    
                if header in ['污水指标','机器预测出水','误差（%）']:
                    label.configure(state='disabled', cursor='arrow')
                rowEntries.append(label)
                label.bind('<Button-1>', partial(self.selectCell, i, j))
            self.entries.append(rowEntries)
            self.rows.append(row)
        
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
    def selectCell(self, i, j, event=1):
        print(i,j)
        #reset all row highlight border to 0
        # for row in self.rows:
        #     row.configure(bd=0)
        # row = self.rows[i]
        # row.configure(bd=1)
        
    def calcError(self, event=1):
        yactual, ypred = [],[]
        for i, feature in enumerate(self.features):
            cell = self.entries[i][3]
            yactual.append(float(cell.get()))
            
            cell = self.entries[i][2]
            try:
                ypred.append(float(cell.get()))
            except ValueError:
                return
        error = fsl.computeError(ypred, yactual)
        print('error', error)
        
        #output error back into table
        for i, feature in enumerate(self.features):
            cell = self.entries[i][4]
            cell.configure(state='normal')
            cell.delete(0,tk.END)
            cell.insert(0,round(error[i],2))
            cell.configure(state='disabled')
            
    def checkUnsaved(self, event=1):
        #check if self.entries are different from saved values;
        #print(self.data)
        self.status.configure(text='正常')
        print(self.id)
        x,ypred,y,err = self.data['X'][self.id], self.data['Ypred'][self.id], self.data['Y'][self.id], self.data['err'][self.id]
        # print('X',x)
        # print('Y',y)
        # print('ypred',ypred) 
        # print('err',err)
        entries = []
        for row in self.entries:
            for i, entry in enumerate(row):
                if i in [1,3]:
                    try:
                        float(entry.get())
                    except ValueError:
                        self.status.configure(text='错误：输入栏中' + str(entry.get()) + '不是数字！')
                        return
        #print(entries)
        
        self.calcError()
        
        data = []
        for feature in self.features:
            row = [feature, x[feature], ypred[feature] if ypred else '', y[feature], err[feature] if ypred else '']
            row = [str(e) if i > 0 else e for i,e in enumerate(row)]
            data.append(row)
        print('data',data)
        entries = [[e.get() for e in row] for row in self.entries]
        print('entries',entries)
        unsaved = entries != data
        print('unsaved?', unsaved)
        if unsaved:
            self.status.configure(text='输入正常，数据已变更，未保存。')
            self.saveBtn.pack(side='left')
        else:
            self.status.configure(text='正常')
            self.saveBtn.pack_forget()
        ...
    
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
            
            self.body.pack(side='top',fill='x')
            self.status.configure(text='正常')
            
            data = json.loads(open(path / 'models' / self.modelName / dataFile, 'r').read())
            self.data = data
            
            X = data['X']
            self.listbox.delete(0,tk.END)
            
            for i, x in enumerate(X):
                self.listbox.insert(tk.END, i+1)  #i+1
            
            # self.previewPane.configure(state=tk.NORMAL)
            # self.previewPane.delete(1.0, tk.END)
            # self.previewPane.insert(tk.END, str(data)[:2000] + '...')
            # self.previewPane.configure(state=tk.DISABLED)

        ...
    
    def selectData(self, event):
        
        print(self.listbox.curselection())
        try:
            ind = self.listbox.curselection()[0]
            
            self.previewTableLabel.configure(text='\n详细数据：id ' + str(ind+1) + '\n')
            self.id = ind
        except IndexError:
            return
        # self.previewPane.configure(state=tk.NORMAL)
        # self.previewPane.delete(1.0, tk.END)
        # self.previewPane.insert(tk.END, str(self.data['Y'][ind])[:2000] + '...')
        # self.previewPane.configure(state=tk.DISABLED)
        
        data = self.data
        X,Y = data['X'][ind], data['Y'][ind]
        try:
            ypred, err = data['Ypred'][ind], data['err'][ind]
        except KeyError:
            ypred, err = None, None
        #X,Y are dicts
        for i, feature in enumerate(X):
            cell = self.entries[i][1]
            #cell.configure(state='normal')
            cell.delete(0,tk.END)
            cell.insert(tk.END, X[feature])
            #cell.configure(state='disabled')
        
        for i, feature in enumerate(Y):
            cell = self.entries[i][3]
            #cell.configure(state='normal')
            cell.delete(0,tk.END)
            cell.insert(tk.END, Y[feature])
            #cell.configure(state='disabled')
        
        if ypred:
            for i, feature in enumerate(ypred):
                cell = self.entries[i][2]
                cell.configure(state='normal')
                cell.delete(0,tk.END)
                cell.insert(tk.END, ypred[feature])
                cell.configure(state='disabled')
        else:
            #clear entry
            for i, feature in enumerate(self.features):
                cell = self.entries[i][2]
                cell.configure(state='normal')
                cell.delete(0,tk.END)
                cell.configure(state='disabled')
          
        if err:
            for i, feature in enumerate(err):
                cell = self.entries[i][4]
                cell.configure(state='normal')
                cell.delete(0,tk.END)
                cell.insert(tk.END, err[feature])
                cell.configure(state='disabled')
        
        else:
            #clear entry
            for i, feature in enumerate(self.features):
                cell = self.entries[i][4]
                cell.configure(state='normal')
                cell.delete(0,tk.END)
                cell.configure(state='disabled')
        
    def saveData(self, event=1):
        entries = [[e.get() for e in row] for row in self.entries]
        x, ypred, y, err = {},{},{},{}
        
        for row in entries:
            feature = row[0]
            x[feature] = row[1]
            if row[2]:
                ypred[feature] = row[2]
            y[feature] = row[3]
            if row[4]:
                err[feature] = row[4]
            
        print('X',x)
        print('Y',y)
        print('ypred',ypred) 
        print('err',err)
        #print(self.data)
        
        self.data['X'][self.id] = x
        self.data['Ypred'][self.id] = ypred
        self.data['Y'][self.id] = y
        self.data['err'][self.id] = err
        
        dataFile = self.modelName + '.data.json'
        with open(path / 'models' / self.modelName / dataFile, 'w') as f:
            f.write(json.dumps(self.data))
        
        self.status.configure(text='保存成功！')
        ...
    
    def exportData(self, event=1):
        timestamp = ('').join(str(time.time()).split('.'))
        
        X = self.data['X']
        Y = self.data['Y']
        Ypred = self.data['Ypred']
        err = self.data['err']
        rows = []
        rows.append(['id','数据类'] + list(X[0].keys()))
        for i, x in enumerate(X):
            row1 = [i+1, '进水'] + list(x.values())
            row2 = [i+1, '机器预测出水'] + list(Ypred[i].values())
            row3 = [i+1, '专家反馈出水'] + list(Y[i].values())
            row4 = [i+1, '误差%'] + list(err[i].values())
            rows.append(row1)
            rows.append(row2)
            rows.append(row3)
            rows.append(row4)
            
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
        try:
            csvreader = csv.reader(open(filename, 'r', encoding='gbk', newline=newline).readlines(), dialect='excel')
        except UnicodeDecodeError:
            csvreader = csv.reader(open(filename, 'r', encoding='utf-8', newline=newline).readlines(), dialect='excel')
        
        #check data validity
        acceptedTypes = ['进水', '专家反馈出水']
        rawdata = []
        for row in csvreader:
            rawdata.append(row)
        
        ls = []
        for i, row in enumerate(rawdata):
            if row:
                if not row[-1]:
                    row.remove(row[-1])
                l = len(row)
                if row[1] in acceptedTypes:
                    ls.append(l)
        for l in ls:
            if l != ls[0]:
                #some row contains extra columns!
                self.status.configure(text='错误：某行的列数不同与其它的！数据格式必须满足每行列数相同。')
                return
         
        typeOrder = ['进水','机器预测出水', '专家反馈出水','误差%']
        acceptedTypes = ['进水', '专家反馈出水']
        correct = typeOrder[0]
        for i, row in enumerate(rawdata):
            if row:
                if i > 0: #i=0 is header
                    for j,v in enumerate(row):
                        print('v',v)
                        try:
                            float(v)
                        except ValueError:
                            coord = str((i+1,j+1))
             
                            if j != 1:
                                if v in acceptedTypes:
                                    self.status.configure(text='错误：在' + coord + '格是空格或存在非数字')
                                    return
                                else:
                                    pass
                            else:
                                if v not in typeOrder:
                                    self.status.configure(text='错误：在' + coord + '格类型标注不对。应该为”出水“或”进水“。')
                                    return
                                else:
                                    if v != correct:
                                        self.status.configure(text='错误：在' + coord + '格类型标注不对。应该为”' + correct + '“。')
                                        return
                                    else:
                                        ind = typeOrder.index(v)
                                        if ind == len(typeOrder) - 1:
                                            correct = typeOrder[0]
                                        else:
                                            correct = typeOrder[ind + 1]
            else:
                #empty row
                ...
        
        
        
        data = []
        for row in rawdata:
            if row:
                data.append(row)
        
        print(data)
        features = data[0][2:]
        #print(features)
        X,Y, Ypred, err, e = [],[],[], [], []
        
        data = data[1:]


        #print(data)
        
        for i, row in enumerate(data):
            if row[1] == '进水':
                j = row[0]
                x = dict(zip(features, [float(v) for v in row[2:]]))
                #print(j, '进水', x)
                X.append(x)
            elif row[1] == '专家反馈出水':
                j = row[0]
                y = dict(zip(features, [float(v) for v in row[2:]]))
                #print(j,'出水',y)
                Y.append(y)
            # elif row[1] == '机器预测出水':
            #     j = row[0]
            #     ypred = dict(zip(features, [float(v) for v in row[2:]]))
            #     #print(j,'出水',y)
            #     Ypred.append(y)
            # elif row[1] == '误差%':
            #     j = row[0]
            #     e = dict(zip(features, [float(v) for v in row[2:]]))
            #     #print(j,'出水',y)
            #     err.append(e)
            else:
                #other row types such as 误差 and 机器预测出水 not required for modeling.
                ...
        # print('X',X)
        # print('Y',Y)
        # print(len(X),len(Y))
        
        #iterative training to simulate error progression.
        for i, x in enumerate(X):
            self.status.configure(text='正在建模...(' + str(i+1) + '/' + str(len(X)) + ')')
            fsl.training(X[:i+1], Y[:i+1], self.modelName)
            try:
                Ypred, errorByRows, errorByCols = fsl.testing([X[i+1]],[Y[i+1]], self.modelName)
                err = errorByRows[0]
                e.append(err)
            except IndexError:
                #last row reached
                ...
        #plot error graphs.
        trainedData = {'X':X, 'Y':Y, "e":e}
        
        plt.scatter(range(1,len(e)+1), e, s=40, marker='o', color='slategray')
        plt.scatter([0,10],[0,30], s=0, marker='o', color='slategray')
        plt.plot(range(1,len(e)+1), e, color='slateblue')
        plt.title('\nPrediction Error Graph\n')
        plt.xlabel('\nIterations\n')
        plt.ylabel('\nError %\n')
        plt.savefig(path / 'models' / self.modelName / 'training.png' , dpi=300, bbox_inches = "tight")
        plt.clf()
        
        #save data
        dataFile =  self.modelName + '.data.json'
        with open(path / 'models'/ self.modelName / dataFile, 'w') as f:
            f.write(json.dumps(trainedData))
        self.status.configure(text='导入成功！建模完成！')
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
    root.geometry('1200x850')
    #show window
    root.mainloop()