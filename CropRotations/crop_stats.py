import constants, glob, os, pdb, shutil, subprocess, logging, itertools, plots, multiprocessing
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

###############################################################################
# Read in data on raw FAO crop acreages globally
#
#
###############################################################################
def read_raw_FAO_data():
    try:
        fao_file = pd.ExcelFile(constants.data_dir+os.sep+constants.RAW_FAO)
    except:
        logging.info('Error reading excel file on FAO data')

    df = fao_file.parse(constants.RAW_FAO_SHT)

    # Drop rows of type Y1961F...Y2013F
    drop_rows = ['Y'+str(x)+'F' for x in range(constants.START_YR,constants.END_YR+1)]
    for row in drop_rows:
        df.drop(row, axis=1, inplace=True)

    # Keep only countries drop data from regions also drop China (country code: 351)
    df.drop(df[df['Country Code'] >= constants.FAO_REGION_CODE].index, inplace=True)

    # Replace NA's by 0 in valid rows and compute sum of area in each row
    vld_rows = ['Y'+str(x) for x in range(constants.START_YR,constants.END_YR+1)]

    df.fillna(0,inplace=True)
    df['sum_area'] = df[vld_rows].sum(axis=1)

    return df

###############################################################################
# Read lookup table of crops
#
#
###############################################################################
def read_crop_lup():
    try:
        crp_file = pd.ExcelFile(constants.data_dir+os.sep+constants.CROP_LUP)
    except:
        logging.info('Error reading excel file on crop lookup data')

    return crp_file.parse(constants.CROP_LUP_SHT)


def plot_top_crops_by_area():
    pass

def plot_top_countries_by_crops():
    pass

if __name__ == '__main__':
    raw_fao_df = read_raw_FAO_data()
    crop_df    = read_crop_lup()

    raw_fao_df = pd.merge(raw_fao_df, crop_df, how='inner', on=['Item Code', 'Item Code'])

    # Select subset df with only Item, Country code and area sum
    sub_df = raw_fao_df[['Country','Item','sum_area']]

    grp_crop = sub_df.groupby('Item').sum().sort('sum_area',ascending=False)
    grp_crop['pct'] = sub_df.groupby('Item').sum()*100.0/sub_df.groupby('Item').sum().sum()

    grp_cnt = sub_df.groupby('Country').sum().sort('sum_area',ascending=False)
    grp_cnt['pct'] = sub_df.groupby('Country').sum()*100.0/sub_df.groupby('Country').sum().sum()

    print grp_crop.head(20)
    print '----'
    print grp_cnt.head(20)

