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
        ax2.plot(area['Year'], area[r], label=r) #, marker='o'

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

dirname = os.path.dirname(__file__)
fileName = os.path.join(dirname, 'data/palm.xlsx')
regions = ['JHR', 'PHG', 'PRK', 'SBH', 'SWK', 'OTHERPEN']

data_plot()
