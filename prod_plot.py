import os;
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings

from helper import prepare_production
from helper import forecast_err

from import_helper import getProduction, getArea, getRainfalls



def data_plot():
    #------- production
    production = getProduction(fileName)

    #make a little extra space between the subplots

    for r in regions:
        plt.plot(production['Date'], production[r], label=r) #, marker='o'
 
    plt.title('Production vs time')
    plt.xlabel('Time')
    plt.ylabel('Production')
    plt.grid(True)
    plt.legend(loc='upper left')
    plt.show()
    
    ##------- area 
    area = getArea(fileName)
    for r in regions:
        plt.plot(area['Year'], area[r], label=r) #, marker='o'

    plt.title('Area vs year')
    plt.xlabel('Year')
    plt.ylabel('Area')
    plt.grid(True)
    plt.legend(loc='upper left')
    plt.show()

    #rainfalls
    rainfalls = getRainfalls(fileName)

    rainfalls.reset_index()
    for r in regions:
        plt.plot(rainfalls.index, rainfalls[r], label=r) #, marker='o'

    plt.title('Rainfalls vs time')
    plt.xlabel('Time')
    plt.ylabel('Rainfalls')
    plt.grid(True)
    plt.legend(loc='upper left')
    plt.show()

dirname = os.path.dirname(__file__)
fileName = os.path.join(dirname, 'data/palm.xlsx')
regions = ['JHR', 'PHG', 'PRK', 'SBH', 'SWK', 'OTHERPEN']

data_plot()
