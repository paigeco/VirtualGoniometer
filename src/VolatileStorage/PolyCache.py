""" A hotfix to save memory and cpu operations """

import bpy
from numpy import array, reshape, stack

# STORAGE >> POLYCACHE ( FILE )
class FaceCache():
    """[ Handles face caching to increase performance for
    nearest neighbors searches ]
    """
    def __init__(self):
        self.check_poly = None
        self.all_centers_and_normals = None
       
    def ensure_cache(self):
        """ [ ensures that the cache is up to date]
        """
        #TODO: Implement a random set version of this code instead, but this will do for now
        try:
            if len(bpy.context.active_object.data.polygons) > 0:
                if self.check_poly != bpy.context.active_object.data.polygons[0]:
                    self.check_poly = bpy.context.active_object.data.polygons[0]
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
        print(self.all_centers_and_normals.shape)
    
    def get_centers_and_normals(self):
        """[gets the centers_and_normals]

        Returns:
            [np_array]: [2x3xN array of all centers and normals]
        """
        self.ensure_cache()
        return self.all_centers_and_normals
