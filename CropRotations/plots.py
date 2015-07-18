import matplotlib, constants
import brewer2mpl
from matplotlib import rcParams

def set_matplotlib_params():
    """
    Set matplotlib defaults to nicer values
    """
    # rcParams dict
    rcParams['mathtext.default'] ='regular'
    rcParams['axes.labelsize']   = 11
    rcParams['xtick.labelsize']  = 11
    rcParams['ytick.labelsize']  = 11
    rcParams['legend.fontsize']  = 11
    rcParams['font.family']      = 'sans-serif'
    rcParams['font.serif']       = ['Helvetica']
    #rcParams['figure.figsize']   = 7.3, 4.2

def get_colors(num_colors):
    """
    Get colorbrewer colors, which are nicer
    """
    bmap = brewer2mpl.get_map('Set2','qualitative',num_colors,reverse=True)
    return bmap.mpl_colors

def simple_axis(ax):
    """
    Remove spines from top and right, set max value of y-axis
    """
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

def simple_legend():
    leg = plt.legend(loc='upper left',fancybox=None)
    leg.get_frame().set_linewidth(0.0)
    leg.get_frame().set_alpha(0.5)


