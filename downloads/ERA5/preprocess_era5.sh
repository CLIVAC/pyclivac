#!/bin/bash
######################################################################
# Filename:    preprocess_era5_data.sh
# Author:      Tessa Montini, tmontini@ucsb.edu
# Description: Script to concatenate ERA5 data files
#
# - Conconcate multiple input files along the time dimension
# - Unpack/repack data files
# - Modify variable attributes and global file attributes
#
######################################################################

# Input parameters
datadir="/home/sbarc/students/montini/data/downloads/"
dataset="era5"
var="tp"
level="sfc"
tstep="1hr"
start_yr=1979
end_yr=2016
title="ERA5 Reanalysis"
institution="European Centre for Medium-Range Weather Forecasts"

outfile="${dataset}_${var}_${level}_${tstep}_${start_yr}-${end_yr}.nc"

# Loop to unpack individual files & make time the record dim
cd $datadir
for year in $(seq $start_yr $end_yr)
do
    infile="${dataset}_${var}_${level}_${tstep}_${year}.nc"
    ncpdq -O --unpack ${infile} tmp.nc
    ncks -O --mk_rec_dmn time tmp.nc upk.${year}.nc
done

# Concatentate files along the time dimension
ncrcat -h upk*.nc concat.nc
ncatted -hO -a history,global,d,, concat.nc
rm -f upk*.nc

# Modify coordinate attributes
ncatted -hO -a axis,longitude,o,c,"X" concat.nc
ncatted -hO -a axis,latitude,o,c,"Y" concat.nc
ncatted -hO -a axis,time,o,c,"T" concat.nc

# Modify global file attributes
ncatted -hO -a title,global,o,c,"${title}" concat.nc
ncatted -hO -a institution,global,o,c,"${institution}" concat.nc

# Repack data file
ncpdq concat.nc ${outfile}
echo $outfile

# Remove tmp files
rm -f tmp.nc
rm -f concat.nc
