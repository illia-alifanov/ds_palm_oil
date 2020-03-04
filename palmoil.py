
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from collections import defaultdict

#import warnings
#import itertools
#warnings.filterwarnings("ignore")
#import statsmodels.api as sm
#import matplotlib
#import array as arr


def getProduction():
    production_ = pd.read_excel(fileName, 'MonthlyProduction')
    production_['Date'] = production_['Year'].apply(str) + '-' + production_['Month'].apply(str) + '-01'
    production_['Date'] = production_['Date'].apply(pd.to_datetime)
    return production_

def getArea():
    area_ = pd.read_excel(fileName, 'TotalPlantedArea')
    area_['OTHERPEN'] = area_['KDH'] + 	area_['KTN'] + area_['MLK'] + area_['NSN'] + area_['PNG'] + area_['SGR'] + area_['TRG']
    return area_

def getRainfalls():
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
        new_data = {date_str: row[m]}
        falls_regions[row.State].update(new_data)

    result = pd.DataFrame()
    for r in regions:
      columns_list = [r]

      if result.empty:
        result = pd.DataFrame.from_dict(falls_regions[r], orient = 'index', columns = [r])
        continue
      else:
        df = pd.DataFrame.from_dict(falls_regions[r], orient = 'index', columns = [r])
      
      result = result.join(df, how = 'outer')

    return result


def main():

    #------- production
    production = getProduction()

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
    area = getArea()
    for r in regions:
        ax2.plot(area['YEAR'], area[r], label=r) #, marker='o'

    ax2.set_title('Area vs year')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Area')
    ax2.grid(True)
    ax2.legend(loc='upper left')

    #rainfalls
    rainfalls = getRainfalls()

    rainfalls.reset_index()
    for r in regions:
        ax3.plot(rainfalls.index, rainfalls[r], label=r) #, marker='o'

    ax3.set_title('Rainfalls vs time')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Rainfalls')
    ax3.grid(True)
    ax3.legend(loc='upper left')

    plt.show()
    

#fileName = 'D:\projects\dsacademy\palmoil\data\palm.xlsx'
fileName = 'C:\DriveD\dsprojects\ds_palm_oil\data\palm.xlsx'
regions = ['JHR', 'PHG', 'PRK', 'SBH', 'SWK', 'OTHERPEN']
plt.style.use('fivethirtyeight')

main()

