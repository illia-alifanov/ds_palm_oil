import os;
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings

from helper import prepare_production
from helper import forecast_err

from prod_import_helper import getProduction, getArea, getRainfalls

from statsmodels.tsa.seasonal import seasonal_decompose

#import statsmodels.api as sm
#import array as arr


def data_plot():
    #------- production
    production = getProduction(fileName)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    #make a little extra space between the subplots
    fig.subplots_adjust(hspace=0.5)

    for r in regions:
        ax1.plot(production['Date'], production[r], label=r) #, marker='o'
 
    ax1.set_title('Production vs time')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Production')
    ax1.grid(True)
    ax1.legend(loc='upper left')
    
    #------- area 
    area = getArea(fileName)
    for r in regions:
        ax2.plot(area['YEAR'], area[r], label=r) #, marker='o'

    ax2.set_title('Area vs year')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Area')
    ax2.grid(True)
    ax2.legend(loc='upper left')

    #rainfalls
    rainfalls = getRainfalls(fileName)

    rainfalls.reset_index()
    for r in regions:
        ax3.plot(rainfalls.index, rainfalls[r], label=r) #, marker='o'

    ax3.set_title('Rainfalls vs time')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Rainfalls')
    ax3.grid(True)
    ax3.legend(loc='upper left')

    plt.show()

def run_arima(reg_name):
  production = getProduction(fileName)
  print(production.head(10))
  ts = prepare_production(production, reg_name)
  
  result = seasonal_decompose(ts[reg_name], model='additive')
  result.plot()
  plt.show()

  ts_decompose = seasonal_decompose(ts['diff'], model='additive')
  #ts_decompose.plot()
  #plt.show()

  ts_resid = ts['diff'] - ts_decompose.seasonal
  ts_resid_decompose = seasonal_decompose(ts_resid, model='additive')
  ts_resid_decompose.plot()
  plt.show()

  from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
  plot_acf(ts_resid)
  plot_pacf(ts_resid)
  plt.show()

  # train ARIMA
  from statsmodels.tsa.arima_model import ARIMA

  p_range = q_range = k_range = [0, 1, 2, 3]
  validation_size = 20
  prediction_window = 6
  order_params = (0, 0, 0)
  err = 140000
  for p in p_range:
      for q in q_range:
          for k in k_range:
              pqk_err = 0
              is_built = True
              for ind in range(len(ts_resid)-validation_size, len(ts_resid) - prediction_window):
                  try:
                      warnings.filterwarnings('ignore')
                      model_arima = ARIMA(ts_resid.head(ind-1), order=(p, k, q)).fit(disp=0)
                      warnings.filterwarnings('ignore')
                      arima_forecast = model_arima.forecast(steps=prediction_window)[0]
                      temp_err = forecast_err(arima_forecast, ts_resid.tail(len(ts_resid) - ind).head(prediction_window))
                      pqk_err = pqk_err + temp_err
                  except:
                      is_built = False
                      break
              if is_built:
                  print(p,q,k,pqk_err/14)
              if pqk_err < err and is_built:
                  err = pqk_err
                  order_params = (p,k,q)

  print(order_params, err)
  
  # show test interval forecast to plan
  model_arima = ARIMA(ts_resid.head(len(ts_resid) - prediction_window -1), order=order_params).fit(disp=0)
  warnings.filterwarnings('ignore')
  arima_forecast = model_arima.forecast(steps=prediction_window)[0]
  test_ts = ts_resid.tail(prediction_window)
  forecast = pd.Series(arima_forecast, index=test_ts.index)
  plt.plot(test_ts)
  plt.plot(forecast, color = 'red')
  plt.show()

  # show ARIMA result #(3,0,1)
  model = ARIMA(ts_resid, order=order_params)
  model_fit = model.fit(disp=0)
  output = model_fit.predict()

  plt.plot(ts_resid)
  plt.plot(output, color='red')
  plt.show()
#-------------------

dirname = os.path.dirname(__file__)
fileName = os.path.join(dirname, 'data/palm.xlsx')
regions = ['JHR', 'PHG', 'PRK', 'SBH', 'SWK', 'OTHERPEN']

#data_plot()
run_arima('JHR')
