import bpy
import numpy as np
# STORAGE >> FACECACHE ( FILE )
class FaceCache():
    def __init__(self):
        self.check_poly = None
        self.ensure_cache()
        
    def ensure_cache(self):
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
        self.all_centers_and_normals = np.array(list(map(lambda p: [p.center,p.normal], bpy.context.active_object.data.polygons)))
    
    def get_CNs(self):
        self.ensure_cache()
        return self.all_centers_and_normals