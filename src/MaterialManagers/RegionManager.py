import mathutils
import bpy
import numpy as np
from . import ManagerInstance

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
        if self.bsp.material is None:
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
        self.bsp.material = bpy.data.materials.new(name=str(self.bsp.name))
        
        # add the material to the object
        bpy.context.active_object.data.materials.append(self.bsp.material)
        
        # set the color
        self.bsp.material.diffuse_color = (self.color.r, self.color.g, self.color.b, 1)
        
        # return the object
        return self.bsp.material
    
    def get_material_index(self):
        # get the index of the given material.
        self.material_index = self.bsp.object_material_index
        return self.material_index
        #self.check_existance(self.material,self.destructor())

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
                
    def destroy(self, material_in_index = True):
        save_mode = bpy.context.active_object.mode
        
        i = self.get_material_index()
        print(self.bsp.material.name)
        print(i)
        
        # PLEASE FIX THIS LATER,,, THIS IS A HORRIFIC SOLUTION
        if save_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode = 'OBJECT')
        
        if material_in_index and i is not None and save_mode == 'OBJECT':
            
            self.update_faces_with_material()
            
            #bm_index = base_material.active_base_material().get_material_index()
            bm_index = ManagerInstance.Material_Group_Manager.return_active_object_entries('BaseColor').get_material_index()
            # TODOO: SOLVE THE BM_INDEX

            for face in self.faces:
                if face.material_index == i:
                    face.material_index = bm_index#FIXED: ADD A WAY TO ACCESS THE BASE MATERIAL

            n = self.bsp.global_material_index
            bpy.context.active_object.data.materials.pop(index = n)
        elif material_in_index and i is not None and save_mode == 'EDIT':
            pass   #ADD CODE HERE LAZY BONES
        #finally:
        bpy.data.materials.remove(material = self.bsp.material)
        bpy.ops.object.mode_set(mode = save_mode)
        
            
    def apply_all(self):
        save_mode = bpy.context.active_object.mode

        i = self.get_material_index()
        
        if save_mode != 'OBJECT' and save_mode != 'EDIT':
            # if our user is in sculpting mode or smthn idk
            bpy.ops.object.mode_set(mode = 'EDIT')
            
        if save_mode == 'OBJECT':
            # runs in n time so like not great for large meshes, might wanna change this
            for p in bpy.context.active_object.data.polygons:
                p.material_index = i
                
        elif save_mode == 'EDIT':
            # this is ugly as i'll get out but it works so oh well
            bpy.context.object.active_material_index = i
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.material_slot_assign()
            bpy.ops.mesh.select_all(action='DESELECT')
