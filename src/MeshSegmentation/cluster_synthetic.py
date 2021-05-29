#import numpy.random as rand
#import scipy.io as io
#import scipy.sparse as sp
#from scipy.sparse.linalg import eigs, eigsh
#import scipy.sparse.linalg as splinalg
#import scipy.spatial as spatial
#from sklearn.neighbors import NearestNeighbors

import numpy as np
import sklearn.cluster as cluster


from .GraphSetup import graph_setup
from .spec_proj import spec_proj
from .onehot import onehot
from .canonical_labels import canonical_labels
from .cplotsurf import cplotsurf

P = np.loadtxt('HalfAnnulusPoints.txt')
Faces = (np.loadtxt('HalfAnnulusConnectivityList.txt') - 1).astype(int)

print(P)
print(Faces)

k = 6 # Number of faces
n = 5000 # Number of Points that are sampled
r = 0.5 # Max radius of the search
p = 2 # Weight matrix

W,J,ss_idx,node_idx = graph_setup(P[:, 0], P[:, 1], P[:, 2], Faces, n, r, p)

V,D,V1 = spec_proj(W,10,3)
kmeans = cluster.KMeans(n_clusters=k).fit(V[:,0:k-1])
u = kmeans.labels_
U = J*onehot(u)
L = np.argmax(U,1)
L = canonical_labels(L)

k_found = len(np.unique(L)+1)

print(k_found)

val = []
print([L[face[0]] for face in Faces])


cplotsurf(P[:, 0], P[:, 1], P[:, 2], Faces, L)
