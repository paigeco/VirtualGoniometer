"""[ object docstring ]"""

import bpy
from bpy.types import OBJECT_PT_context_object, Region
from mathutils import Color
from .PairManager import PairManager
from .RegionManager import RegionManager


class MaterialGroupManager(object):
    def __init__(self):
        self.p = bpy.context.active_object.cs_individual_VG_
        self.base_default_name = "Base Color"
        self.object_data_dictionary = {}
    
    def create_region(self):
        self.p = bpy.context.active_object.cs_individual_VG_
        p = self.p.material_regions.add()
        rm = RegionManager(p)
        return rm
    
    def create_pair(self):
        self.p = bpy.context.active_object.cs_individual_VG_
        p = self.p.material_pairs.add()
        pm = PairManager(p)
        return pm
    
    def create_base_color(self):
        self.p = bpy.context.active_object.cs_individual_VG_
        p = self.p.base_region
        bm = RegionManager(p)
        return bm

    def add_pair_to_active(self):
        context_object = bpy.context.active_object
        try:
            
            pair = self.create_pair()
            self.object_data_dictionary[context_object]['Pairs'].append(pair)
            
        except KeyError:
            self.construct_new_object_pair_list(context_object)
            #self.attempt_restore_object_pair_list(context_object)
            self.add_pair_to_active()
    
    def add_region_to_active(self):
        context_object = bpy.context.active_object
        try:
            
            region = self.create_region()
            self.object_data_dictionary[context_object]['Regions'].append(region)
            return region
        
        except KeyError:
            self.construct_new_object_pair_list(context_object)
            #self.attempt_restore_object_pair_list(context_object)
            self.add_region_to_active()


    def reset_base_material(self):
        context_object = bpy.context.active_object
        try:
            
            bc = self.create_region()
            self.object_data_dictionary[context_object]['BaseColor'] = bc
            return bc
        
        except KeyError:
            self.construct_new_object_pair_list(context_object)
            #self.attempt_restore_object_pair_list(context_object)
            self.reset_base_material()



    def construct_new_object_pair_list(self, context_object):
        self.object_data_dictionary[context_object] = {'Regions':[], 'Pairs':[], 'BaseColor':None}
        self.reset_base_material()
        
    def attempt_restore_object_pair_list(self, context_object):
        try:
            b_length_stored = len(context_object.material_pairs)
            self.construct_new_object_pair_list(context_object)
            
        except AttributeError:
            b_length_stored = 0
            print('Something has gone very, very wrong.')
        
        
        if (b_length_stored > len(self.object_data_dictionary[context_object])):
            for pair in context_object.material_pairs:
                print("Attempting data restore...")
                p = PairManager()
                p.load_from_backup(pair)
                self.add_material_pair_to_object(context_object, p)
                print("Restored: ", p.name)
                #print("restore failed")
    
    def return_object_material_pairs(self, context_object):
        try:
            return self.object_data_dictionary[context_object]
        except KeyError:
            #self.attempt_restore_object_pair_list(context_object)
            self.construct_new_object_pair_list(context_object)
            return self.return_object_material_pairs(context_object)

        
    def return_active_material_pairs(self):
        if bpy.context.active_object is None:
            return []
        else:
            return self.return_object_material_pairs(bpy.context.active_object)
    
    def clear_active_material_pairs(self):
        if bpy.context.active_object is not None:
            self.construct_new_object_pair_list(bpy.context.active_object)
    
    def return_index_and_object_of_pair_pointer(self, pair):
        ompd = self.object_material_pairs_dictionary
        for key_object in ompd:
            for index, check_pair in enumerate(ompd[key_object]):
                if check_pair is pair:
                    return index, key_object
        
        return None, None
    
    def destroy_by_active_pair_pointer(self, pair_pointer, destroy=True):
        index, context_object = self.return_index_and_object_of_pair_pointer(pair_pointer)
        if index is None or context_object is None:
            pass
        else:
            self.destroy_by_index(index, context_object=context_object, destroy=destroy)

        
    def destroy_by_index(self, index, context_object=None, destroy=True):
        if context_object is None:
            context_object = bpy.context.active_object
        pair_pointer = self.return_object_material_pairs(context_object)[index]
        self.return_object_material_pairs(context_object).pop(index)
        if destroy:
            pair_pointer.destroy()
    
    def resync(self, context_object=None):
        if context_object is None:
            context_object = bpy.context.active_object
        b_pairs = bpy.context.active_object.material_pairs.values()
        for i, pair in enumerate(self.return_active_material_pairs()):
            pair.blender_store_pointer = b_pairs[i]





class BaseMaterialManager():
    
    def apply_all(self):
        save_mode = bpy.context.active_object.mode

        i = self.active_base_material().get_material_index()
        
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
        
        # Return to the user's mode
        bpy.ops.object.mode_set(mode = save_mode)

    def handle_blender_storage(self):
        # add it to the blender storage
        context = bpy.context.active_object
        cpi = bpy.context.active_object.cs_individual_VG_
        cpi.base_material = self.active_base_material().material
    
    def create_new(self):
        context = bpy.context.active_object
        self.base_material_dict[context] = MaterialManager(name = self.name, color = self.default_color)
    
    def attempt_recovery(self):
        try:
            cpi = bpy.context.active_object.cs_individual_VG_
            context = bpy.context.active_object
            self.base_material_dict[context] = MaterialManager(name = self.name, material = cpi.base_material)
            self.active_base_material().check_existance(self.create_new)
        except AttributeError:
            self.create_new()
        
    def create(self):
        self.attempt_recovery()
        self.apply_all()
        self.handle_blender_storage()
        
    def active_base_material(self):
        return self.base_material_dict[bpy.context.active_object]