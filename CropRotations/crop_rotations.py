import constants, glob, os, pdb, shutil, subprocess, logging, itertools, plots
import pandas as pd
import matplotlib.pyplot as plt
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

# Aggregate years to decades and compute fraction
# of each crop functional type in that decade
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

# Read in data on FAO crop acreages globally
def read_FAO_data():
    try:
        fao_file = pd.ExcelFile(constants.data_dir+os.sep+constants.FAO_FILE)
    except:
        logging.info('Error reading excel file on FAO data')

    return fao_file.parse(constants.FAO_SHEET)

if __name__ == '__main__':
    fao_df   = read_FAO_data()

    out_dec_df = per_CFT_by_decade(fao_df,'United States of America')
    out_ann_df = per_CFT_annual(fao_df,'United States of America')

    out_dec_df = out_dec_df.set_index('functional_crop_type')
    out_dec_df.drop('country_name', axis=1).T.plot(kind='bar',stacked=True,color=plots.get_colors(5))
    plt.show()

    out_ann_df = out_ann_df.reset_index(level=0)
    out_ann_df.drop('country_name', axis=1).T.plot(kind='bar',stacked=True,color=plots.get_colors(5))
    plt.show()


