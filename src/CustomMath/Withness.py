import numpy as np

#Withness is a measure of how well 1D data clusters into two groups
############################################
def withness(x):
    x = np.sort(x)
    sigma = np.std(x)
    n = x.shape[0]
    v = np.zeros(n-1,)
    for i in range(n-1):
        x1 = x[:(i+1)]
        x2 = x[(i+1):]
        m1 = np.mean(x1)
        m2 = np.mean(x2)
        v[i] = (np.sum((x1-m1)**2) + np.sum((x2-m2)**2))/(sigma**2*n)
    ind = np.argmin(v)
    m = x[ind]
    w = v[ind]
    return w,m