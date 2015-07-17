import constants, logging, sys, os, errno

###############################################################################
#
#
#
###############################################################################
def make_dir_if_missing(d):
    try:
        os.makedirs(d)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise