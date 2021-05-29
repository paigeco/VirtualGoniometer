import numpy as np

def onehot(u):
    k = np.max(u)
    targets = np.array(u).reshape(-1)
    return np.eye(k)[targets-1]
