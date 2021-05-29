import numpy as np
import sklearn.cluster as cluster

from .GraphSetup import graph_setup
from .spec_proj import spec_proj
from .onehot import onehot
from .canonical_labels import canonical_labels



def segment_mesh(context):
    from ..MaterialManagers.ManagerInstance import Material_Group_Manager


    polygons = context.active_object.data.polygons
    vertices = context.active_object.data.vertices
    
    # Add triangulation stage
    
    P = np.empty(len(vertices)*3, dtype=float)
    Faces = np.empty(len(polygons)*3, dtype=int)

    vertices.foreach_get('co', P)    
    polygons.foreach_get('vertices', Faces)

    P = np.reshape(P, (-1, 3))
    Faces = np.reshape(Faces, (-1, 3))

    print(P.shape)
    print(Faces.shape)

    #P = np.loadtxt('HalfAnnulusPoints')
    #import Faces = (np.loadtxt('HalfAnnulusConnectivityList') - 1).astype(int)
    k = 6 # Number of faces
    n = 10000 # Number of Points that are sampled
    r = 10 # Max radius of the search
    p = 0.5 # Weight matrix

    W, J, _ss_idx, _node_idx = graph_setup(P[:, 0], P[:, 1], P[:, 2], Faces, n, r, p)

    V, _D, _V1 = spec_proj(W, 10, 3)
    
    kmeans = cluster.KMeans(n_clusters=k).fit(V[:, 0:k-1])
    
    u = kmeans.labels_
    U = J*onehot(u)
    L = np.argmax(U, 1)
    L = canonical_labels(L)
    
    regions = [Material_Group_Manager.add_region_to_active() for i in range(k)]

    print(regions)
    
    
    colors = [region.bsp.local_material_index for region in regions]
    
    sequence = [int(colors[L[face[0]]]) for face in Faces]
    
    print(sequence)
    
    polygons.foreach_set('material_index', sequence)
