""" Returns the Angle from two Regions's Centroids
and Normals """
import numpy as np

from .PCASmallestEig import pca_smallest_eig, pca_smallest_eig_powermethod

def get_angle(P1, P2, N1, N2, UsePCA=True, UsePower=False):
    """[summary]

    Args:
        P1 ([type]): [description]
        P2 ([type]): [description]
        N1 ([type]): [description]
        N2 ([type]): [description]
        UsePCA (bool, optional): [description]. Defaults to True.
        UsePower (bool, optional): [description]. Defaults to False.

    Returns:
        [float]: [angle between the two Regions]
    """
    if UsePCA:
        if UsePower:
            n1 = pca_smallest_eig_powermethod(P1)
            n2 = pca_smallest_eig_powermethod(P2)
        else:
            n1 = pca_smallest_eig(P1)
            n2 = pca_smallest_eig(P2)

        s1 = np.mean(N1,axis=0)
        if np.dot(n1,s1) < 0:
            n1 = -n1

        s2 = np.mean(N2,axis=0)
        if np.dot(n2,s2) < 0:
            n2 = -n2
    else: #Use average of surface normals

        n1 = np.average(N1,axis=0)
        n1 = n1/np.linalg.norm(n1)
        n2 = np.average(N2,axis=0)
        n2 = n2/np.linalg.norm(n2)
    
    #Angle between
    return float(180.0-np.arccos(np.dot(n1,n2))*180.0/np.pi), n1, n2
