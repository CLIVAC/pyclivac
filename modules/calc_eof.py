"""
Collection of functions used to calculate and anaylze EOFs

"""

# Imports

import os, sys
import numpy as np


# Define functions

def get_eofs(z):
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


def get_pcs(Z, evecs, neofs):
    """Calculate principal components from eigenvalues and eigenvectors
    
    Parameters
    ----------
    Z : array_like, float
        standardized data matrix
    evecs : array_like, float
        pxk matrix of eigenvectors (columns), where k<=p (may be truncated)
    neofs : scalar, int
        number of pcs to return
        
    Returns
    -------
    pcs : array_like, float
        vector of eigenvalues of size ...
    
    """
    
    tmp = np.matmul(Z, evecs[:,0:neofs])
    pcs = tmp.T
    
    return pcs


def get_loadings(evals, evecs, neofs):
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


def eofs_svd(z, neofs):
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



def north_test(evals, ns):
    """North Test for separation of eigenvalues
    
    Parameters
    ----------
    evals : array_like, float
        Array of eigenvalues
    ns : scalar, float
        number of independent samples
        
    Returns
    -------
    error : array_like, float
        Array of errors scaled by the variance fraction
    
    """
    
    tmp = evals * np.sqrt(2.0/ns)
    error = tmp / np.sum(evals) * 100
    
    return error
