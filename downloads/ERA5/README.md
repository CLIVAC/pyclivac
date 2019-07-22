# ERA5

### Overview
* Dataset Description ([ERA5 documentation](https://confluence.ecmwf.int/display/CKB/ERA5+data+documentation))
    * ERA5 is the 5th generation ECMWF atmospheric reanalysis
    * Horizontal resolution: 0.25&deg;x0.25&deg;
    * Temporal resolution: hourly
* Two options for downloading ERA5 data: **1) [CDS web interface](https://cds.climate.copernicus.eu/#!/search?text=ERA5&type=dataset)** or **2) CDS API client** (python package)
    * [How to use the CDS API](https://cds.climate.copernicus.eu/api-how-to)
    * [How to download ERA5](https://confluence.ecmwf.int/display/CKB/How+to+download+ERA5)

### Scripts
| Name | Description |
|:---  |:---         |
| `download_era5_prs_level.py` | script for downloading ERA5 data on pressure levels
| `download_era5_single_level.py` | scring for downloading ERA5 data on single levels |
| `preprocess_era5.py` | script for preprocessing and concatenating ERA5 data files (uses NCO and CDO command line tools) |


### Variables
Frequently used data variables are listed in the tables below. See [here](https://confluence.ecmwf.int/display/CKB/ERA5+data+documentation#ERA5datadocumentation-Parameterlistings) for the full list of ERA5 parameters.

#### Pressure level variables
CDS request variable | Name in data file
:---        | :---
`'geopotential'` | `z`
`'temperature'` | `t`
`'specific_humidity'` | `q`
`'u_component_of_wind'` | `u`
`'v_component_of_wind'` | `v`
`'vorticity'` (relative) | `vo`
`'vertical_velocity'` | `w`

#### Single level variables
CDS request 'variable' value | Name in data file
:---        | :---
`'surface_pressure'` | `sp`
`'mean_sea_level_pressure'` | `msl` 
`'total_precipitation'` | `tp`
`'vertical_integral_of_eastward_water_vapour_flux'` | `p71.162`
`'vertical_integral_of_northward_water_vapour_flux'` | `p72.162`

#### Variable modifications
* Convert **geopotential** to **geopotential height**:  
  `zg = z / 9.80655`
* **Total precipitation** is the accumulation (in meters) from the end of one forecast hour to the start of the next. Therefore, precip must be downloaded at a 1-hour temporal resolution in order to convert the hourly accumulation to some other rain rate (e.g. mm/day).

  
### Keywords to refine your data request
* **`area`** : geographical area subset
* **`grid`** : change the grid resolution
* For example, to request a geographical subset of data over South America at 0.5x0.5 degrees resolution, add the following lines to your data request:
```
   'area' : [15, -85, -50, -30]   # North, West, South, East. Default: global 
   'grid' : [0.5, 0.5]            # Default: 0.25 x 0.25
```
