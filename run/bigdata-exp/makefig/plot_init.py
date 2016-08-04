import matplotlib.pyplot as plt
def draw_init():
    params ={\
        'backend': 'GTKAgg',
        
        #'font.fontname':'Calibri',
        'font.weight': 900,
        'font.family': 'serif',
        'font.serif': ['Times', 'Palatino', 'New Century Schoolbook', 'Bookman', 'Computer Modern Roman'],
        'font.sans-serif' : ['Helvetica', 'Avant Garde', 'Computer Modern Sans serif'],
    #font.cursive       : Zapf Chancery
    #font.monospace     : Courier, Computer Modern Typewriter
        'text.usetex': False,
        
        'axes.labelsize': 12,
        'axes.linewidth': .75,
        
        #'figure.figsize': (8,6),
        'figure.figsize': (4,3),
        'figure.subplot.left' : 0.175,
        'figure.subplot.right': 0.95,
        'figure.subplot.bottom': 0.15,
        'figure.subplot.top': .95,
        
        'figure.dpi':150,
        
        'text.fontsize': 5,
        'legend.fontsize': 10,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        
        'lines.linewidth':1.25,
        'lines.markersize'  : 3,
        'lines.markeredgewidth': 0.1,
        'savefig.dpi':600,
        }
    
    plt.rcParams.update(params)



