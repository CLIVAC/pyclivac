"""
Filename:    getERA5_sfc.py
Author:      Tessa Montini, tmontini@ucsb.edu
Description: Download ERA5 data on the surface or single levels

- simple download / retrieves one data file / short time range

"""
import cdsapi

# Data directory and file names
datadir = "/Users/tessamontini/Google_Drive/DATA/downloads/orog/"
outfile = "era5_sfc_orog_spac3.nc"

# Input parameters
var = 'orography'

# Optional parameters
area = [20, -165, -60, -12]  # Default: global
grid = [0.5, 0.5]            # Default: 0.25 x 0.25

# CDS API request
c = cdsapi.Client()
c.retrieve('reanalysis-era5-single-levels', 
           {'product_type'  : 'reanalysis',
            'variable'      : var,
            'year'          : "{0}".format(yr),
            'month'         : '01',
            'day'           : '01',
            'time'          : '00:00',
            'area'          : area,
            'grid'          : grid,
            'format'        : 'netcdf'
           }, 
           outfile)
print("Download complete: {filename} \n".format(filename=outfile))

