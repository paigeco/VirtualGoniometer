import mathutils
import bpy
import numpy as np

class RegionManager():
    """ Controls a single material
    """
    def __init__(self, storage_pointer):
        self.material_index = 0
        self.bsp = storage_pointer

        # Set color
        # Initiailize the faces
        self.faces = []
        
        self.color = mathutils.Color(self.bsp.default_color)
        # Create the constituent material
        self.create_material()
        

        #else:
        #    self.bsp.material = material
        #    self.bsp.name = material.name
        #    self.bsp.dc  = material.diffuse_color
        #    self.color = mathutils.Color((dc[0],dc[1],dc[2]))
        
        # Find all the faces
        self.update_faces_with_material()
        
        # Set the mathematical components
        self.get_face_mathematical_components()
    
    def create_material(self):
        
        # create a new material
        material = bpy.data.materials.new(name=str(self.bsp.name))
        
        # add the material to the object
        
        self.bsp.context_object.data.materials.append(material)
        
        # set the color
        material.diffuse_color = (self.color.r, self.color.g, self.color.b, 1)
        
        self.bsp.material = material
        # return the object
        return self.bsp.material
    
    def get_material_index(self):
        # get the index of the given material.
        self.material_index = self.bsp.local_material_index
        if self.material_index != 2147483647:
            return self.material_index
        else:
            pass
            #Attempt restore and if not, delete parent pair

    def apply_to_faces_by_face_index(self, face_indexes):
        original_area = bpy.context.area.type
        bpy.context.area.type = 'VIEW_3D'


        self.get_material_index()
        for index in face_indexes:
            bpy.context.object.data.polygons[index].material_index = self.material_index
        bpy.context.area.type = original_area

    def update_faces_with_material(self):
        self.get_material_index()
        self.faces = []
        for face in bpy.context.active_object.data.polygons:
            if face.material_index == self.material_index:
                self.faces.append(face)
    
    def get_face_mathematical_components(self):
        self.update_faces_with_material()
        normals = []
        centers = []

        for f in self.faces:
            normals.append(f.normal)
            centers.append(f.center)
        
        self.normals = np.array(normals)
        self.centers = np.array(centers)
    
    def set_color_from_MU_object(self):
        self.bsp.material.diffuse_color = (self.color.r, self.color.g, self.color.b, 1.0)
        

    def check_existance(self, callback):
        for i in range(len(bpy.context.active_object.material_slots)):
            if bpy.context.active_object.material_slots[i].name == self.bsp.material.name_full:
                return
        callback()
                
    def destroy(self):
        cpi = bpy.context.active_object.cs_individual_VG_
        p = self.bsp.context_object.data.polygons
        
        bm_index = cpi.base_region.local_material_index
        
        
        # Resets the material patches to remove the 
        l_index = self.bsp.local_material_index
        if l_index != 2147483647: # l_index is set to the largest index if the material is not found
            li = [None]*len(p)
            
            
            p.foreach_get('material_index', li)
            
            for i, l in enumerate(li):
                if l_index == l:
                    li[i] = bm_index
            
            p.foreach_set('material_index', li)
            bpy.context.active_object.data.materials.pop(index=l_index)
        
        # Removes the material from the data if it hasn't been already
        g_index = self.bsp.local_material_index
        if g_index != 2147483647:
            bpy.data.materials.remove(material=self.bsp.material)     
    
        #cpi.material_regions.remove(self.bsp)       
        
        
    def apply_all(self):
        """ [ Applies the given region to the context objects ]
        """
        material_index = self.get_material_index()
        
        p = self.bsp.context_object.data.polygons
        li = [material_index]*len(p)
        p.foreach_set('material_index', li)
        
        
        
