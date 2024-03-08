import matplotlib.pyplot as plt

# draw a plot with multiple functions (f_lab and y must be arrays)
def draw(title, x_lab, y_lab, x, y, f_lab=[], width=25, height=5):
    
    plt.figure(figsize=(width, height), dpi=80)
    plt.title(title)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    
    for i in range(len(y)):
        if(f_lab != []):
            plt.plot(x, y[i], label=f_lab[i])
        else:
            plt.plot(x, y[i])
        
    plt.xticks(rotation=90)
    
    if(f_lab != []):
        plt.legend(loc='best')

    plt.show()
    
# use this if you have functions with different starting x 
def draw_multi_x(title, x_lab, y_lab, x, y, f_lab=[], width=15, height=5):
    
    plt.figure(figsize=(width, height), dpi=80)
    plt.title(title)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    
    for i in range(len(y)):
        if(f_lab != []):
            plt.plot(x[i], y[i], label=f_lab[i])
        else:
            plt.plot(x[i], y[i])
        
    plt.xticks(rotation=90)
    
    if(f_lab != []):
        plt.legend(loc='best')

    plt.show()