"""
Filename:    plotter.py
Author:      Deanna Nash, dlnash@ucsb.edu
Description: Functions for plotting
"""


import os
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4 as nc
import matplotlib.pyplot as plt
import colorsys
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.ticker as mticker
import matplotlib.animation as animation


def simple_line_plot(df, varname, title=None, x_label=None,  y_label=None, color='b'):

    '''A plug and chug quick line plot with one dependent variable, using matplotlib.
    
        Parameters
        ----------
        df: pandas dataframe
            What data frame name taking data from, name potentially defined in resample (ex: df_daily).  
        varname: str
            the variable you want to plot.
        
        title: string, optional
        
        x_label: string, optional
        
        y_label: string, optional
        
        color: string, optional
            Change line color, can also add line styles.
            Quick reminder of color options: b,g,r,c,m,y,k,w
        
        Returns
        -------
        Line plot of df and variable entered.        
        '''
    x=df.index
    y=df[varname]
    c=color
    
    plt.plot_date(x, y, c)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.xticks(rotation=45)
    plt.show()

    
def simple_xarray_contour_map(data, cmap, cflevs=None):
    data = data
    # Set map projection
    mapcrs = ccrs.PlateCarree()  # what we want data to plot as
    datacrs = ccrs.PlateCarree() # what projection data comes in

    # Set up figure and axes
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(1, 1, 1, projection=mapcrs)

    # Add data
    p = ax.contourf(data.longitude, data.latitude, data[0].values, transform=datacrs,
                cmap=cmap, levels=cflevs, extend='both')

    # Add plot elements
    ax.coastlines()
    ax.gridlines()
    t0 = pd.to_datetime(str(data.time.values[0])).strftime("%Y-%m-%d %H:%M")
    plt.title(data.attrs['long_name'] + ' (' + data.attrs['units'] + ') at ' + t0)

    # Add colorbar
    cbar = plt.colorbar(p, orientation='horizontal',
                        shrink=0.85, pad=0.05, 
                        label=data.attrs['units'], spacing='uniform')

    # Save to file
    plt.savefig('plotfile.png')

    # Show plot
    plt.show()
    
def simple_xarray_pcolormesh_map(data, cmap, vmin, vmax):
    data = data
    # Set map projection
    mapcrs = ccrs.PlateCarree()  # what we want data to plot as
    datacrs = ccrs.PlateCarree() # what projection data comes in

    # Set up figure and axes
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(1, 1, 1, projection=mapcrs)

    # Add data
    p = ax.pcolormesh(data.longitude, data.latitude, data[0].values, transform=datacrs,
                cmap=cmap, vmin=vmin, vmax=vmax)

    # Add plot elements
    ax.coastlines()
    ax.gridlines()
    t0 = pd.to_datetime(str(data.time.values[0])).strftime("%Y-%m-%d %H:%M")
    plt.title(data.attrs['long_name'] + ' (' + data.attrs['units'] + ') at ' + t0)

    # Add colorbar
    cbar = plt.colorbar(p, orientation='horizontal',
                        shrink=0.85, pad=0.05, 
                        label=data.attrs['units'])

    # Save to file
    plt.savefig('plotfile.png')

    # Show plot
    plt.show()
    
def simple_contour_plot (data, lons, lats, datacrs= ccrs.PlateCarree(), mapcrs= ccrs.PlateCarree(), title = None, data_units = '', sequential = False, diverging = False, colormap='', cbar_orientation = 'horizontal'):

    '''A plug and chug quick contour plot for spatial data.
    
        Parameters
        ----------
        data: string
        
        lons: float
        
        lats: float
        
        datacrs: string, optional
            What projection data comes in.
            Note: If data comes in lons & lats, means that it is PlateCarree().
            https://scitools.org.uk/cartopy/docs/latest/crs/projections.html#cartopy-projections
            
        mapcrs: string, optional
            What projection you want output to be in.
            
        title: string, optional
        
        data_units: string, optional
            Used to label the colorbar values.
        
        colormap: string, optional
            https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
            
        cbar_orientation: string, optional
            Color bar orientation, either horizonatal or vertical.
            
        Returns
        -------
        Contour plot of data within specified lat and lon.
    
        '''
