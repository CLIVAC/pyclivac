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
from matplotlib.colors import LinearSegmentedColormap # Linear interpolation for color maps
import seaborn as sns
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def simple_line_plot(df_name, df_loc, title=None, x_label=None,  y_label=None, color='b'):

    '''A plug and chug quick line plot with one dependent variable, using matplotlib.
    
        Parameters
        ----------
        df_name: string
            What data frame name taking data from, name potentially defined in resample (ex: df_daily).  
        df_loc: int
            What array index of a data frame to graph.
        
        title: string, optional
        
        x_label: string, optional
        
        y_label: string, optional
        
        color: string, optional
            Change line color, can also add line styles.
            Quick reminder of color options: b,g,r,c,m,y,k,w
        
        Returns
        -------
        Line plot of df_name and df_loc entered.
        
        '''
    x=df_name.index
    y=df_name.iloc[:,df_loc]
    c=color
    
    plt.plot(x, y, c)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.xticks(rotation=90)
    plt.show()

    
def simple_xarray_contour_map(data, cmap):
    data = data
    # Set map projection
    mapcrs = ccrs.PlateCarree()  # what we want data to plot as
    datacrs = ccrs.PlateCarree() # what projection data comes in

    # Set up figure and axes
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(1, 1, 1, projection=mapcrs)

    # Add data
    p = ax.contourf(data.longitude, data.latitude, data[0].values, transform=datacrs,
                cmap=cmap, extend='both')

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