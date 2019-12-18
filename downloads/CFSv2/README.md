# CFSv2 grib to netCDF

### Overview
* Dataset Description ([CFS documentation](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/climate-forecast-system-version2-cfsv2))
    * CFSv2 is an operational analysis model representing the global interaction between Earth's oceans, land, and atmosphere.
    * Horizontal resolution: 0.5&deg;x0.5&deg;
    * Temporal resolution: 6-hourly
* Three options for downloading CFS data: **1) [FTP](ftp://nomads.ncdc.noaa.gov/modeldata/cfsv2_analysis_pgbh/)** **2) [THREDDs](https://www.ncei.noaa.gov/thredds/catalog/cfs_v2_for_ts/catalog.html) **3) [HTTP](https://nomads.ncdc.noaa.gov/modeldata/cfsv2_analysis_pgbh/)

### Scripts
| Name | Description |
|:---  |:---         |
| `cfsv2_g2nc_pressure.table` | script for converting grib files to netCDF | 


### Variables
Frequently used data variables are listed in the tables below.

#### Pressure level variables
CFSv2 variable | Name in data file
:---        | :---
`'geopotential'` | `hgtpres`
`'temperature'` | `temp`
`'specific_humidity'` | `spfh`
`'u_component_of_wind'` | `u`
`'v_component_of_wind'` | `v`
`'vorticity'` (absolute) | `absv`
`'vertical_velocity'` | `omega`

#### Single level variables
CFSv2 'variable' value | Name in data file
:---        | :---
`'mean_sea_level_pressure'` | `prmsl` 
`'precipitation_rate'` | `prate`
`'surface_evap'` | `evapsfc`

  
### Converting grib file to netCDF using wgrib2
The following information was derived using [this website](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/netcdf.html)

`cfsv2_g2nc_pressure.table` is a script to specify parameters for conversion from grib2 format to netCDF format specifically from CFSv2 6-hourly pressure level data. 

* Download CFSv2 data (see above)
* Install wgrib2 using instructions found [here](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/compile_questions.html)
* Run wgrib code with .table file to convert grib files to netCDF. 
`wgrib2 ../path/to/grib/file/20190304cdas1.t00z.pgrbh00.grib2 -nc_table ../path/to/table/cfsv2_g2nc_pressure.table -netcdf new_file.nc`