#     clevs = _nice_intervals(data, 10)
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(1, 1, 1, projection=mapcrs)
    
    if sequential == True:
        colorbar = 'cool'
    else: 
        colobar = 'YlOrRd'
    if diverging == True:
        colorbar = 'RdBu'
    else: 
        colobar = 'YlOrRd'

    p = ax.contourf(lons, lats, data, transform=datacrs,
                cmap = colormap, extend='both'
#                     , levels=clevs
                   )
    
    ax.coastlines()
    ax.gridlines()
    plt.title(title)
    
    cbar = plt.colorbar(p, orientation=cbar_orientation,
                    shrink=0.85, pad=0.05, label=data_units)
    
    plt.show()



def _nice_intervals(data, nlevs):
    '''
    Purpose::
        Calculates nice intervals between each color level for colorbars
        and contour plots. The target minimum and maximum color levels are
        calculated by taking the minimum and maximum of the distribution
        after cutting off the tails to remove outliers.
    Input::
        data - an array of data to be plotted
        nlevs - an int giving the target number of intervals
    Output::
        clevs - A list of floats for the resultant colorbar levels
    '''
    # Find the min and max levels by cutting off the tails of the distribution
    # This mitigates the influence of outliers
    data = data.ravel()
    mn = mstats.scoreatpercentile(data, 5)
    mx = mstats.scoreatpercentile(data, 95)
    #if there min less than 0 and
    # or max more than 0 
    #put 0 in center of color bar
    if mn < 0 and mx > 0:
        level = max(abs(mn), abs(mx))
        mnlvl = -1 * level
        mxlvl = level
    #if min is larger than 0 then
    #have color bar between min and max
    else:
        mnlvl = mn
        mxlvl = mx
    locator = mpl.ticker.MaxNLocator(nlevs)
    clevs = locator.tick_values(mnlvl, mxlvl)

    # Make sure the bounds of clevs are reasonable since sometimes
    # MaxNLocator gives values outside the domain of the input data
    clevs = clevs[(clevs >= mnlvl) & (clevs <= mxlvl)]
    return clevs


def loadCPT(path):
    """A function that loads a .cpt file and converts it into a colormap for the colorbar.
    
    This code was adapted from the GEONETClass Tutorial written by Diego Souza, retrieved 18 July 2019. 
    https://geonetcast.wordpress.com/2017/06/02/geonetclass-manipulating-goes-16-data-with-python-part-v/
    
    Parameters
    ----------
    path : 
        Path to the .cpt file
        
    Returns
    -------
    cpt :
        A colormap that can be used for the cmap argument in matplotlib type plot.
    """
    
    try:
        f = open(path)
    except:
        print ("File ", path, "not found")
        return None
 
    lines = f.readlines()
 
    f.close()
 
    x = np.array([])
    r = np.array([])
    g = np.array([])
    b = np.array([])
 
    colorModel = 'RGB'
 
    for l in lines:
        ls = l.split()
        if l[0] == '#':
            if ls[-1] == 'HSV':
                colorModel = 'HSV'
                continue
            else:
                continue
        if ls[0] == 'B' or ls[0] == 'F' or ls[0] == 'N':
            pass
        else:
            x=np.append(x,float(ls[0]))
            r=np.append(r,float(ls[1]))
            g=np.append(g,float(ls[2]))
            b=np.append(b,float(ls[3]))
            xtemp = float(ls[4])
            rtemp = float(ls[5])
            gtemp = float(ls[6])
            btemp = float(ls[7])
 
        x=np.append(x,xtemp)
        r=np.append(r,rtemp)
        g=np.append(g,gtemp)
        b=np.append(b,btemp)
 
    if colorModel == 'HSV':
        for i in range(r.shape[0]):
            rr, gg, bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
        r[i] = rr ; g[i] = gg ; b[i] = bb
 
    if colorModel == 'RGB':
        r = r/255.0
        g = g/255.0
        b = b/255.0
 
    xNorm = (x - x[0])/(x[-1] - x[0])
 
    red   = []
    blue  = []
    green = []
 
    for i in range(len(x)):
        red.append([xNorm[i],r[i],r[i]])
        green.append([xNorm[i],g[i],g[i]])
        blue.append([xNorm[i],b[i],b[i]])
 
    colorDict = {'red': red, 'green': green, 'blue': blue}
    # Makes a linear interpolation
    cpt = LinearSegmentedColormap('cpt', colorDict)
    
    return cpt


