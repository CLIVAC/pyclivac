#!/bin/bash
######################################################################
# Filename:    preprocessERA5_to_daily.sh
# Author:      Tessa Montini, tmontini@ucsb.edu
# Description: Script to compute daily means from 6-hourly data
#               and concatenate the daily data files
#
# - Convert 6hr to daily data
# - Conconcate multiple input files along the time dimension
# - Unpack/repack data files
# - Rename data variable according to DRS syntax
# - Modify variable atts and global atts
#
######################################################################

# Input parameters
datadir="/Users/tessamontini/Google_Drive/DATA/downloads/q850"
invar="q"
outvar="shum"
level="850"
tstep="6hr"
spatial="spac3"
start_yr=1979
end_yr=2016
title="ERA5 Reanalysis"
institution="European Centre for Medium-Range Weather Forecasts"
outfile="era5_${outvar}_${level}_day_${start_yr}-${end_yr}_${spatial}_pkd.nc"

# Loop to unpack individual files & make time the record dim
cd $datadir
for year in $(seq $start_yr $end_yr)
do
    infile="era5_${invar}_${level}_${tstep}_${year}.nc"
    # unpack file
    ncpdq -O --unpack ${infile} tmp1.nc
    # make time the record dimension
    ncks -O --mk_rec_dmn time tmp1.nc tmp2.nc
    # Calculate daily mean
    cdo daymean tmp2.nc upk${year}.nc
done
rm -f tmp*.nc

# Concatentate files along the time dimension
ncrcat -h upk*.nc concat.nc
ncatted -hO -a history,global,d,, concat.nc
rm -f upk*.nc

# Modify coordinate attributes
ncatted -hO -a axis,longitude,o,c,"X" concat.nc
ncatted -hO -a axis,latitude,o,c,"Y" concat.nc
ncatted -hO -a axis,time,o,c,"T" concat.nc

# Modify global attributes
ncatted -hO -a title,global,o,c,"${title}" concat.nc
ncatted -hO -a institution,global,o,c,"${institution}" concat.nc

# Rename data variable and modify its attributes
ncrename -O -v ${invar},${outvar} concat.nc 
ncatted -hO -a level,${outvar},o,c,"${level}" concat.nc

# Special variable modifications
if [[ "${outvar}" = "zg" ]]; then
    cdo divc,9.80665 concat.nc tmp2.nc
    ncatted -hO -a standard_name,${outvar},o,c,"geopotential_height" tmp2.nc
    ncatted -hO -a long_name,${outvar},o,c,"Geopotential height" tmp2.nc
    ncatted -hO -a units,${outvar},o,c,"m" tmp2.nc
    mv tmp2.nc concat.nc
fi

# Repack data file
ncpdq concat.nc ${outfile}
#mv concat.nc ${outfile}    #don't repack
echo $outfile

# Remove tmp files
rm -f tmp*.nc
rm -f concat.nc
