import matplotlib.pyplot as plt
import numpy as np

class Logger:
    
    
    def __init__(self):
        self.data = {}
    
    def log(self, dataset, x, y):
        
        if dataset not in self.data.keys():
            self.data[dataset] = ([],[])
        
        self.data[dataset][0].append(x)
        self.data[dataset][1].append(y)
    
    def plot(self, datasets, xlabel=None, ylabel=None, title=None, grid=True, xlog = False, ylog=False):
        
        for dataset in datasets:
            x = np.asarray( self.data[dataset][0] )
            y = np.asarray( self.data[dataset][1] )
            plt.plot( x, y, label=dataset )
        
        plt.legend()
        
        plt.xlabel( xlabel )
        plt.ylabel( ylabel )
        
        plt.title( title )
        
        plt.grid( grid )
        
        if xlog is True:
            plt.xscale('log')
        else:
            plt.xscale('linear')
        
        if ylog is True:
            plt.yscale('log')
        else:
            plt.yscale('linear')
        
        plt.show()
