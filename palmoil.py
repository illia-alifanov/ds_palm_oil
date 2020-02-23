#import warnings
#import itertools
import numpy as np
import matplotlib.pyplot as plt
#warnings.filterwarnings("ignore")
#plt.style.use('fivethirtyeight')
import pandas as pd
#import statsmodels.api as sm
import matplotlib


def getExcelSheet(fileName, sheetName):
    production_ = pd.read_excel(fileName, sheetName)

    production_['date'] = production_['Year'].apply(str) + '-' + production_['Month'].apply(str) + '-01'
    production_['date'] = production_['date'].apply(pd.to_datetime)
    return production_

def main():
    fileName = 'D:\projects\dsacademy\palmoil\data\palm.xlsx'
    sheetName = 'MonthlyProduction'
    production = getExcelSheet(fileName, sheetName)


    print(production)

main()

