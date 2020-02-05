# ERA5

### Overview
* Dataset Description ([ERA5 documentation](https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation))
    * ERA5 is the 5th generation ECMWF atmospheric reanalysis
    * Horizontal resolution: 0.25&deg;x0.25&deg;
    * Temporal resolution: hourly
* [How to download ERA5](https://confluence.ecmwf.int/display/CKB/How+to+download+ERA5) data via the Climate Data Store (CDS) 
   * Downloading ERA5 through the [CDS web interface](https://cds.climate.copernicus.eu/#!/search?text=ERA5&type=dataset)
   * Downloading ERA5 through the [CDS API](https://cds.climate.copernicus.eu/api-how-to) (python package)

### Scripts
| Name | Description |
|:---  |:---         |
| `getERA5_prs.py` | script for retrieving ERA5 data on pressure levels |
| `getERA5_sfc.py` | script for retrieving ERA5 data on single levels |
| `getERA5_prs_batch.py` | scripts for retrieving large data requests (breaks request into smaller increments and saves to multiple outfiles) |
| `getERA5_sfc_batch.py` |   |
| `preprocessERA5_concat.py` | script for preprocessing and concatenating ERA5 data files (uses NCO and CDO command line tools) |


### Variables
Frequently used data variables are listed in the tables below. See [here](https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation#ERA5:datadocumentation-Parameterlistings) for the full list of ERA5 parameters.

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
