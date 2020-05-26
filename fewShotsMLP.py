# -*- coding: utf-8 -*-
import numpy as np
import json
import matplotlib.pyplot as plt
import time
import wastewater as ww
import treatmentEffect as te
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor,ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import MultiTaskElasticNetCV
from sklearn.linear_model import MultiTaskLassoCV, MultiTaskLasso, LinearRegression, RidgeCV, Lasso, LassoCV, LassoLars, BayesianRidge
from sklearn.preprocessing import StandardScaler
import random
import gplearn.genetic as gp

dict2Array = lambda dictionary : [dictionary[feature] for feature in dictionary.keys()]
array2Dict = lambda array, features: dict(zip(list(features),array))

#trX,trY = map(lambda x: np.array(list(map(dict2Array, x))), [X,Y])

def training(X,Y):
    trX,trY = map(lambda x: np.array(list(map(dict2Array, x))), [X,Y])
    scaler = StandardScaler(trX)
    scaler.fit(trX)
    #trX = scaler.fit_transform(trX)
    
    regrs = [gp.SymbolicRegressor(verbose=1).fit(trX, trY[:,i]) for i in range(len(trY[0]))]
    #regr = BayesianRidge().fit(trX, trY)
    
    Ypred = np.array([np.clip(regr.predict(trX),0,1e10)  for regr in regrs]).T
    with np.errstate(divide='ignore', invalid='ignore'):
        e = (np.abs(Ypred-trY)/Ypred)
    e[np.isnan(e)] = 0
    e[np.isinf(e)] = 0
    errorByRows = np.mean(e,axis=1)*100
    errorByCols = np.mean(e,axis=0)*100
    return Ypred, regrs, scaler, errorByRows, errorByCols

def testing(X,Y, regrs, scaler):
    trX,trY = map(lambda x: np.array(list(map(dict2Array, x))), [X,Y])
    #trX = scaler.fit_transform(trX)
    #Ypred = np.clip(regr.predict(trX),0,1e10) 
    Ypred = np.array([np.clip(regr.predict(trX),0,1e10)  for regr in regrs]).T
    with np.errstate(divide='ignore', invalid='ignore'):
        e = (np.abs(Ypred-trY)/Ypred)
    e[np.isnan(e)] = 0
    e[np.isinf(e)] = 0
    errorByRows = np.mean(e,axis=1)*100
    errorByCols = np.mean(e,axis=0)*100
    return Ypred, errorByRows, errorByCols

if __name__=='__main__':
    t1 = time.time()
    print('TRAINING')
    modelname = '厌氧'
    model = te.loadModel(modelname)
    opt = te.parseModel(model)[0]
    opt['可生化性']['max'] = 100
    X,Y = [],[]
    for i in range(10):
        x = ww.wastewater()
        if random.random() > 0.0:
            x.generateFromOpt(opt)
        else:
            x.simulate(random=True)
        X.append(x.water)
        #print('input wastewater',x.water)
        y = te.treat(x,modelname)['effluent'].water
        #print(y['COD'])
        Y.append(y)
    
    
    Ypred, regr, scaler, ebr, ebc = training(X,Y)
    
    print("\nTESTING")
    X,Y = [],[]
    for i in range(5):
        x = ww.wastewater()
        if random.random() > 0.0:
            x.generateFromOpt(opt)
        else:
            x.simulate(random=True)
        X.append(x.water)
        #print('input wastewater',x.water)
        y = te.treat(x,modelname)['effluent'].water
        #print(y['COD'])
        Y.append(y)
    
    
    Ypred, ebr, ebc = testing(X,Y, regr, scaler)
    Y2 = list(map(lambda arr: array2Dict(arr, Y[0].keys()), Ypred))
    print(Y,Y2)
    print('error by rows', ebr)
    print('error by cols', ebc)
    print('error', np.mean(ebr), '%')
    print(ebr[0])
    for feature in Y[0]:
        print(feature, Y[0][feature], Y2[0][feature])
    
    
    
