import numpy as np
from CustomMath.PowerMethod import power_method

#PCA SMALLEST EIG WITHOUT PMETH
############################################
def pca_smallest_eig(X,center=True):
    if center:
        m = np.mean(X,axis=0)
        cov = np.transpose(X-m)@(X-m)
    else:
        cov = np.transpose(X)@X
    w,v = np.linalg.eig(cov)
    i = np.argmin(w)
    return v[:,i]

#PCA SMALLEST EIG W? PMETH
#################################################
def pca_smallest_eig_powermethod(X,center=True):

    if center:
        m = np.mean(X,axis=0)
        cov = np.transpose(X-m)@(X-m)/X.shape[0]
    else:
        cov = np.transpose(X)@X/X.shape[0]
    lmax,v = power_method(cov)
    _w,v = np.linalg.eig(cov)
    _l,v = power_method(cov - (lmax+1)*np.eye(3))
    return v.flatten()