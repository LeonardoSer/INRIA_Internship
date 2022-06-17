import sys
import numpy as np

from scipy.optimize import curve_fit
from myLibraries.events import *
from myLibraries.queries import *

            ##### Theoretichal Trajectory #####



# Theoretichal vertex trajectory for stretched exponential distribution
def theoretical_func(x, a, b, start_x):
    return  pow((a*(np.log(x/start_x)) + 1), b)

# Method to fit the theoretical trajectory to the given average trajectory 
def fit_trajectory(xdata, ydata):
    
    popt, pcov = curve_fit(lambda x, a, b: theoretical_func(x, a, b, xdata[0]), xdata, ydata, maxfev=5000, bounds=([0, 1], [np.inf, np.inf]))
    alpha = popt[0]
    beta = popt[1]

    return theoretical_func(xdata, alpha, beta, np.int64(xdata[0])), alpha, beta 



# Theoretichal Polynomial vertex trajectory for stretched exponential distribution
def poly_theoretical_func(x, a, b, start_x):
    return  (1+a)*pow((x/start_x), b) - a

# Method to fit the theoretical trajectory to the given average trajectory 
def poly_fit_trajectory(xdata, ydata):
    
    popt, pcov = curve_fit(lambda x, a, b: poly_theoretical_func(x, a, b, xdata[0]), xdata, ydata, maxfev=5000, bounds=(0, [np.inf, 0.9]))
    alpha = popt[0]
    beta = popt[1]

    return poly_theoretical_func(xdata, alpha, beta, np.int64(xdata[0])), alpha, beta 


        #### POWERLAW DISTRIBUTION ###
        

# powerlaw 
def powerlaw(x,c, gamma):
    y = []
    for i in range(len(x)):
        y.append(c*pow(x[i], - gamma))
   
    return y

def fit_powerlaw(xdata, ydata):
    popt, pcov = curve_fit(powerlaw, xdata, ydata)
    c = popt[0]
    gamma = popt[1]

    print('c:', c, ', gamma:', gamma)
    
    return powerlaw(xdata, c, gamma), c, gamma

# broken powerlaw
def broken_powerlaw(x,c1, a1,a2, xc):
    y = []
    for i in range(len(x)):
        if(x[i]<xc):
            y.append(c1*pow(x[i], -a1))
        if(x[i]>=xc):
            c2 = (c1*pow(xc, -a1))/pow(xc, -a2)
            y.append(c2*pow(x[i], -a2))

    return y

def xc_fit_broken_powerlaw(xdata, ydata, xc):
    
    popt, pcov = curve_fit(lambda x,c1, a1,a2: broken_powerlaw(x,c1, a1,a2, xc), xdata, ydata)
    c1 = popt[0]
    a1 = popt[1]
    a2 = popt[2]
    
    c2 = (c1*pow(xc, -a1))/pow(xc, -a2)

    return broken_powerlaw(xdata, c1, a1, a2, xc), c1, c2, a1, a2, xc