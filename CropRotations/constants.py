import os, logging, datetime, multiprocessing, pdb, ast, util
from ConfigParser import SafeConfigParser

# Parse config file
parser = SafeConfigParser()
parser.read('config_rotations.txt')

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

# Directories
data_dir    = parser.get('PATHS','data_dir')+os.sep
out_dir     = parser.get('PATHS','out_dir')+os.sep+parser.get('PROJECT','project_name')+os.sep

# Create directories
util.make_dir_if_missing(data_dir)
util.make_dir_if_missing(out_dir)

# Logging
LOG_FILENAME   = out_dir+os.sep+'Log_'+TAG+'.txt'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,\
                    format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',\
                    datefmt="%m-%d %H:%M") # Logging levels are DEBUG, INFO, WARNING, ERROR, and CRITICAL