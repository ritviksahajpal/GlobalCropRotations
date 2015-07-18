import constants, glob, os, pdb, shutil, subprocess, logging, itertools, plots, multiprocessing
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

def iround(x, base = 10):
    return int(base * round(float(x)/base))

def get_list_decades(lyrs):
    return np.array([list(g) for k,g in itertools.groupby(lyrs, lambda i: i // 10)])

def get_list_yrs(df):
    return df.columns.values[4:]

# Select data for a country/region by country code or name
def select_data_by_country(df, cnt):
    cnt_df = df[df['country_name'] == cnt]

    return cnt_df


###############################################################################
# Aggregate years to decades and compute fraction
# of each crop functional type in that decade
#
###############################################################################
def per_CFT_by_decade(df,cnt_name):
    dec_df = pd.DataFrame()

    # Get list of years in FAO data
    list_yrs = get_list_yrs(df)

    # Separate years into decades
    yrs_dec  = get_list_decades(list_yrs)

    # Select data by country
    out_df   = select_data_by_country(df,cnt_name)

    for dec in yrs_dec:
        dec_name = str(iround(dec[0]))+'s'

        total_ar = np.sum(out_df.ix[:,dec].values)
        dec_df[dec_name] = out_df.ix[:,dec].sum(axis=1)/total_ar * 100

    # Join the decadal dataframe with country and crop functional type name columns
    dec_df     = pd.concat([out_df[['country_name', 'functional_crop_type']],dec_df],axis=1,join='inner')

    return dec_df

###############################################################################
# per_CFT_annual
#
#
###############################################################################
def per_CFT_annual(df,cnt_name):
    per_df = pd.DataFrame()

    # Select data by country
    out_df   = select_data_by_country(df,cnt_name)

    # Get list of years in FAO data
    list_yrs = get_list_yrs(out_df)

    for yr in list_yrs:
        grp_df = out_df.groupby(['country_name', 'functional_crop_type']).agg({yr: 'sum'})
        pct_df = grp_df.groupby(level=0).apply(lambda x: 100*x/float(x.sum()))

        per_df = pd.concat([per_df, pct_df], axis=1, join='inner')

    return per_df


###############################################################################
# Read in data on FAO crop acreages globally
#
#
###############################################################################
def read_FAO_data():
    try:
        fao_file = pd.ExcelFile(constants.data_dir+os.sep+constants.FAO_FILE)
    except:
        logging.info('Error reading excel file on FAO data')

    return fao_file.parse(constants.FAO_SHEET)

###############################################################################
# plot_cnt_decade
#
#
###############################################################################
def plot_cnt_decade(inp_fao_df,cnt):
    out_dec_df = per_CFT_by_decade(inp_fao_df,cnt)
    out_ann_df = per_CFT_annual(inp_fao_df,cnt)

    out_dec_df = out_dec_df.set_index('functional_crop_type')
    ax = out_dec_df.drop('country_name', axis=1).T.plot(kind='bar',stacked=True,color=plots.get_colors(5),linewidth=0)

    plots.simple_axis(ax) # Simple axis, no axis on top and right of plot

    # Transparent legend in lower left corner
    leg = plt.legend(loc='lower left',fancybox=None)
    leg.get_frame().set_linewidth(0.0)
    leg.get_frame().set_alpha(0.5)

    # Set X and Y axis labels and title
    ax.set_title(cnt)
    ax.set_xlabel('')
    plt.ylim(ymax = 100)
    ax.set_ylabel('Percentage of cropland area \noccupied by each crop functional type')
    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    yticks = mtick.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(yticks)

    # remove ticks from X axis
    plt.tick_params(\
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off')         # ticks along the top edge are off

    # Rotate the X axis labels to be horizontal
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=0)

    plt.tight_layout()
    plt.savefig(constants.out_dir+os.sep+cnt+'.png', bbox_inches='tight', dpi=600)
    plt.close()

###############################################################################
# plot_cnt_mean_decade
#
#
###############################################################################
def plot_cnt_mean_decade(inp_fao_df,cnt):
    out_dec_df = mean_CFT_by_decade(inp_fao_df,cnt)

    out_dec_df = out_dec_df.set_index('functional_crop_type')
    ax = out_dec_df.drop('country_name', axis=1).T.plot(kind='bar',stacked=True,color=plots.get_colors(5),linewidth=0)

    plots.simple_axis(ax) # Simple axis, no axis on top and right of plot

    # Transparent legend in lower left corner
    leg = plt.legend(loc='lower left',fancybox=None)
    leg.get_frame().set_linewidth(0.0)
    leg.get_frame().set_alpha(0.5)

    # Set X and Y axis labels and title
    ax.set_title(cnt)
    ax.set_xlabel('')
    plt.ylim(ymax = 100)
    ax.set_ylabel('Mean crop functional type area in each decade')
    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    yticks = mtick.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(yticks)

    # remove ticks from X axis
    plt.tick_params(\
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off')         # ticks along the top edge are off

    # Rotate the X axis labels to be horizontal
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=0)

    plt.tight_layout()
    plt.savefig(constants.out_dir+os.sep+'Mean_'+cnt+'.png', bbox_inches='tight', dpi=600)
    plt.close()

if __name__ == '__main__':
    fao_df   = read_FAO_data()
    list_cnt = fao_df['country_name'].unique()

    for ctry in list_cnt:
        print ctry
        logging.info(ctry)

        plot_cnt_decade(fao_df, ctry)

    print 'Done'

    # out_ann_df = out_ann_df.reset_index(level=0)
    # out_ann_df.drop('country_name', axis=1).T.plot(kind='bar',stacked=True,color=plots.get_colors(5))
    # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.09),ncol=5)
    # plt.show()
    #
    #
