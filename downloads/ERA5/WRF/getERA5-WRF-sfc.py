#!/usr/bin/env python

"""
Filename:    getERA5-WRF-sfc.py
Author:      Tessa Montini, tmontini@ucsb.edu
Description: Download ERA5 surface data for initializing WRF

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
DATADIR = '/home/sbarc/students/montini/data/downloads/'
OUTFILE = f'{DATADIR}/ERA5_sfc_{DATE1}_{DATE2}.grib'


# API Request 
c = cdsapi.Client()
c.retrieve('reanalysis-era5-complete',{
    'class'   : 'ea',
    'expver'  : '1',
    'stream'  : 'oper',
    'type'    : 'an',    
    'param'   : 'msl/sp/skt/2t/10u/10v/2d/z/lsm/sst/ci/sd/stl1/stl2/stl3/stl4/swvl1/swvl2/swvl3/swvl4',
    'levtype' : 'sfc',
    'date'    : f'{DATE1}/to/{DATE2}',
    'time'    : TIMES,
    'area'    : f'{NORTH}/{WEST}/{SOUTH}/{EAST}',
    'grid'    : "0.25/0.25",
    'format'  : 'grib'
}, OUTFILE)

print(OUTFILE)
