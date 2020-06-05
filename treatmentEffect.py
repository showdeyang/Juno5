# -*- coding: utf-8 -*-
import json
import numpy as np
from pathlib import Path
import wastewater as ww
import time
path = Path('./')

########################################
# treatment effect as functions
#These functions will be called through Lambda-currying (Currying is a functional programming concept)

def removal(wastewater, feature, removalRate):
    #wastewater is an object with attribute 'water being the dictionary of wastewater with features as keys.
    #removalRate is %-based, it removes % removalRate from the said feature of wastewater, and return the resultant wastewater object
    assert isinstance(wastewater, ww.wastewater), \
    'The input object is not of the type "wastewater".'
    x = wastewater.water
    y = {fea: x[fea] for fea in x}
    y[feature] = x[feature]*(1-(removalRate/100))
    y[feature] = np.random.normal(y[feature], y[feature]/50)
    y = ww.wastewater(y)
    #print('RMV triggered on', feature)
    return y

def regulate(wastewater, feature, target):
    #regulates the feature at a target value.
    assert isinstance(wastewater, ww.wastewater), \
    'The input object is not of the type "wastewater".'
    x = wastewater.water
    y = {fea: x[fea] for fea in x}
    y[feature] = np.random.normal(target, target/30)
    y = ww.wastewater(y)
    #print('RGL triggered on', feature)
    return y

def limit(wastewater, feature, limit):
    #limits the feature to be lower than the limit. This is a low-pass filter
    assert isinstance(wastewater, ww.wastewater), \
    'The input object is not of the type "wastewater".'
    x = wastewater.water
    y = {fea: x[fea] for fea in x}
    y[feature] = min(x[feature], np.random.uniform(0,limit))
    
    y = ww.wastewater(y)
    #print('LMT triggered on', feature)
    return y

def shift(wastewater, feature, change):
    #shifts the feature through the amount specified by the change. Change can be +\-.
    assert isinstance(wastewater, ww.wastewater), \
    'The input object is not of the type "wastewater".'
    x = wastewater.water
    y = {fea: float(x[fea]) for fea in x}
    #print(type(y[feature]))
    #print(type(change))
    y[feature] += np.random.normal(change, np.abs(change)/20)
    y[feature] = max(y[feature], 0)
    y = ww.wastewater(y)
    #print('SFT triggered on', feature)
    return y

def changeInProportion(wastewater, wastewater_init, feature, dependentFeature, ratio):
    #shifts the dependentFeature by the amount proportionate to the change in the (target) feature, at a ratio defined by (change in the dependentFeature)/ (change in target feature).
    assert isinstance(wastewater, ww.wastewater), \
    'The input object is not of the type "wastewater".'
    assert isinstance(wastewater_init, ww.wastewater), \
    'The input object is not of the type "wastewater".'
    x = wastewater.water
    y = {fea: x[fea] for fea in x}
    change = (x[dependentFeature] - wastewater_init.water[dependentFeature])/ratio
    y[feature] = max(x[feature] + change, 0)
    y = ww.wastewater(y)
    #print('CIP triggered on', feature)
    return y
    
def removalInProportion(wastewater, wastewater_init, feature, dependentFeature):
    assert isinstance(wastewater, ww.wastewater), \
    'The input object is not of the type "wastewater".'
    assert isinstance(wastewater_init, ww.wastewater), \
    'The input object is not of the type "wastewater".'
    x = wastewater.water
    y = {fea: x[fea] for fea in x}
    ratio = x[dependentFeature] / (wastewater_init.water[dependentFeature] + 10e-10)
    y[feature]*=ratio
    y = ww.wastewater(y)
    #print('RIP triggered on', feature)
    return y

def shiftByFeature(wastewater, wastewater_init, feature, dependentFeature):
    assert isinstance(wastewater, ww.wastewater), \
    'The input object is not of the type "wastewater".'
    assert isinstance(wastewater_init, ww.wastewater), \
    'The input object is not of the type "wastewater".'
    x = wastewater.water
    y = {fea: x[fea] for fea in x}
    change = x[dependentFeature] - wastewater_init.water[dependentFeature]
    y[feature] += change
    y = ww.wastewater(y)
    #print('SBF triggered on', feature)
    return y
    
#####################################
# Model processing
    
def loadSyntax():
    funcD = {'同比增减':changeInProportion, '限制':limit, '调节': regulate, '去除': removal, '增减': shift, '同比去除': removalInProportion, '同额增减': shiftByFeature}
    parameters = [['去除率'],['目标值'],['閥值'],['增量'],['依赖指标','增减比例']]
    operators = ['≤',' ≥','介于']
    effects = ['同比增减','限制', '调节','去除','增减']
    return funcD, parameters, operators, effects

