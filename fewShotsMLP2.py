# -*- coding: utf-8 -*-
import numpy as np
import json
import matplotlib.pyplot as plt
import time
import wastewater as ww
import treatmentEffect as te
from sklearn.linear_model import BayesianRidge
import joblib
from sklearn.neural_network import MLPRegressor
#from sklearn.ensemble import RandomForestRegressor,ExtraTreesRegressor, GradientBoostingRegressor
#from sklearn.neighbors import KNeighborsRegressor
#from sklearn.linear_model import MultiTaskElasticNetCV
#from sklearn.linear_model import MultiTaskLassoCV, MultiTaskLasso, LinearRegression, RidgeCV, Lasso, LassoCV, LassoLars, BayesianRidge, Ridge
from sklearn.preprocessing import StandardScaler
import random
import gplearn.genetic as gp
#from sklearn.preprocessing import PolynomialFeatures
 
dict2Array = lambda dictionary : [dictionary[feature] for feature in dictionary.keys()]
array2Dict = lambda array, features: dict(zip(list(features),array))

#trX,trY = map(lambda x: np.array(list(map(dict2Array, x))), [X,Y])

def training(X,Y, depVars):
    trX,trY = map(lambda x: list(map(dict2Array, x)), [X,Y])
    features = list(X[0].keys())
    scaler1, scaler2 = StandardScaler(trX),  StandardScaler(trY)
    trX = scaler1.fit_transform(trX)
    #trY = scaler2.fit_transform(trY)
    trX,trY = np.array(trX),np.array(trY)
    
    regr = MLPRegressor(hidden_layer_sizes=(30,30), max_iter=int(1e10), activation='relu', solver='adam', alpha=10 , learning_rate='adaptive').fit(trX,trY)
    Ypred = np.clip(regr.predict(trX),0,1e10)
    #print(Ypred)
    trY[trY<1e-4] = 0
    Ypred[Ypred<1e-4] = 0
    with np.errstate(divide='ignore', invalid='ignore'):
        e = np.abs(Ypred - trY)/(trY)
    e[np.isnan(e)] = 0
    e[np.isinf(e)] = 0
    errorByRows = np.mean(e,axis=1)*100
    errorByCols = np.mean(e,axis=0)*100
    print('Error by Rows', np.round(errorByRows, 2).tolist())
    print("Error by Cols", np.round(errorByCols,2).tolist())
    print("error", np.mean(errorByRows))
    return Ypred, regr, scaler1, scaler2, errorByRows, errorByCols

def testing(X,Y, depVars, regr, scaler1, scaler2):
    trX,trY = map(lambda x: list(map(dict2Array, x)), [X,Y])
    features = list(X[0].keys())
    trX = scaler1.fit_transform(trX)
    
    trX,trY = np.array(trX),np.array(trY)
    Ypred = np.clip(regr.predict(trX),0,1e10) 
    #Ypred = scaler2.inverse_transform(Ypred)
    trY[trY<1e-4] = 0
    Ypred[Ypred<1e-4] = 0
    with np.errstate(divide='ignore', invalid='ignore'):
        e = np.abs(Ypred - trY)/(trY)
    e[np.isnan(e)] = 0
    e[np.isinf(e)] = 0
    errorByRows = np.mean(e,axis=1)*100
    errorByCols = np.mean(e,axis=0)*100
    return Ypred, errorByRows, errorByCols

if __name__=='__main__':
    
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
        y = te.treat(x,modelname)['optEff'].water
        #print(y['COD'])
        Y.append(y)
    
    depVars = {feature: [feature] for feature in x.features}
    depVars['TN'] += ['COD']
    depVars['N-NH3'] += ['COD','TN']
    depVars['N-NO3'] += ['COD','TN']
    #depVars['TP'] += ['COD']
    
    
    Ypred, regrs, scaler1, scaler2, ebr, ebc = training(X,Y, depVars)
    
    
    print("\nTESTING")
    X,Y = [],[]
    for i in range(10):
        x = ww.wastewater()
        if random.random() > 0.0:
            x.generateFromOpt(opt)
        else:
            x.simulate(random=True)
        X.append(x.water)
        #print('input wastewater',x.water)
        y = te.treat(x,modelname)['optEff'].water
        #print(y['COD'])
        Y.append(y)
    
    t1 = time.time()
    Ypred, ebr, ebc = testing(X,Y, depVars, regrs,scaler1,scaler2)
    t2 = time.time()
    print('time taken for training and testing in real time', t2-t1,'ms')
    Y2 = list(map(lambda arr: array2Dict(arr, Y[0].keys()), Ypred))
    #print(Y,Y2)
    print('error by rows', ebr)
    print('error by cols', ebc)
    print('mean error', np.mean(ebr), '%')
    print('this sample error', ebr[0], '%')
    for feature in Y[0]:
        print(feature, Y[0][feature], Y2[0][feature])
    
#    for regr in regrs:
#        print(regrs.index(regr),list(Y[0].keys())[regrs.index(regr)],regr._program)
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

