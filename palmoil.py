
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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
    #https://www.geeksforgeeks.org/create-a-list-from-rows-in-pandas-dataframe/
    rainfalls_ = []

    return rainfalls_


def main():
    #------- production
    production = getProduction()

    regions = ['JHR', 'PHG', 'PRK', 'SBH', 'SWK', 'OTHERPEN']

    fig, (ax1, ax2) = plt.subplots(2, 1)
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

    plt.show()

    
#
fileName = 'D:\projects\dsacademy\palmoil\data\palm.xlsx'
plt.style.use('fivethirtyeight')

main()

