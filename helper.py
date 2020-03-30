import pandas as pd
import numpy as np

def prepare_production(_production, reg_name):
  ts = _production[['Date', reg_name]]
  ts = ts.set_index('Date')
  dp = [0]
  reg_prod = ts[reg_name]
  for i in range(1, len(reg_prod)):
    dp = dp + [reg_prod[i] - reg_prod[i-1]]

  ts['diff'] = dp
  print(ts.head(10))
  return ts
  


def forecast_err(forecast, fact):
    forecast = np.array(forecast)
    fact = np.array(fact)
    mapes = np.abs((forecast-fact)/fact)
    return np.mean(mapes)

  
def form_lag_ts_sample(dataset, ts_name, window):
    names = ['lag_{0}'.format(i) for i in range(window, 0, -1)]
    names.append(ts_name)
    # names = names + list(dataset.columns)
    ts_sample = pd.DataFrame(columns=names, index=dataset.index[window:])
    # ts_sample[list(dataset.columns)]
    for i in range(window, len(dataset.index)):
        inds = [dataset.index[j] for j in range(i - window, i+1)]
        temp = [dataset[ts_name][ind] for ind in inds]
        ts_sample.loc[dataset.index[i]] = temp
    return ts_sample

def area_form(planted_area):
    planted_area = planted_area[['YEAR', 'JH', 'KD', 'KLT', 'MLC', 'nSB', 'PH', 'PN', 'PRK', 'SLG', 'TGN', 'Pmalay', 'SBH', 'SWK', 'E Malay']]
    area_ = pd.DataFrame(columns=['Region', 'Year', 'Area_npa'])

    for r in planted_area.columns[1:]:
        temp = planted_area[['YEAR', r]]
        temp['Region'] = pd.Series([r]*len(temp), index=temp.index)
        temp.columns = ['Year', 'Area_npa', 'Region']

        # temp = temp.fillna(0)
        temp.Year = temp.Year.astype(int)
        temp = temp.reset_index()
        temp = temp.sort_values(['Year'])
        temp['Area_npa'] = [str(x).replace(' ', '') for x in temp.Area_npa]
        temp.Area_npa = temp.Area_npa.astype(float)
        area_ = area_.append(temp[['Region', 'Year', 'Area_npa']])
    print(area_.shape)
    otherPen = ['KD', 'KLT', 'MLC', 'nSB', 'PN', 'SLG', 'TGN']
    otherPen_df = area_[area_.Region.isin(otherPen)][['Year', 'Area_npa']]
    otherPen_groups = otherPen_df.groupby('Year').sum().reset_index()
    otherPen_groups['Region'] = pd.Series(['OtherPEN'] * len(otherPen_groups), index=otherPen_groups.index)
    area_ = area_.append(otherPen_groups)
    area_.Year = area_.Year.astype(int)
    return area_
