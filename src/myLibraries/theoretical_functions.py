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

    print('c:', c, ', exp:', gamma)
    
    return powerlaw(xdata, c, gamma), c, gamma

# powerlaw_exp_cutoff 
def powerlaw_exp_cutoff(x,c, gamma, sigma):
    y = []
    for i in range(len(x)):
        y.append(c*pow(x[i], - gamma) * pow(sigma, x[i]))
    return y

def fit_powerlaw_exp_cutoff(xdata, ydata):
    popt, pcov = curve_fit(powerlaw_exp_cutoff, xdata, ydata, bounds=(0, [np.inf, np.inf, 1]))
    c = popt[0]
    gamma = popt[1]
    sigma = popt[2]

    print('c:', c, ', exp:', gamma, ', cutoff:', sigma)
    
    return powerlaw_exp_cutoff(xdata, c, gamma, sigma), c, gamma, sigma

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
    
    popt, pcov = curve_fit(lambda x,c1, a1,a2: broken_powerlaw(x,c1, a1,a2, xc), xdata, ydata, maxfev=50000)
    c1 = popt[0]
    a1 = popt[1]
    a2 = popt[2]
    
    c2 = (c1*pow(xc, -a1))/pow(xc, -a2)

    return broken_powerlaw(xdata, c1, a1, a2, xc), c1, c2, a1, a2, xc


def bestBrokenPowelaw(x,y): 
        # Broken powerlaw fit
        x,y = x, y
        y = [a / sum(y) for a in y] # normalization

        xcs, c1s, c2s, a1s, a2s, errs = x, [], [], [], [], []

        for xc in xcs:
                dd, c1, c2, a1, a2, xc = xc_fit_broken_powerlaw(x,y, xc)

                err = sum([pow(abs(dd[i] - y[i]),2) for i in range(len(x))])
                
                c1s.append(c1)
                c2s.append(c2)
                a1s.append(a1)
                a2s.append(a2)
                errs.append(err)
                # draw("broken powerlaw fit", "#_collaborations", "#_authors", ['real', 'fit'], [x, x], [y, dd])
                # draw("loglog broken powerlaw fit", "log(#_collaborations)", "log(#_authors)", ['real', 'fit'], [np.log(x), np.log(x)], [np.log(y), np.log(dd)])

        results = pd.DataFrame({"xc": xcs, "c1": c1s, "c2": c2s, "a1": a1s, "a2": a2s, "err": errs})

        # sorted my err
        best = results.sort_values(by="err",  ascending=True).loc[5]
        xc = best["xc"]
        c1 = best["c1"]
        a1 = best["a1"]
        a2 = best["a2"]

        dd = broken_powerlaw(x, c1, a1, a2, xc)
        # print("broken DD fitting: \n",best)

        return dd, best