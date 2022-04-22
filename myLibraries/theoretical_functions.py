import sys
import numpy as np

from scipy.optimize import curve_fit
from myLibraries.events import *
from myLibraries.queries import *

            ##### Theoretichal Trajectory #####

# Theoretichal vertex trajectory for stretched exponential distribution
def theoretical_func(x, a, b, start_x):
    return  pow((a*(np.log(x/start_x)) + 1), b)

# Theoretichal Polynomial vertex trajectory for stretched exponential distribution
def poly_theoretical_func(x, a, b, start_x):
    return  (1+a)*pow((x/start_x), b) - a

# Method to fit the theoretical trajectory to the given average trajectory 
def fit_trajectory(xdata, ydata):
    
    popt, pcov = curve_fit(lambda x, a, b: theoretical_func(x, a, b, xdata[0]), xdata, ydata, maxfev=5000, bounds=(0, [np.inf, np.inf]))
    alpha = popt[0]
    beta = popt[1]

    return theoretical_func(xdata, alpha, beta, np.int64(xdata[0])), alpha, beta 

# Method to fit the theoretical trajectory to the given average trajectory 
def poly_fit_trajectory(xdata, ydata):
    
    popt, pcov = curve_fit(lambda x, a, b: poly_theoretical_func(x, a, b, xdata[0]), xdata, ydata, maxfev=5000, bounds=(0, [np.inf, 0.9]))
    alpha = popt[0]
    beta = popt[1]

    return poly_theoretical_func(xdata, alpha, beta, np.int64(xdata[0])), alpha, beta 