#    trX,trY = map(lambda x: np.array(list(map(dict2Array, x))), [X,Y])
#    
#    outputVar = '可生化性'
#    dependentVars ='可生化性',# ('温度','COD','pH','TN','重金属','SS（纤维）','SS（絮状）','Cond','可生化性')
#    
#    outInd = x.features.index(outputVar)
#    inInds = list(map(lambda var: x.features.index(var), dependentVars))
#    Y1 = trY[:,outInd]
#    X1 = list(zip(*list(map(lambda ind: trX[:,ind], inInds))))
##     #regr = MLPRegressor(hidden_layer_sizes=(10,), max_iter=10000).fit(X1[:-1], Y1[:-1])#random_state=1,  
##     #regr = RandomForestRegressor().fit(X1[:-1], Y1[:-1])
##     regr = ElasticNetCV().fit(X1[:-5], Y1[:-5])
##     #regr = KNeighborsRegressor(weights='distance').fit(X1[:-1], Y1[:-1])
##     Y2 = np.clip(regr.predict(X1[:-5]),0,1e10) 
##     [print(X1[:-5][i][0],Y1[:-5][i],Y2[i]) for i in range(len(Y2))]
##     print('errors', np.mean(np.abs(Y2-Y1[:-5]))/np.max((Y1[:-5]))*100, '%')
## #    #args, ypreds, errors, probs, optBounds = learning(X,Y) #TRAINING GOES HERE
##     print('\nTESTING')
##     Y2 = np.clip(regr.predict(X1[-5:]),0,1e10) 
##     [print(X1[-5:][i][0],Y1[-5:][i],Y2[i]) for i in range(len(Y2))]
##     print('errors', np.mean(np.abs(Y2-Y1[-5:]))/np.max((Y1[-5:]))*100, '%')
## #    
#    
#    
#    
#    #regr = MLPRegressor(hidden_layer_sizes=(10,), max_iter=10000).fit(trX[:-5],trY[:-5]) 
#    #regr = RandomForestRegressor().fit(trX[:-5],trY[:-5])
#    regr = MultiTaskLassoCV(normalize=False).fit(trX[:-5], trY[:-5])
#    #regr = KNeighborsRegressor().fit(trX[:-5],trY[:-5]) #weights='distance'
#    Y2 = np.clip(regr.predict(trX[:-5]),0,1e10) 
#    [print(trX[:-5][i][0],trY[:-5][i],Y2[i]) for i in range(len(Y2))]
#    print('errors', np.mean(np.abs(Y2-trY[:-5]))/np.max((trY[:-5]))*100, '%')
##    #args, ypreds, errors, probs, optBounds = learning(X,Y) #TRAINING GOES HERE
#    print('\nTESTING')
#    Y2 = np.clip(regr.predict(trX[-5:]),0,1e10) 
#    [print(list(map( lambda arr: list(np.round(arr,2)), [trX[-5:][i],trY[-5:][i],Y2[i]]))) for i in range(len(Y2))]
#    print('errors', np.mean(np.abs(Y2-trY[-5:]))/np.max((trY[-5:]))*100, '%')
##    
#    
##    x = ww.wastewater()
##    x.generateFromOpt(opt)
##    #x.simulate(random=True)
##    #ypred = predict(x,args,probs, optBounds) #TEST PREDICTION GOES HERE!
##    
##    y = te.treat(x,'厌氧')['effluent']
##    print('\nactual y')
##    list(map(lambda row: print(row[0][0],round(row[0][1],1),round(row[1][1],1),round(row[2][1],1)), zip(x.water.items(), ypred.water.items(),y.water.items())))
##    print('probability distribution')
##    print(np.array(probs).T)
##    print('args')
##    print(np.array(args).T)
    t2 = time.time()
    print('time taken for training and testing in real time', t2-t1,'ms')