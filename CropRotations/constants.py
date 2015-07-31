import os, logging, multiprocessing, pdb, ast, util
from ConfigParser import SafeConfigParser

# Parse config file
parser = SafeConfigParser()
parser.read('config_rotations.txt')

FAO_REGION_CODE = 350

###############################################################################
# User modifiable values
#
#
###############################################################################
START_YR    = parser.getint('PARAMETERS','START_YR')                  # Starting year of weather data
END_YR      = parser.getint('PARAMETERS','END_YR')                    # Ending year of weather data
TAG         = parser.get('PROJECT','TAG')                             # Tag of NARR folder
FAO_FILE    = parser.get('PROJECT','fao_data')
FAO_SHEET   = parser.get('PROJECT','fao_sheet')
RAW_FAO     = parser.get('PROJECT','raw_fao_data')
RAW_FAO_SHT = parser.get('PROJECT','raw_fao_shet')
CROP_LUP    = parser.get('PROJECT','crop_lup')
CROP_LUP_SHT= parser.get('PROJECT','crop_lup_sht')
PROJ_NAME   = parser.get('PROJECT','project_name')

# Directories
data_dir    = parser.get('PATHS','data_dir')+os.sep
out_dir     = parser.get('PATHS','out_dir')+os.sep+PROJ_NAME+os.sep

# Create directories
util.make_dir_if_missing(data_dir)
util.make_dir_if_missing(out_dir)

# Logging
LOG_FILENAME   = out_dir+os.sep+'Log_'+TAG+'.txt'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,\
                    format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',\
                    datefmt="%m-%d %H:%M") # Logging levels are DEBUG, INFO, WARNING, ERROR, and CRITICAL