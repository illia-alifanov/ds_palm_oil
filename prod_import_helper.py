import pandas as pd
import numpy as np
from collections import defaultdict

def getProduction(fileName):
    production_ = pd.read_excel(fileName, 'MonthlyProduction')
    production_['Date'] = production_['Year'].apply(str) + '-' + production_['Month'].apply(str) + '-01'
    production_['Date'] = production_['Date'].apply(pd.to_datetime)
    return production_

def getArea(fileName):
    area_ = pd.read_excel(fileName, 'TotalPlantedArea')
    area_['OTHERPEN'] = area_['KDH'] + 	area_['KTN'] + area_['MLK'] + area_['NSN'] + area_['PNG'] + area_['SGR'] + area_['TRG']
    area_ = area_.rename(columns={'YEAR':'Year'})
    return area_

def getRainfalls(fileName):
    rainfalls_ = pd.read_excel(fileName, 'MonthlyRainfall')

    # initialize month list
    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    # initialize dictionary of dictionaries
    falls_regions = defaultdict(dict)

    for index, row in rainfalls_.iterrows():
      if row.State not in regions:
        continue

      for i, m in enumerate(month, start = 1):
        date_str = str(row['Year']) + '-' + "{:02d}".format(i) + '-01'
        temp = {date_str: row[m]}
        falls_regions[row.State].update(temp)

    result = pd.DataFrame()
    for r in regions:
      if result.empty:
        result = pd.DataFrame.from_dict(falls_regions[r], orient = 'index', columns = [r])
        continue
      else:
        df = pd.DataFrame.from_dict(falls_regions[r], orient = 'index', columns = [r])
      
      result = result.join(df, how = 'outer')

    return result
