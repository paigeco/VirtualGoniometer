"""[ object docstring ]"""

import bpy
from .PairManager import PairManager
from .RegionManager import RegionManager


class MaterialGroupManager(object):
    def __init__(self):
        self.base_default_name = "Base Color"
        self.object_data_dictionary = {}
    
    def create_region(self, context):
        p = context.active_object.cs_individual_VG_.material_regions.add()
        rm = RegionManager(p)
        return rm
    
    def create_pair(self, context, cpolygon_pointer):
        p = context.active_object.cs_individual_VG_.material_pairs.add()
        pm = PairManager(p)
        pm.construct_new(c_polygon_pointer=cpolygon_pointer)
        return pm
    
    def create_base_color(self, context):
        p = context.active_object.cs_individual_VG_.base_region
        p.name = self.base_default_name
        p.context_object = context.active_object
        bm = RegionManager(p)
        bm.apply_all()
        return bm

    def add_pair_to_active(self, context=None, cp=None):
        context = bpy.context if context is None else context
        context_object = context.active_object
        
        try:
            # Ensure a base color exists
            s = self.object_data_dictionary[context_object]['BaseColor']
            _ = self.reset_base_material(context=context) if s is None else None
            
            #Create a pair
            pair = self.create_pair(context, cp)
            self.object_data_dictionary[context_object]['Pairs'].append(pair)
            return pair
        
        except KeyError:
            self.construct_new_object_pair_list(context_object)
            #self.attempt_restore_object_pair_list(context_object)
            self.add_pair_to_active()
    
    def add_region_to_active(self, context=None):
        context = bpy.context if context is None else context
        context_object = context.active_object
        try:
            # Ensure a base color exists
            s = self.object_data_dictionary[context_object]['BaseColor']
            _ = self.reset_base_material(context=context) if s is None else None
            
            # Create a region
            region = self.create_region(context_object)
            self.object_data_dictionary[context_object]['Regions'].append(region)
            return region
        
        except KeyError:
            self.construct_new_object_pair_list(context_object)
            #self.attempt_restore_object_pair_list(context_object)
            self.add_region_to_active(context=context)


    def reset_base_material(self, context=None):
        context = bpy.context if context is None else context
        context_object = context.active_object
        try:
            bc = self.create_base_color(context)
            self.object_data_dictionary[context_object]['BaseColor'] = bc
            return bc
        
        except KeyError:
            self.construct_new_object_pair_list(context_object)
            #self.attempt_restore_object_pair_list(context_object)
            self.reset_base_material()



    def construct_new_object_pair_list(self, context_object):
        self.object_data_dictionary[context_object] = {'Regions':[], 'Pairs':[], 'BaseColor':None}
        #self.reset_base_material()
        
    def attempt_restore_object_pair_list(self, context_object):
        try:
            b_length_stored = len(context_object.material_pairs)
            self.construct_new_object_pair_list(context_object)
            
        except AttributeError:
            b_length_stored = 0
            print('Something has gone very, very wrong.')
        
        
        if b_length_stored > len(self.object_data_dictionary[context_object]):
            for pair in context_object.material_pairs:
                print("Attempting data restore...")
                p = PairManager(pair)
                p.load_from_backup(pair)
                #self.add_material_pair_to_object(context_object, p)
                print("Restored: ", p.bsp.name)
                #print("restore failed")
    
    def return_object_entries(self, context_object, field):
        try:
            return self.object_data_dictionary[context_object][str(field)]
        except KeyError:
            #self.attempt_restore_object_pair_list(context_object)
            self.construct_new_object_pair_list(context_object)
            return self.return_object_entries(context_object, field)
        
    def return_active_object_entries(self, field):
        if bpy.context.active_object is None:
            return []
        else:
            return self.return_object_entries(bpy.context.active_object, field)
    
    def clear_active_object_entries(self):
        if bpy.context.active_object is not None:
            self.construct_new_object_pair_list(bpy.context.active_object)
    
    def return_index_and_object_of_pair_pointer(self, pair):
        ompd = self.object_data_dictionary
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
            self.destroy_by_index(index, 'Pairs', context_object=context_object, destroy=destroy)

        
    def destroy_by_index(self, index, field, context_object=None, destroy=True):
        if context_object is None:
            context_object = bpy.context.active_object
        pair_pointer = self.return_object_entries(context_object, field)[index]
        self.return_object_entries(context_object, field).pop(index)
        if destroy:
            pair_pointer.destroy()
    
    def resync(self, context_object=None):
        if context_object is None:
            context_object = bpy.context.active_object
        b_pairs = bpy.context.active_object.material_pairs.values()
        for i, pair in enumerate(self.return_object_entries(context_object, 'Pairs')):
            pair.blender_store_pointer = b_pairs[i]