def make_cmap(colors, position=None, bit=False):
    '''
    make_cmap takes a list of tuples which contain RGB values. The RGB
    values may either be in 8-bit [0 to 255] (in which bit must be set to
    True when called) or arithmetic [0 to 1] (default). make_cmap returns
    a cmap with equally spaced colors.
    Arrange your tuples so that the first color is the lowest value for the
    colorbar and the last is the highest.
    position contains values from 0 to 1 to dictate the location of each color.
    '''
    bit_rgb = np.linspace(0,1,256)
    if position == None:
        position = np.linspace(0,1,len(colors))
    else:
        if len(position) != len(colors):
            sys.exit("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            sys.exit("position must start with 0 and end with 1")
    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],
                         bit_rgb[colors[i][1]],
                         bit_rgb[colors[i][2]])
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = LinearSegmentedColormap('my_colormap',cdict,256)
    return cmap


def _drawmap(fig, lons, lats, VO, cmap, clevs, title):
    '''Draw contour map for create_animation.'''
    # Set global extent on map
    ext = [-180.0, 180.0, -90., 90.]
    
    # Set map and data projections
    datacrs = ccrs.PlateCarree()  ## the projection the data is in
    mapcrs = ccrs.PlateCarree() ## the projection you want your map displayed in
    
    # Add subplot, title, and set extent
    ax = fig.add_subplot(1,1,1, projection=mapcrs)
    ax.set_title(title, fontsize=14)
    ax.set_extent(ext, crs=mapcrs)
    
    # Add Border Features
    coast = ax.coastlines(linewidths=1.0)
    ax.add_feature(cfeature.BORDERS)
    
    # Add grid lines
    ndeg=20.
    gl = ax.gridlines(crs=datacrs, draw_labels=True,
                      linewidth=.5, color='black', alpha=0.5, linestyle='--')
    gl.xlocator = mticker.FixedLocator(np.arange(ext[0], ext[1]+ndeg, ndeg))
    gl.ylocator = mticker.FixedLocator(np.arange(ext[2], ext[3]+ndeg, ndeg))
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabels_top = False
    gl.ylabels_right = False
    
    # Add contour plot
    cs = ax.contourf(lons, lats, VO, transform=datacrs, cmap=cmap, levels=clevs, zorder=1)
    return cs
    
def _myanimate(i, fig, DS, var, lats, lons, cmap, clevs):
    '''Loop through time steps for create_animation.'''
    # Clear current axis to overplot next time step
    ax = fig.gca()
    ax.clear()
    # Loop through time steps in ds
    VO = DS[var].values[i]
    # Set title based on long name and current time step
    ts = pd.to_datetime(str(DS.time.values[i])).strftime("%Y-%m-%d %H:%M")
    long_name = DS[var].long_name
    title = '{0} at {1}'.format(long_name, ts)
    # Add next contour map
    new_contour = _drawmap(fig, lons, lats, VO, cmap, clevs, title) 
    return new_contour

