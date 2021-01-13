""" A hotfix to save memory and cpu operations
"""

from bpy import context as C
from numpy import array

# STORAGE >> POLYCACHE ( FILE )
class FaceCache():
    """[ Handles face caching to increase performance for
    nearest neighbors searches ]
    """
    def __init__(self):
        self.check_poly = None
        self.all_centers_and_normals = None
        #self.ensure_cache()
       
    def ensure_cache(self):
        """ [ ensures that the cache is up to date]
        """
        #TODO: Implement a random set version of this code instead, but this will do for now
        try:
            if len(C.active_object.data.polygons) > 0:
                if self.check_poly != C.active_object.data.polygons[0]:
                    self.check_poly = C.active_object.data.polygons[0]
                    self.reset_cache()
                else:
                    pass
            else:
                pass
        except AttributeError:
            pass        
                
    def reset_cache(self):
        """ [ reruns the cache ]
        """
        #TODO: Good candidate for multiprocessing
        polys = C.active_object.data.polygons
        self.all_centers_and_normals = array(list(map(lambda p: [p.center, p.normal], polys)))
    
    def get_centers_and_normals(self):
        """[gets the centers_and_normals]

        Returns:
            [np_array]: [2x3xN array of all centers and normals]
        """
        self.ensure_cache()
        return self.all_centers_and_normals
