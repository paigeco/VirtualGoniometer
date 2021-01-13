import numpy as np
from .PCASmallestEig import pca_smallest_eig, pca_smallest_eig_powermethod
from .Withness import withness
from .CalculateAngle import get_angle

#RP1D clustering from
#Han, Sangchun, and Mireille Boutin. "The hidden structure of image datasets." 2015 IEEE International Conference on Image Processing (ICIP). IEEE, 2015.
############################################
def ClusteringMeanRP1D(P,N,T,A=0,UsePCA=True,UsePower=False):
    n = N.shape[0]
    d = N.shape[1]
    v = np.random.rand(T,d)
    
    #u = np.mean(N,axis=0)
    
    if UsePower:
        N1 = pca_smallest_eig_powermethod(N, center=False)
        N1 = np.reshape(N1,(3,))
    else:
        N1 = pca_smallest_eig(N, center=False)
    
    N2 = np.sum(N,axis=0)
    v = np.cross(N1,N2)
    v = v/np.linalg.norm(v)
    
    m = np.mean(P,axis=0)
    dist = np.sqrt(np.sum((P - m)**2,axis=1))
    i = np.argmin(dist)
    radius = np.max(dist)
    D = (P - P[i,:])/radius

    #The A=2 is just hand tuned. Larger A encourages the clustering to split the patch in half
    #A=0 is the previous version of the virtual goniometer
    x = np.sum(v*N,axis=1) + A*np.sum(v*D,axis=1)

    #Clustering
    _, m = withness(x)

    C = np.zeros(n,)
    C[x>m] = 1
    C[x<=m] = 2
    
    P1 = P[C==1,:]
    P2 = P[C==2,:]
    N1 = N[C==1,:]
    N2 = N[C==2,:]
    
    theta, n1, n2 = get_angle(P1,P2,N1,N2,UsePCA = UsePCA, UsePower = UsePower)
    
    
    return C,n1,n2,theta

def ClusteringRandomRP1D(X,T):
    n = X.shape[0]
    d = X.shape[1]
    v = np.random.rand(T,d)
    u = np.mean(X,axis=0)
    wmin = float("inf")
    imin = 0
    
    #w_list = []
    #m_list = []
    
    for i in range(T):
        x = np.sum((v[i,:]-(np.dot(v[i,:],u)/np.dot(v[i,:],v[i,:]))*u)*X,axis=1)
        w,m = withness(x) 
        if w < wmin:
            wmin = w
            imin = i
    
    x = np.sum((v[imin,:]-(np.dot(v[imin,:],u)/np.dot(v[imin,:],v[imin,:]))*u)*X,axis=1)
    
    _,m = withness(x)

    C = np.zeros(n,)
    C[x>m] = 1
    C[x<=m] = 2
    
    return C