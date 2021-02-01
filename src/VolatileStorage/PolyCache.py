""" A hotfix to save memory and cpu operations """
from random import randint
from numpy import array, reshape

import bpy



# STORAGE >> POLYCACHE ( FILE )
class FaceCache():
    """[ Handles face caching to increase performance for
    nearest neighbors searches ]
    """
    def __init__(self):
        self.random_check = 0
        self.check_poly = None
        self.all_centers_and_normals = None
       
    def ensure_cache(self):
        """ [ ensures that the cache is up to date]
        """
        #Completed: Implement a random set version of this code instead, but this will do for now
        try:
            n = len(bpy.context.active_object.data.polygons)
            if n > 0:
                if self.check_poly != bpy.context.active_object.data.polygons[self.random_check]:
                    self.random_check = randint(0, n)
                    self.check_poly = bpy.context.active_object.data.polygons[self.random_check]
                    self.reset_cache()
                else:
                    pass
            else:
                pass
        except AttributeError:
            pass        
                
    def reset_cache(self):
        """ Redownloads the data for the cache """
        polys = bpy.context.active_object.data.polygons
        n = len(polys)
        li = [None]*n*3
        
        polys.foreach_get('center', li)
        centers = array(li)
        centers = reshape(centers, (n, 3))
        
        polys.foreach_get('normal', li)
        normals = array(li)
        del li
        
        normals = reshape(normals, (n, 3))
        self.all_centers_and_normals = array([centers.tolist(), normals.tolist()])
    
    def get_centers_and_normals(self):
        """[gets the centers_and_normals]

        Returns:
            [np_array]: [2x3xN array of all centers and normals]
        """
        self.ensure_cache()
        return self.all_centers_and_normals
