import os;
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as ss

from helper import prepare_production, prepare_area, prepare_production_byyear, form_lag_ts_sample, area_form, forecast_err

from helper import forecast_err
from prod_import_helper import getProduction, getArea, getRainfalls

import sklearn.linear_model as lm

from statsmodels.tsa.seasonal import seasonal_decompose

def mae_calc(model, validation, fact_values):
    pred = model.predict(validation)
    fact_values = np.array(fact_values)
    diff = [abs((pred[i] - fact_values[i])/fact_values[i]) for i in range(0, len(pred))]
    return sum(diff) / len(pred)

def main(fileName, reg_name):

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
  #data_sample = pd.merge(data_sample, planted_area, on = 'Year', how = 'left')
  data_sample = pd.merge(data_sample, rainfals, on = 'Year', how = 'left')

  validation_size = 20
  prediction_window = 6
  err = []

  train_set = data_sample.head(len(data_sample) - prediction_window-1)
  test_set = data_sample.tail(prediction_window)

  #linear reression validation with step = 1
  for ind in range(len(train_set) - validation_size, len(train_set) - prediction_window):
      train = train_set.head(ind-1)
      validation = train_set.tail(len(train_set) - ind).head(prediction_window)
      target_train = train[reg_name]
      train = train.drop([reg_name], axis=1)
      target_valid = validation[reg_name]
      validation = validation.drop([reg_name], axis=1)

      # linear regression
      regr = lm.LinearRegression()
      regr.fit(train, target_train)
      err.append(mae_calc(regr, validation, target_valid))

  print('**** validation error (MAPE) is {0}'.format(np.mean(err)))

  regr = lm.LinearRegression()
  regr.fit(train_set.drop([reg_name], axis=1), train_set[reg_name])
  test_err = mae_calc(regr, test_set.drop([reg_name], axis=1), test_set[reg_name])
  print('**** test error (MAPE) is {0}'.format(test_err))

  pred = regr.predict(data_sample.drop([reg_name], axis=1))
  forecast = pd.Series(pred, index=data_sample.index)
  plt.plot(data_sample[reg_name])
  plt.plot(forecast, color = 'red')
  plt.show()


dirname = os.path.dirname(__file__)
fileName = os.path.join(dirname, 'data/palm.xlsx')

reg_name = 'JHR'
main(fileName, reg_name)