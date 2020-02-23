#import warnings
#import itertools
import numpy as np
import matplotlib.pyplot as plt
#warnings.filterwarnings("ignore")
#plt.style.use('fivethirtyeight')
import pandas as pd
#import statsmodels.api as sm
#import matplotlib
import array as arr


def getExcelSheet(fileName, sheetName):
    production_ = pd.read_excel(fileName, sheetName)

    production_['Date'] = production_['Year'].apply(str) + '-' + production_['Month'].apply(str) + '-01'
    production_['Date'] = production_['Date'].apply(pd.to_datetime)
    return production_

def main():
    fileName = 'D:\projects\dsacademy\palmoil\data\palm.xlsx'
    sheetName = 'MonthlyProduction'
    production = getExcelSheet(fileName, sheetName)

    regions = ['JHR', 'PHG', 'PRK', 'SBH', 'SWK', 'OTHERPEN']

    for r in regions:
        plt.plot(production['Date'], production[r], label=r) #, marker='o'
 
    
    plt.xlabel('Production date')
    plt.ylabel('Production vs Date')
    plt.grid(True)
    plt.legend(loc='lower right')

    plt.show()

    #print(production)

main()

