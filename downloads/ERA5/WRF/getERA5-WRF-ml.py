#!/usr/bin/env python
"""
Filename:    getERA5-WRF-ml.py
Author:      Tessa Montini, tmontini@ucsb.edu
Description: Download ERA5 model level data for initializing WRF

conda activate cds

"""
import cdsapi

# Date/Time
DATE1 = 20180706
DATE2 = 20180707
TIMES = '00/to/23/by/3'

# Area
NORTH = 60
WEST  = -150
SOUTH = 10
EAST  = -100

# Data directory and filename
DATADIR = '/home/sbarc/students/montini/data/downloads'
OUTFILE = f'{DATADIR}/ERA5_ml_{DATE1}_{DATE2}.grib'


# API Request 
c = cdsapi.Client()
c.retrieve('reanalysis-era5-complete',{
    'class'  : 'ea',
    'expver' : '1',
    'stream' : 'oper',
    'type'   : 'an',    
    'param'  : '129/130/131/132/133/152',
    'levtype' : 'ml',
    'levelist': '1/to/137',
    'date' : f'{DATE1}/to/{DATE2}',
    'time' : TIMES,
    'area' : f'{NORTH}/{WEST}/{SOUTH}/{EAST}',
    'grid' : "0.25/0.25",
}, OUTFILE)

print(OUTFILE)
