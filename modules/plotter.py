## used for plotting functions

def draw_contour_map(dataset, lats, lons, fname, fmt='png', gridshape=(1, 1),
                     clabel='', ptitle='', subtitles=None, cmap=None,
                     clevs=None, nlevs=10, parallels=None, meridians=None,
                     extend='neither', aspect=8.5/2.5):
    ''' Draw a multiple panel contour map plot.
    :param dataset: 3D array of data to be plotted with shape (nT, nLat, nLon).
    :type dataset: :class:`numpy.ndarray`
    :param lats: Array of latitudes values.
    :type lats: :class:`numpy.ndarray`
    :param lons: Array of longitudes
    :type lons: :class:`numpy.ndarray`
    :param fname: The filename of the plot.
    :type fname: :mod:`string`
    :param fmt: (Optional) filetype for the output.
    :type fmt: :mod:`string`
    :param gridshape: (Optional) tuple denoting the desired grid shape
        (num_rows, num_cols) for arranging the subplots.
    :type gridshape: :func:`tuple` of the form (num_rows, num_cols)
    :param clabel: (Optional) colorbar title.
    :type clabel: :mod:`string`
    :param ptitle: (Optional) plot title.
    :type ptitle: :mod:`string`
    :param subtitles: (Optional) list of titles for each subplot.
    :type subtitles: :class:`list` of :mod:`string`
    :param cmap: (Optional) string or :class:`matplotlib.colors.LinearSegmentedColormap`
        instance denoting the colormap. This must be able to be recognized by
        `Matplotlib's get_cmap function <http://matplotlib.org/api/cm_api.html#matplotlib.cm.get_cmap>`_.
    :type cmap: :mod:`string` or :class:`matplotlib.colors.LinearSegmentedColormap`
    :param clevs: (Optional) contour levels values.
    :type clevs: :class:`list` of :class:`int` or :class:`float`
    
    :param nlevs: (Optional) target number of contour levels if clevs is None.
    :type nlevs: :class:`int`
    :param parallels: (Optional) list of ints or floats for the parallels to
        be drawn. See the `Basemap documentation <http://matplotlib.org/basemap/users/graticule.html>`_
        for additional information.
    :type parallels: :class:`list` of :class:`int` or :class:`float`
    :param meridians: (Optional) list of ints or floats for the meridians to
        be drawn. See the `Basemap documentation <http://matplotlib.org/basemap/users/graticule.html>`_
        for additional information.
    :type meridians: :class:`list` of :class:`int` or :class:`float`
    :param extend: (Optional) flag to toggle whether to place arrows at the colorbar
         boundaries. Default is 'neither', but can also be 'min', 'max', or
         'both'. Will be automatically set to 'both' if clevs is None.
    :type extend: :mod:`string`
    '''
    # Handle the single plot case. Meridians and Parallels are not labeled for
    # multiple plots to save space.
    if dataset.ndim == 2 or (dataset.ndim == 3 and dataset.shape[0] == 1):
        if dataset.ndim == 2:
            dataset = dataset.reshape(1, *dataset.shape)
        mlabels = [0, 0, 0, 1]
        plabels = [1, 0, 0, 1]
    else:
        mlabels = [0, 0, 0, 0]
        plabels = [0, 0, 0, 0]

    # Make sure gridshape is compatible with input data
    nplots = dataset.shape[0]
    gridshape = _best_grid_shape(nplots, gridshape)

    # Set up the figure
    fig = plt.figure()
    fig.set_size_inches((8.5, 11.))
    fig.dpi = 300

    # Make the subplot grid
    grid = ImageGrid(fig, 111,
                     nrows_ncols=gridshape,
                     axes_pad=0.3,
                     share_all=True,
                     add_all=True,
                     ngrids=nplots,
                     label_mode='L',
                     cbar_mode='single',
                     cbar_location='bottom',
                     cbar_size=.15,
                     cbar_pad='0%'
                     )

    # Determine the map boundaries and construct a Basemap object
    lonmin = lons.min()
    lonmax = lons.max()
    latmin = lats.min()
    latmax = lats.max()
    m = Basemap(projection = 'cyl', llcrnrlat = latmin, urcrnrlat = latmax,
                llcrnrlon = lonmin, urcrnrlon = lonmax, resolution = 'l')

    # Convert lats and lons to projection coordinates
    if lats.ndim == 1 and lons.ndim == 1:
        lons, lats = np.meshgrid(lons, lats)

    # Calculate contour levels if not given
    if clevs is None:
        # Cut off the tails of the distribution
        # for more representative contour levels
        clevs = _nice_intervals(dataset, nlevs)
        extend = 'both'

    cmap = plt.get_cmap(cmap)

    # Create default meridians and parallels. The interval between
    # them should be 1, 5, 10, 20, 30, or 40 depending on the size
    # of the domain
    length = max((latmax - latmin), (lonmax - lonmin)) / 5
    if length <= 1:
        dlatlon = 1
    elif length <= 5:
        dlatlon = 5
    else:
        dlatlon = np.round(length, decimals = -1)
    if meridians is None:
        meridians = np.r_[np.arange(0, -180, -dlatlon)[::-1], np.arange(0, 180, dlatlon)]
    if parallels is None:
        parallels = np.r_[np.arange(0, -90, -dlatlon)[::-1], np.arange(0, 90, dlatlon)]

    x, y = m(lons, lats)
    for i, ax in enumerate(grid):
        # Load the data to be plotted
        data = dataset[i]
        m.ax = ax

        # Draw the borders for coastlines and countries
        m.drawcoastlines(linewidth=1)
        m.drawcountries(linewidth=.75)

        # Draw parallels / meridians
        m.drawmeridians(meridians, labels=mlabels, linewidth=.75, fontsize=10)
        m.drawparallels(parallels, labels=plabels, linewidth=.75, fontsize=10)

        # Draw filled contours
        cs = m.contourf(x, y, data, cmap=cmap, levels=clevs, extend=extend)

        # Add title
        if subtitles is not None:
            ax.set_title(subtitles[i], fontsize='small')

    # Add colorbar
    cbar = fig.colorbar(cs, cax=ax.cax, drawedges=True, orientation='horizontal', extendfrac='auto')
    cbar.set_label(clabel)
    cbar.set_ticks(clevs)
    cbar.ax.tick_params(labelsize=6)
    cbar.ax.xaxis.set_ticks_position('none')
    cbar.ax.yaxis.set_ticks_position('none')

    # This is an ugly hack to make the title show up at the correct height.
    # Basically save the figure once to achieve tight layout and calculate
    # the adjusted heights of the axes, then draw the title slightly above
    # that height and save the figure again
    fig.savefig(TemporaryFile(), bbox_inches='tight', dpi=fig.dpi)
    ymax = 0
    for ax in grid:
        bbox = ax.get_position()
        ymax = max(ymax, bbox.ymax)

    # Add figure title
    fig.suptitle(ptitle, y=ymax + .06, fontsize=16)
    fig.savefig('%s.%s' %(fname, fmt), bbox_inches='tight', dpi=fig.dpi)
    fig.clf()

