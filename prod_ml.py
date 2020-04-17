import os
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
from sklearn.metrics import explained_variance_score
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor

#from statsmodels.tsa.seasonal import

def plot_feature_importances(feature_importances, title, feature_names):
  # Normalize the importance values 
  feature_importances = 100.0 * (feature_importances / max(feature_importances))

  # Sort the values and flip them
  index_sorted = np.flipud(np.argsort(feature_importances))

  # Arrange the X ticks
  pos = np.arange(index_sorted.shape[0]) + 0.5

  # Plot the bar graph
  plt.figure()
  plt.bar(pos, feature_importances[index_sorted], align='center')
  plt.xticks(pos, feature_names[index_sorted])
  plt.ylabel('Relative Importance')
  plt.title(title)
  plt.show()

def main(fileName, reg_name):
  #production = getProduction(fileName)
  #region_ts = prepare_production_byyear(production, reg_name)

  ##area data processing
  #planted_area = getArea(fileName)
  #planted_area = prepare_area(planted_area, reg_name)
  #planted_area = planted_area.rename(columns={reg_name:'Area'})

  ##rainfalls data processing
  #rainfals = getRainfalls(fileName)
  #rainfals = rainfals.rename(columns={reg_name:'Rainfalls'})
  #rainfals['Date'] = list(rainfals.Year.index)
  #rainfals = rainfals[['Rainfalls', 'Date']]
  ## ml
  #data_sample = region_ts
  #data_sample = pd.merge(data_sample, rainfals, on = 'Date', how = 'inner')

  #production data processing
  production = getProduction(fileName)
  print(production.head(10))
  region_ts = prepare_production_byyear(production, reg_name)
  
  
  #production ts decomposition
  from statsmodels.tsa.seasonal import seasonal_decompose
  region_ts = region_ts.set_index('Date')
  ts_seasonal = seasonal_decompose(region_ts[reg_name]).seasonal
  region_ts[reg_name] = region_ts[reg_name] - ts_seasonal

  #form laged data. Lag value can be validated as well
  print(reg_name + ' mines seasonal component')
  print(region_ts.head(10))
  data_sample =  form_lag_ts_sample(region_ts, reg_name, 3)
  
  data_sample['season_value'] = ts_seasonal

  #area data processing
  planted_area = getArea(fileName)
  planted_area = prepare_area(planted_area, reg_name)
  planted_area = planted_area.rename(columns={reg_name:'Area'})

  #rainfalls data processing
  rainfals = getRainfalls(fileName)
  rainfals = rainfals.rename(columns={reg_name:'Rainfalls'})

  #create dataset for regression 
  data_sample = pd.merge(data_sample, planted_area, on = 'Year', how = 'left')
  data_sample = pd.merge(data_sample, rainfals, on = 'Year', how = 'left')

  x = data_sample[['Rainfalls', 'Area']]
  y = data_sample[[reg_name]]
  xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.15)

  rng = np.random.RandomState(1)
  #Fit regression model
  regr_1 = DecisionTreeRegressor(max_depth = 4)

  ab_regressor = AdaBoostRegressor(DecisionTreeRegressor(max_depth=4),
                        n_estimators=300, random_state=rng)

  regr_1.fit(xtrain, ytrain)
  ab_regressor.fit(xtrain, ytrain)

  # Evaluate performance of AdaBoost
  y_pred = ab_regressor.predict(xtest)
  forecast = pd.Series(y_pred, index=data_sample.index)

  mse = mean_squared_error(ytest, forecast)
  evs = explained_variance_score(ytest, forecast) 
  print("\n#### AdaBoost performance ####")
  print(("Mean squared error =", round(mse, 2)))
  print(("Explained variance score =", round(evs, 2)))

  plt.plot(ytest)
  plt.plot(forecast, color = 'red')
  plt.show()
  #indices = [0, 1]
  #labels = np.array(['Rainfalls', 'Area'])[indices]
  #plot_feature_importances(ab_regressor.feature_importances_, 
  #          'AdaBoost regressor', labels)

dirname = os.path.dirname(__file__)
fileName = os.path.join(dirname, 'data/palm.xlsx')

reg_name = 'JHR'
main(fileName, reg_name)
