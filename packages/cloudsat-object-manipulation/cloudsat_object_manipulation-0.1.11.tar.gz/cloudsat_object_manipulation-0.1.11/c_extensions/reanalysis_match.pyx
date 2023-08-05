cimport numpy as cnp
import numpy as np

cdef extern from "env_match.cpp" nogil:
    void match_env(float lat_bnds[][2], float lon_bnds[][2], float lat_bins[],float lon_bins[], int num_clds,int num_lat_bins, int num_lon_bins)

def reanalysis_match_var(cnp.ndarray[float,ndim = 2] lat_bnds,cnp.ndarray[float,ndim = 2] lon_bnds, cnp.ndarray[float,ndim = 1] lat_bins, cnp.ndarray[float,ndim = 1] lon_bins):
    '''
    Purpose:

    Input:

    Output:
    '''

    cdef cnp.ndarray[long,ndim = 1] i_indc,j_indc

    lon_bnds = lon_bnds % 360.

    i_indc   = lat_bins.argsort()
    j_indc   = lon_bins.argsort()
    if(lat_bins[0] < lat_bins[-1]): print(i_indc)
    if(lon_bins[0] < lon_bins[-1]): j_indc = j_indc[::-1]

    lat_bins = lat_bins[i_indc]
    lon_bins = lon_bins[j_indc]

    match_env(<float (*)[2]> lat_bnds.data, <float (*)[2]> lon_bnds.data, <float (*)> lat_bins.data, <float (*)> lon_bins.data, lon_bnds.shape[0], lat_bins.size, lon_bins.size)
