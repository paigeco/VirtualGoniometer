import numpy as np

def conjgrad(A,b,x,T,tol):
    r = b - A@x
    p = r
    rsold = np.sum(r * r,0)
    for i in range(T):
        Ap = A@p
        alpha = rsold / np.sum(p*Ap,0)
        x = x + alpha*p
        r = r - alpha*Ap
        rsnew = np.sum(r*r,0)
        if np.sqrt(np.sum(rsnew)) < tol:
            break
        p = r + (rsnew / rsold) * p
        rsold = rsnew
    return x,i
