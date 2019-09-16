"""
Filename:    getERA5_prs.py
Author:      Tessa Montini, tmontini@ucsb.edu
Description: Download ERA5 data on pressure levels

- simple download / retrieves one data file / short time range

"""
import cdsapi

# Data directory and file names
datadir = "/Users/tessamontini/Google_Drive/DATA/downloads/"
outfile = "era5_z_500_200901.nc"

# Input parameters
var = 'geopotential'
level = '500'

# Optional parameters
area = [20, -165, -60, -12]  # [N,W,S,E] Default: global
grid = [0.5, 0.5]            # Default: 0.25 x 0.25

# CDS API request
c = cdsapi.Client()
c.retrieve('reanalysis-era5-pressure-levels', 
           {'product_type'  : 'reanalysis',
            'pressure_level': level,
            'variable'      : var,
            'year'          : '2009',
            'month'         : '01',
            'day'           : ['01','02','03',
                               '04','05','06',
                               '07','08','09',
                               '10','11','12',
                               '13','14','15',
                               '16','17','18',
                               '19','20','21',
                               '22','23','24',
                               '25','26','27',
                               '28','29','30',
                               '31'],
            'time'          : ['00:00','06:00',
                               '12:00','18:00'],
            'area'          : area,
            'grid'          : grid,
            'format'        : 'netcdf'
           }, 
           outfile)

print("Download complete: {filename} \n".format(filename=outfile))

