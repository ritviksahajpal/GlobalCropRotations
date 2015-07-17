import constants, glob, os, pdb, shutil, subprocess, logging, itertools
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def iround(x, base = 10):
    return int(base * round(float(x)/base))

# Select data for a country/region by country code or name
def select_data_by_country(df, cnt):
    cnt_df = df[df['country_name'] == cnt]

    return cnt_df

# Aggregate years to decades and compute fraction
# of each crop functional type in that decade
def agg_CFT_by_decade():
    pass

def per_CFT_annual(df,year):
    grp_df = df.groupby(['country_name', 'functional_crop_type']).agg({year: 'sum'})
    pct_df = grp_df.groupby(level=0).apply(lambda x: 100*x/float(x.sum()))

    return pct_df

if __name__ == '__main__':
    # Create empty data frame
    dec_df = pd.DataFrame()
    per_df = pd.DataFrame()

    # Read in data on FAO crop acreages globally
    fao_file = pd.ExcelFile(constants.data_dir+os.sep+constants.FAO_FILE)
    fao_df   = fao_file.parse(constants.FAO_SHEET)

    # Get list of years in FAO data
    list_yrs = fao_df.columns.values[4:]
    # Separate years into decades
    yrs_dec  = np.array([list(g) for k,g in itertools.groupby(list_yrs, lambda i: i // 10)])

    # Select data by country
    out_df   = select_data_by_country(fao_df,'United States of America')
    for dec in yrs_dec:
        dec_name = str(iround(dec[0]))+'s'

        total_ar = np.sum(out_df.ix[:,dec].values)
        dec_df[dec_name] = out_df.ix[:,dec].sum(axis=1)/total_ar * 100

    # Join the decadal dataframe with country and crop functional type name columns
    dec_df     = pd.concat([out_df[['country_name', 'functional_crop_type']],dec_df],axis=1,join='inner')

    for yr in list_yrs:
        df     = per_CFT_annual(out_df,yr)
        per_df = pd.concat([per_df, df], axis=1, join='inner')

    print per_df.head()
    print '----'
    print dec_df.head()
    pdb.set_trace()

    agg_CFT_by_decade(out_df)