def loadModel(modelName):
    modelFile = modelName + '.json'
    model = json.loads(open(path / 'models'/ modelFile,'r').read())

    return model

def loadOpt(modelName):
    modelFile = modelName + '.opt.json'
    model = json.loads(open(path / 'models'/ modelName/modelFile,'r').read())

    return model

def parseModel(model):
    
    def isnum(x):
        try:
            float(x)
            return True
        except ValueError:
            return False
    
    syntax = loadSyntax()
    funcD = syntax[0]
    dOpt = model['最优运行条件']
    dTre = model['最优处理效果']
    #print('dTre', dTre)
    opt = {}
    
    for condition in dOpt:
        #print('opt condition',condition)
        for feature in condition:
            
            opt[feature] = {}
            operator = list(condition[feature].keys())[0]
            
            vector = [float(v.strip()) for v in condition[feature][operator]]
            operator = operator.strip()
            opt[feature]['min'] = min(vector) * (operator!='≤') + 0 * (operator=='≤')
            opt[feature]['max'] = 10e10 * (operator=='≥') + max(vector)  * (operator!='≥')
            #print('parsed opt',opt[feature])
    fs,vs = [], []
    for effect in dTre:
        for feature in effect:
            
            #fea.append(feature)
            funcs = list(effect[feature].keys())
            fs.append(funcD[funcs[0]])
            #print(funcD[funcs[0]])
            for func in funcs:
                v = list(effect[feature][func].values())
                
                    
                v = list(map(lambda x: float(x) if isnum(x) else x, v))
                vs.append([feature,*v])
            
    treObj = list(zip(fs, vs))
    #[print('treobject',treobj) for treobj in treObj]
    return opt, treObj

def optimality(wastewater, opt):
    #determine how optimal is the wastewater to be treated based on opt. Opt is a dictionary.
    assert isinstance(wastewater, ww.wastewater)
    x = wastewater.water
    optVec = [(x[feature] - opt[feature]['min']) * (opt[feature]['max'] - x[feature]) / (opt[feature]['max'] - opt[feature]['min'])**2 for feature in opt]
    
    od = dict(zip(opt.keys(),optVec))
    optDict = {feature: 0.25 for feature in wastewater.features}
    optDict.update(od)
    efficacy = 1 + np.clip(min(optVec), -1, 0)
    optFlag = dict(filter(lambda x: x[1] < 0, optDict.items()))
    
    return efficacy, optDict, optFlag

def optTreat(x, modelname, treObj):
    assert isinstance(x, ww.wastewater), 'input is not a wastewater object.'
    
    y = ww.wastewater(x.water) #create a new wastewater y with the same characteristics of x.
    #delayF = []
    for tre in treObj:
        try:
            func = tre[0] #<function changeInProportion at 0x7f7b44034c80>
            args = tre[1] #['TN', 'COD', 250.0]
            #print('func',func)
            #print('args',args)
            y = func(y, *args)
            #print('x',x.water)
            #print('y',y.water)
        except TypeError:
            #delayF.append(tre)
            y = func(y,x, *args)
        #xlist.append(y)
#    for df in delayF:
#        y = df(y,x)
    #print('treated wastewater', y.water)
    return y

def treat(x, modelname):
    assert isinstance(x, ww.wastewater), 'input is not a wastewater object.'
    model = loadModel(modelname)
    opt, treObj = parseModel(model)
    y = optTreat(x, modelname, treObj)
    efficacy, optDict, optFlag = optimality(x, opt)
    #print('opt',opt)
    #print('optimality', optDict)
    #print('suboptimal features', optFlag)
    #print('treatment efficacy',efficacy)
    act_y = {feature: x.water[feature] + (y.water[feature] - x.water[feature])*efficacy for feature in y.water}
    z = ww.wastewater(act_y)
    result = {'effluent':z, 'efficacy': efficacy, 'flags': optFlag, 'opt':optDict , 'optEff':y}
    return result


if __name__ == '__main__':
    t1 = time.time()
    x = ww.wastewater({'COD': 1000, 'TN': 100, '温度':41})
    x.simulate(random=False)
    #print('input wastewater',x.water)
    zs = treat(x,'厌氧')
    
    t2 = time.time()
    print('time taken',(t2-t1)*1e3, 'ms')