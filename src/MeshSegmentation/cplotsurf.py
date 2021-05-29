import numpy as np
#import vtk
#import colorsys
#import h5py
#import mayavi
#from mayavi import mlab

def cplotsurf(x, _y, _z, _triangles, C=-1):
    if C.any == -1: #if no C given
        C = np.ones((len(x), 1))
        
    n = len(np.unique(C))
    C = C.astype(int)
    if n > 20:
        pass
        #mesh = mlab.triangular_mesh(x,y,z,triangles,scalars=C)
    else:
        col = (np.arange(1, n+1)) / n
        _colors = col[C-1]
        #mesh = mlab.triangular_mesh(x,y,z,triangles,scalars=colors)
        
    #return mesh