def draw_portrait_diagram(results, rowlabels, collabels, fname, fmt='png',
                          gridshape=(1, 1), xlabel='', ylabel='', clabel='',
                          ptitle='', subtitles=None, cmap=None, clevs=None,
                          nlevs=10, extend='neither', aspect=None):
    ''' Draw a portrait diagram plot.
    :param results: 3D array of the fields to be plotted. The second dimension
              should correspond to the number of rows in the diagram and the
              third should correspond to the number of columns.
    :type results: :class:`numpy.ndarray`
    :param rowlabels: Labels for each row.
    :type rowlabels: :class:`list` of :mod:`string`
    :param collabels: Labels for each row.
    :type collabels: :class:`list` of :mod:`string`
    :param fname: Filename of the plot.
    :type fname: :mod:`string`
    
    :param fmt: (Optional) filetype for the output.
    :type fmt: :mod:`string`
    :param gridshape: (Optional) tuple denoting the desired grid shape
        (num_rows, num_cols) for arranging the subplots.
    :type gridshape: :func:`tuple` of the form (num_rows, num_cols)
    :param xlabel: (Optional) x-axis title.
    :type xlabel: :mod:`string`
    :param ylabel: (Optional) y-ayis title.
    :type ylabel: :mod:`string`
    :param clabel: (Optional) colorbar title.
    :type clabel: :mod:`string`
    :param ptitle: (Optional) plot title.
    :type ptitle: :mod:`string`
    :param subtitles: (Optional) list of titles for each subplot.
    :type subtitles: :class:`list` of :mod:`string`
    :param cmap: (Optional) string or :class:`matplotlib.colors.LinearSegmentedColormap`
        instance denoting the colormap. This must be able to be recognized by
        `Matplotlib's get_cmap function <http://matplotlib.org/api/cm_api.html#matplotlib.cm.get_cmap>`_.
    :type cmap: :mod:`string` or :class:`matplotlib.colors.LinearSegmentedColormap`
    :param clevs: (Optional) contour levels values.
    :type clevs: :class:`list` of :class:`int` or :class:`float`
    :param nlevs: Optional target number of contour levels if clevs is None.
    :type nlevs: :class:`int`
    :param extend: (Optional) flag to toggle whether to place arrows at the colorbar
         boundaries. Default is 'neither', but can also be 'min', 'max', or
         'both'. Will be automatically set to 'both' if clevs is None.
    :type extend: :mod:`string`
    :param aspect: (Optional) approximate aspect ratio of each subplot
        (width / height). Default is 8.5 / 5.5
    :type aspect: :class:`float`
    '''
    # Handle the single plot case.
    if results.ndim == 2:
        results = results.reshape(1, *results.shape)

    nplots = results.shape[0]

    # Make sure gridshape is compatible with input data
    gridshape = _best_grid_shape(nplots, gridshape)

    # Row and Column labels must be consistent with the shape of
    # the input data too
    prows, pcols = results.shape[1:]
    if len(rowlabels) != prows or len(collabels) != pcols:
        raise ValueError('rowlabels and collabels must have %d and %d elements respectively' %(prows, pcols))

    # Set up the figure
    width, height = _fig_size(gridshape)
    fig = plt.figure()
    fig.set_size_inches((width, height))
    fig.dpi = 300

    # Make the subplot grid
    grid = ImageGrid(fig, 111,
                     nrows_ncols=gridshape,
                     axes_pad=0.4,
                     share_all=True,
                     aspect=False,
                     add_all=True,
                     ngrids=nplots,
                     label_mode='all',
                     cbar_mode='single',
                     cbar_location='bottom',
                     cbar_size=.15,
                     cbar_pad='3%'
                     )

    # Calculate colorbar levels if not given
    if clevs is None:
        # Cut off the tails of the distribution
        # for more representative colorbar levels
        clevs = _nice_intervals(results, nlevs)
        extend = 'both'

    cmap = plt.get_cmap(cmap)
    norm = mpl.colors.BoundaryNorm(clevs, cmap.N)

    # Do the plotting
    for i, ax in enumerate(grid):
        data = results[i]
        cs = ax.matshow(data, cmap=cmap, aspect='auto', origin='lower', norm=norm)

        # Add grid lines
        ax.xaxis.set_ticks(np.arange(data.shape[1] + 1))
        ax.yaxis.set_ticks(np.arange(data.shape[0] + 1))
        x = (ax.xaxis.get_majorticklocs() - .5)
        y = (ax.yaxis.get_majorticklocs() - .5)
        ax.vlines(x, y.min(), y.max())
        ax.hlines(y, x.min(), x.max())

        # Configure ticks
        ax.xaxis.tick_bottom()
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        ax.set_xticklabels(collabels, fontsize='xx-small')
        ax.set_yticklabels(rowlabels, fontsize='xx-small')

        # Add axes title
        if subtitles is not None:
            ax.text(0.5, 1.04, subtitles[i], va='center', ha='center',
                    transform = ax.transAxes, fontsize='small')

    # Create a master axes rectangle for figure wide labels
    fax = fig.add_subplot(111, frameon=False)
    fax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
    fax.set_ylabel(ylabel)
    fax.set_title(ptitle, fontsize=16)
    fax.title.set_y(1.04)

    # Add colorbar
    cax = ax.cax
    cbar = fig.colorbar(cs, cax=cax, norm=norm, boundaries=clevs, drawedges=True,
                        extend=extend, orientation='horizontal', extendfrac='auto')
    cbar.set_label(clabel)
    cbar.set_ticks(clevs)
    cbar.ax.tick_params(labelsize=6)
    cbar.ax.xaxis.set_ticks_position('none')
    cbar.ax.yaxis.set_ticks_position('none')

    # Note that due to weird behavior by axes_grid, it is more convenient to
    # place the x-axis label relative to the colorbar axes instead of the
    # master axes rectangle.
    cax.set_title(xlabel, fontsize=12)
    cax.title.set_y(1.5)

    # Save the figure
    fig.savefig('%s.%s' %(fname, fmt), bbox_inches='tight', dpi=fig.dpi)
    fig.clf()