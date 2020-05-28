# -*- coding: utf-8 -*-
import numpy as np
import json
import matplotlib.pyplot as plt
import time
import wastewater as ww
import treatmentEffect as te

dict2Array = lambda dictionary : [dictionary[feature] for feature in dictionary.keys()]
array2Dict = lambda array, features: dict(zip(list(features),array))

############
#treatmentEffects
#water and removalRate are numpy arrays.

removal = lambda water, removalRate: np.multiply(water, 1-removalRate/100) 

limit = lambda water, threshold: np.multiply(np.less(water,threshold),water) + np.multiply(1-np.less(water,threshold),np.random.uniform(0,threshold))

shift = lambda water, change: np.clip(water + change, 0, 1e20)

regulate = lambda water, target: target

##############################
evaluate = lambda trX, func, arg: list(map(lambda x: func(x, np.array(arg)), trX))
funcs = [removal, limit, shift, regulate]

def learning(X,Y):
    #X,Y are two lists of dicts.
    trX,trY = map(lambda x: np.array(list(map(dict2Array, x))), [X,Y])
    
    changes = lambda trX,trY: np.clip(np.max(np.abs((trY-trX)/(trX+1e-2)), axis=1),0,1)
    
    pchange = changes(trX,trY)
    optChange = np.mean(pchange)
    
    resX,resY = [], [] 
    i = 0
    for c in pchange:
        if c > optChange:
            resX.append(trX[i].tolist())
            resY.append(trY[i].tolist())
        i += 1
    
    trX,trY = np.array(resX),np.array(resY)
    
    optBounds = dict(zip(X[0].keys(),list(zip(np.percentile(trX,25,axis=0),np.percentile(trX,75,axis=0)))))
    print('OPTBOUNDS',optBounds)
    
#    print('FILTERED',trX,trY)
#    print('LENGTHS',len(trX), len(trY))
#    
    print('\nPCHANGE',pchange)
    print('\nOPTCHANGE',optChange)
#    
    args = map(lambda x:x.tolist(), [(trX-trY)*100/(trX+1e-10), np.max([trX,trY], axis=0), trY-trX, trY])
    args = list(map(lambda arr: np.mean(arr,axis=0).tolist(), args))
    ypreds = map(lambda z: evaluate(trX, *z), zip(funcs,args))
    diff = lambda ypred, trY: np.mean(np.abs(ypred - trY)/(trY+1e-10), axis=0)
    errors = np.array(list(map(lambda ypred: diff(ypred, trY).tolist(), ypreds))) + 1e-10
    probs =  np.round((1/errors)**1/np.sum((1/errors)**1, axis=0),2).tolist()
    return args, ypreds, errors, probs, optBounds
    
def predict(x, args, probs, optBounds):
    #x is a wastewater object
    features = x.features
    x = dict2Array(x.water)
    ypreds = list(map(lambda z: evaluate([x], *z), zip(funcs,args)))[0]
    ypred = np.sum(np.multiply(ypreds, probs),axis=0)
    
#    optMin, optMax = map(np.array,map(list,zip(*optBounds.values())))
#    print('optMinMax', optMin, optMax)
#    print('OPTMINMAX X', list(zip(features,optMin, optMax, x)))
#    optimality = 1 + np.clip(np.median((np.array(x) - optMin) * (optMax-np.array(x))/((optMax-optMin)**2 + 1e-3)),-1,0)
#    
#    print('OPTIMALITY',optimality)
#    ypred = np.array(x) + optimality*(ypred - np.array(x))
    y = array2Dict(ypred, features)
    return ww.wastewater(y)
    
#def learnOptimality(X,Y):
#    #compare X,Y average percentage change, and sort by that, select out the top performing (top 25-percentile) datapoints giving the largest percentage change, analyze the X-boundary. This boundary represents the optimal X-boundary. 
#


#







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
        x.generateFromOpt(opt)
        #x.simulate(random=True)
        X.append(x.water)
        #print('input wastewater',x.water)
        y = te.treat(x,modelname)['optEff'].water
        #print(y['COD'])
        Y.append(y)

    args, ypreds, errors, probs, optBounds = learning(X,Y)
    print('\nTESTING')
    
    
    x = ww.wastewater()
    x.generateFromOpt(opt)
    #x.simulate(random=True)
    ypred = predict(x,args,probs, optBounds)
    
    y = te.treat(x,'厌氧')['optEff']
    print('\nactual y')
    list(map(lambda row: print(row[0][0],round(row[0][1],1),round(row[1][1],1),round(row[2][1],1)), zip(x.water.items(), ypred.water.items(),y.water.items())))
    print('probability distribution')
    print(np.array(probs).T)
    print('args')
    print(np.array(args).T)
    t2 = time.time()
    print('time taken for training and testing in real time', t2-t1,'ms')
   