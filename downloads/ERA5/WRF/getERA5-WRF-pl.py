#!/usr/bin/env python

"""
Filename:    getERA5-WRF-pl.py
Author:      Tessa Montini, tmontini@ucsb.edu
Description: Download ERA5 pressure level data for initializing WRF

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
OUTFILE = f'{DATADIR}/ERA5_pl_{DATE1}_{DATE2}.grib'


# API Request 
c = cdsapi.Client()
c.retrieve('reanalysis-era5-pressure-levels',{
    'product_type'  : 'reanalysis',
    'pressure_level': ['1','2','3',
                       '5','7','10',
                       '20','30','50',
                       '70','100','125',
                       '150','175','200',
                       '225','250','300',
                       '350','400','450',
                       '500','550','600',
                       '650','700','750',
                       '775','800','825',
                       '850','875','900',
                       '925','950','975',
                       '1000'
    ],
    'variable': ['geopotential','relative_humidity','specific_humidity',
                 'temperature','u_component_of_wind','v_component_of_wind'
    ],
    'date'    : f'{DATE1}/{DATE2}',
    'time'    : TIMES,
    'area'    : f'{NORTH}/{WEST}/{SOUTH}/{EAST}',
    'grid'    : [0.25, 0.25],
    'format'  : 'grib'
}, OUTFILE)

print(OUTFILE)
