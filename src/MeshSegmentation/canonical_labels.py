import numpy as np

def canonical_labels(u):
    n = len(u)
    k = len(np.unique(u))
    _label_set = np.zeros((k, 1))
    label = 0
    
    for i in range(n):
        if u[i] > label:
            label += 1
            l = u[i]
            I = u == label
            J = u == l
            u[I] = l
            u[J] = label
    return u
