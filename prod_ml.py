import os;
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from helper import prepare_production, prepare_area, prepare_production_byyear, form_lag_ts_sample, area_form, forecast_err

from helper import forecast_err
from import_helper import getProduction, getArea, getRainfalls

import sklearn.linear_model as lm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score, KFold

from sklearn.metrics import mean_squared_error
from sklearn.ensemble import AdaBoostRegressor

#from statsmodels.tsa.seasonal import 


def main(fileName, reg_name):
  production = getProduction(fileName)
  region_ts = prepare_production_byyear(production, reg_name)

  #area data processing
  planted_area = getArea(fileName)
  planted_area = prepare_area(planted_area, reg_name)
  planted_area = planted_area.rename(columns={reg_name:'Area'})

  #rainfalls data processing
  rainfals = getRainfalls(fileName)
  rainfals = rainfals.rename(columns={reg_name:'Rainfalls'})
  rainfals['Date'] = list(rainfals.Year.index)
  rainfals = rainfals[['Rainfalls', 'Date']]
  # ml
  data_sample = region_ts
  data_sample = pd.merge(data_sample, rainfals, on = 'Date', how = 'inner')
  x = data_sample[['Rainfalls']]
  y = data_sample[[reg_name]]
  xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.15)

  ada_reg = AdaBoostRegressor(n_estimators=100)
  print(ada_reg)

  ada_reg.fit(xtrain, ytrain)

  ### - cross validataion 
  scores = cross_val_score(ada_reg, xtrain,ytrain,cv=5)
  print("Mean cross-validataion score: %.2f" % scores.mean())

  # k-fold cross validataion 
  kfold = KFold(n_splits=10, shuffle=True)
  kf_cv_scores = cross_val_score(ada_reg, xtrain, ytrain, cv=kfold )
  print("K-fold CV average score: %.2f" % kf_cv_scores.mean())

  # prediction
  ypred = ada_reg.predict(xtest)
  mse = mean_squared_error(ytest,ypred)
  print("MSE: %.2f" % mse)
  print("RMSE: %.2f" % np.sqrt(mse))

  # plotting the result
  x_ax = range(len(ytest))
  plt.plot(x_ax, ytest, color="blue", label="original")
  plt.plot(x_ax, ypred, lw=0.8, color="red", label="predicted")
  plt.legend()
  plt.show()

dirname = os.path.dirname(__file__)
fileName = os.path.join(dirname, 'data/palm.xlsx')

reg_name = 'JHR'
main(fileName, reg_name)