def create_animation(DS, lats, lons, var, clevs, cmap):
    '''Create an mp4 animation using an xarray dataset with lat, lon, and time dimensions.
    
        Parameters
        ----------
        DS: xarray dataset object
              
        lats: int
            Array of latitudes from xarray dataset object
        lons: int
            Array of longitudes from xarray dataset object
        var: string
            Variable name to plot
        clevs: int
            Contour levels to plot
        cmap: string
            Colormap for plotting
            
        Returns
        -------
        filename, mp4 file of animation
        
        '''
    
    # Get information from ds
    long_name = DS[var].long_name
    units = DS[var].units
    t0 = pd.to_datetime(str(DS.time.values[0])).strftime("%Y-%m-%d %H:%M")
    title = '{0} at {1}'.format(long_name, t0)
    FFMpegWriter = animation.writers['ffmpeg']
    metadata = dict(title=title,
                    comment='')
    writer = FFMpegWriter(fps=20, metadata=metadata)
    
    # Create a new figure window
    fig = plt.figure(figsize=[12,4])
    # Draw first timestep
    first_contour = _drawmap(fig, lons, lats, DS[var].values[0], cmap, clevs, title)

    # Add a color bar
    cbar = fig.colorbar(first_contour, orientation='vertical', cmap=cmap, shrink=0.55)
    cbar.set_label(units, fontsize=12)
    
    # Loop through animation
    ani = animation.FuncAnimation(fig, _myanimate, frames=np.arange(len(DS[var])),
                                  fargs=(fig, DS, var, lats, lons, cmap, clevs), interval=50)
    filename = long_name + ".mp4"
    ani.save(filename)
    
    return filename


def draw_basemap(ax, extent=None, xticks=None, yticks=None, grid=False):
    """
    Draws a basemap on which to plot data. 
    
    Map features include continents and country borders.
    Option to set lat/lon tickmarks and draw gridlines.
    
    Parameters
    ----------
    ax : 
        plot Axes on which to draw the basemap
    
    extent : float
        Set map extent to [lonmin, lonmax, latmin, latmax] 
        Default: None (uses global extent)
        
    grid : bool
        Whether to draw grid lines. Default: False
        
    xticks : float
        array of xtick locations (longitude tick marks)
    
    yticks : float
        array of ytick locations (latitude tick marks)
        
    Returns
    -------
    ax :
        plot Axes with Basemap
    
    Notes
    -----
    - Grayscale colors can be set using 0 (black) to 1 (white)
    - Alpha sets transparency (0 is transparent, 1 is solid)
    
    Author
    ------
    Tessa Montini, tmontini@ucsb.edu
    
    """

    # Use map projection (CRS) of the given Axes
    mapcrs = ax.projection    
    
    ## Map Extent
    # If no extent is given, use global extent
    if extent is None:        
        ax.set_global()
    # If extent is given, set map extent to lat/lon bounding box
    else:
        ax.set_extent(extent, crs=mapcrs)
    
    # Add map features (continents and country borders)
    ax.add_feature(cfeature.LAND, facecolor='0.9')      
    ax.add_feature(cfeature.BORDERS, edgecolor='0.4', linewidth=0.8)
    ax.add_feature(cfeature.COASTLINE, edgecolor='0.4', linewidth=0.8)

    ## Tickmarks/Labels
    # Set xticks if requested
    if xticks is not None:
        ax.set_xticks(xticks, crs=mapcrs)      
        lon_formatter = LongitudeFormatter()
        ax.xaxis.set_major_formatter(lon_formatter)
    # Set yticks if requested
    if yticks is not None:
        ax.set_yticks(yticks, crs=mapcrs)
        lat_formatter = LatitudeFormatter()
        ax.yaxis.set_major_formatter(lat_formatter)
    # apply tick parameters    
    ax.tick_params(direction='out', 
                   labelsize=8.5, 
                   length=4, 
                   pad=2, 
                   color='black')
    
    ## Gridlines
    # Draw gridlines if requested
    if (grid == True):
        ax.grid(color='k', alpha=0.5, linewidth=0.5, linestyle='--')
    
    return ax