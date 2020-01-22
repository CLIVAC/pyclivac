"""
Filename:    eofs.py
Author:      Tessa Montini, tmontini@ucsb.edu
Description: Functions used to calculate and anaylze EOFs
"""

## Imports

import os, sys
import numpy as np


## FUNCTIONS

def spatial_weights(latitude):
    """Spatial weights
    
    Returns a 1D array of weights equal to the sqrt of the cos of latitude.
    
    Parameters
    ----------
    latitude : 1D array, float
        latitudes in degrees
  
    Returns
    -------
    weights : 1D array, float
        weights equal to the sqrt of the cosine of latitude
    
    Example
    -------
    # Apply spatial weights using xarray
    wgts = spatial_weights(lats)            # compute weights
    era['wgts'] = ('latitude', wgts)        # add `wgts` to dataset
    era['uwnd_wgt'] = era.uwnd * era.wgts   # apply wgts to data variable
    
    """
    # convert lats from degrees to radians
    lat_rad = np.deg2rad(latitude)
    # compute weights
    weights = np.sqrt(np.cos(lat_rad))
    
    return weights


def calc_eofs(z):
    """Eigenvector decomposition of covariance/correlation matrix
    
    Parameters
    ----------
    z : array_like, float
        matrix of data values [nxp];
        n = number of observations (rows);
        p = number of variables (columns)
        
    Returns
    -------
    evals : array_like, float
        vector of eigenvalues of size [p]
    evecs : array_like, float
        pxp matrix of eigenvectors (columns)
    
    """
    # Compute covariance/correlation matix [R]
    ntot = z.shape[0]
    R = np.matmul(z.T,z) / (ntot - 1.)

    # Eigenvector decomposition of R
    evals, evecs = np.linalg.eig(R)

    return evals, evecs


def calc_pcs(z, evecs, npcs):
    """Calculate principal components from eigenvalues and eigenvectors
    
    Parameters
    ----------
    z : array_like, float
        standardized data matrix
    evecs : array_like, float
        pxk matrix of eigenvectors (columns), where k<=p (may be truncated)
    npcs : scalar, int
        number of pcs to return
        
    Returns
    -------
    pcs : array_like, float
        .........
    
    """   
    tmp = np.matmul(z, evecs[:,0:npcs])
    pcs = tmp.T
    
    return pcs


def loadings(evals, evecs, neofs):
    """Calculate loadings matrix
    
    Parameters
    ----------
    evals : array_like, float
        Vector of eignvalues
    evecs : array_like, float
        Matrix of eigenvectors
    neofs : scalar, int
        number of eofs to calculate loadings for
             
    Returns
    -------
    loadings : array_like, float
        Loadings matrix
    
    """
    evals_tr = evals[0:neofs]
    evecs_tr = evecs[:, 0:neofs]
    loadings = evecs_tr * np.sqrt(evals_tr)

    return loadings


def calc_eofs_svd(z, neofs):
    """Singular value decomposition of data matrix
    
    Parameters
    ----------
    z : array_like, float
        2d array of standardized data values of size [n x p];
        n = number of observations (rows);
        p = number of variables (columns)
    
    neofs : scalar, int
        number of eofs to return (used in loadings and pcs calculation)
        
    Returns
    -------
    evals : array_like, float
        vector of eigenvalues of size [p]
    evecs : array_like, float
        array of eigenvectors (columns); size [p x p]
    loadings : array_like, float
        loadings matrix
    pcs : array_like, float
        principal components
    
    """    
    # Singular Value Decomposition of z
    U, S, Vt = np.linalg.svd(z)
    ntot = z.shape[0]

    # Compute eigenvalues
    evals = S**2.0 / (ntot-1)
    
    # Compute eigenvectors
    evecs = Vt.T
    
    # Compute loadings *** add neof
    loadings = evecs * S / np.sqrt(ntot-1.0)
    
    # Compute principal components
    tmp = U[:,0:neofs] * S[0:neofs]
    pcs = tmp.T

    return evals, evecs, loadings, pcs


def exp_variance(evals, neofs=None):
    """Explained variance of EOFs
    
    Calculates the percent of the total variance explained by each EOF.
    
    Parameters
    ----------
    evals : array_like, float
        Array of eigenvalues
    neofs : scalar, int
        Number of eigenvectors to return the percent variance for.
        Defaults to all eigenvalues.
    
    Returns
    -------
    pct_var : array_like, float
        Percent variances for each EOF
        
    """    
    slicer = slice(0, neofs)
    pct_var = evals[slicer] / np.sum(evals) * 100.
    
    return pct_var


def north_test(evals, n):
    """North Test for separation of eigenvalues
    
    Parameters
    ----------
    evals : array_like, float
        Array of eigenvalues
    n : scalar, float
        number of independent samples
        
    Returns
    -------
    error : array_like, float
        Array of errors scaled by the variance fraction (%)
    
    """   
    tmp = evals * np.sqrt(2.0/n)
    error = tmp / np.sum(evals) * 100
    
    return error


# def get_pcs_std(z, npcs, npts):
#     """Calculate standardized PC scores using SVD
    
#     **** need to verify equations... 
#     different from pc calculatin in calc_eofs_svd **** 
    
#     """
#     U, S, Vt = np.linalg.svd(z)
#     tmp = np.sqrt(npts-1) * U[:,0:npcs]
#     pcs_std = tmp.T
    
#     return pcs_std
