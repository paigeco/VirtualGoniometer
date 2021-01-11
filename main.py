import bpy, bmesh
from bpy.types import ColorManagedSequencerColorspaceSettings

import numpy as np
from mathutils import Color
import time

# QUESTIONABLE PACKAGES
try:
    import scipy.io as sio
    from sklearn.neighbors import NearestNeighbors
    import sklearn.decomposition as decomp
    
except ImportError:
    pass


# OPERATORS >> CENTERSAMPLE ( FILE )
class CenterSample(bpy.types.Operator):
    """Center Sample"""
    bl_idname = "object.center_sample"
    bl_label = "Center Sample"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        save_mode = bpy.context.active_object.mode
        bpy.ops.object.mode_set(mode = 'OBJECT')
        #base_material.attempt_recovery()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        bpy.ops.object.location_clear()
        bpy.ops.object.mode_set(mode = save_mode)
        return {'FINISHED'}

# OPERATORS >> CLEARSELECTION ( FILE )
class ClearSelection(bpy.types.Operator):
    """Clear Selected Patches"""
    bl_idname = "object.clear_selection"
    bl_label = "Clear Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Log the current mode so we can return to it
        save_mode = bpy.context.active_object.mode
        
        # Chcange over to object mode so we can change materials
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        
        # Initialize scene, mats & obj for EOU
        cpi = bpy.context.active_object.cs_individual_VG_
        ms = bpy.context.active_object.data.materials
        
        # Reset status variables to default
        cpi.property_unset('cp_index')
        cpi.property_unset('is_patch_editor_active')
        cpi.property_unset('is_side_one_active')
        
        # Remove everything from the patches
        pairs = material_pair_manager.return_active_material_pairs()
        for pair in reversed(pairs):
            pair.destroy()
            material_pair_manager.resync()
        
        # Check if base material exists after this process
        #base_material.attempt_recovery()

        bpy.context.active_object.material_pairs.clear()
        material_pair_manager.clear_active_material_pairs()
        
        # Return to the user's mode
        #bpy.ops.object.mode_set(mode = save_mode)
        
        return {'FINISHED'}




class DeletePatch(bpy.types.Operator):
    """Deletes this specific patch"""
    bl_idname = 'object.deletepatch'
    bl_label = 'Delete Patch'
    bl_description = 'Deletes this specific patch'
    bl_options = {'REGISTER', 'UNDO'}

    patch_int: bpy.props.IntProperty(default=0)

    def execute(self, context):
        print(self.patch_int)
        
        pairs = material_pair_manager.return_active_material_pairs()
        pairs[self.patch_int].destroy()
        material_pair_manager.resync()
        
        # Log the current mode so we can return to it
        #save_mode = bpy.context.active_object.mode
        
        #bpy.ops.object.mode_set(mode = 'OBJECT')  
        
        # REMOVE THE PATCH
               
        # Return to the user's mode
        #if bpy.context.active_object.mode != save_mode:
            #bpy.ops.object.mode_set(mode = save_mode)

        return {'FINISHED'}


class EditSide(bpy.types.Operator):
    bl_idname = 'view3d.editside'
    bl_label = 'Edit Side'
    bl_description = 'Edit Side'
    bl_options = {'REGISTER', 'UNDO'}
    
    save_mode: bpy.props.StringProperty(default = 'OBJECT')
    options: bpy.props.IntVectorProperty(name = 'side edit options',
        description = '[ Side Integer (1 or 2), Material Pair Integer (i)]',
        default = (0,0),
        size=2)
    def execute(self, context):
        # Log the current mode so we can return to it
        cpi = bpy.context.active_object.cs_individual_VG_
        
        #Handle material pairs
        pairs = material_pair_manager.return_active_material_pairs()
        active_pair = pairs[int(self.options[1])]
        
        m1, m2 = active_pair.refresh_material_indexes()
        
        baseindex = base_material.active_base_material().get_material_index()
                    
        if self.options[0] == 1:
            mi = m1
            cpi.is_side_one_active = True
            cpi.depressed = (True,False)
        else:
            mi = m2
            cpi.is_side_one_active = False
            cpi.depressed = (False,True)
        

        if cpi.is_patch_editor_active:
            cpi.is_patch_editor_active = False
            cpi.depressed = (False,False)
            if self.save_mode != 'OBJECT':

                if self.save_mode != 'EDIT':
                    bpy.ops.object.mode_set(mode = 'EDIT')
                
                v_temp = []
                bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
                for v in bm.faces:
                    if v.select:
                        v_temp.append(v)
                
                bmesh.update_edit_mesh(bpy.context.active_object.data)
                
                bpy.context.active_object.active_material_index = baseindex
                bpy.ops.object.material_slot_select()
                
                bpy.context.active_object.active_material_index = mi
                bpy.ops.object.material_slot_select()
                
                bpy.context.active_object.active_material_index = baseindex
                bpy.ops.object.material_slot_assign()
                
                bpy.ops.mesh.select_all(action = 'DESELECT')
                
                for v in v_temp:
                    v.select = True
                    print(v.normal)
                bmesh.update_edit_mesh(bpy.context.active_object.data)
                
                bpy.context.active_object.active_material_index = mi
                bpy.ops.object.material_slot_assign()
                
                #active_pair.get_angle()
                
                
                #bpy.ops.mesh.select_all(action = 'DESELECT')
            elif self.save_mode == 'OBJECT':
                bpy.ops.mesh.select_all(action = 'DESELECT')
                #APPLY PATCH CHANGES
                # Set to object mode
                bpy.ops.object.mode_set(mode = 'OBJECT')
                
                for po in bpy.context.active_object.data.polygons:
                    if po.select:
                        po.material_index = mi
                        #po.select = False
                
               # active_pair.get_angle()
            # Return to the user's mode
            if bpy.context.active_object.mode != self.save_mode:
                bpy.ops.object.mode_set(mode = self.save_mode)

        else:
            self.save_mode = str(bpy.context.active_object.mode)
            # HIGHLIGHT_PATCH
            if self.save_mode != 'EDIT':
                bpy.ops.object.mode_set(mode = 'EDIT')
            
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.context.active_object.active_material_index = mi
            bpy.ops.object.material_slot_select()

            # SET for Embossing
            cpi.active_patch_index = int(self.options[1])
            cpi.is_patch_editor_active = True

        return {'FINISHED'}


# OPERATORS >> PERFORMOPTIMALSELECT( FILE )
class PerformOptimalSelect(bpy.types.Operator):
    """Perform Side Differentiation"""
    bl_idname = "view3d.run_optimal_select"
    bl_label = "Side Differentiation"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        save_mode = context.active_object.mode
        override = find_3d_view_override(context)
        if save_mode == 'OBJECT':
            bpy.ops.view3d.raycast_select_pair(override,'INVOKE_DEFAULT')
        elif save_mode == 'EDIT':
            bpy.ops.view3d.face_select_pair()
        return {'FINISHED'}


# OPERATORS >> PERFORMVERTEXSELECT( FILE )
class PerformFaceSelect(bpy.types.Operator):
    """Run a side differentiation and select the center point of a region by face"""
    bl_idname = "view3d.face_select_pair"
    bl_label = "Face Select Operator"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        save_mode = context.active_object.mode
        if save_mode == 'OBJECT':
            pass
        elif save_mode == 'EDIT':
            bpy.ops.object.mode_set(mode = 'OBJECT')
        override = find_3d_view_override(context)
        bpy.ops.view3d.raycast_select_pair(override,'INVOKE_DEFAULT')
        return {'FINISHED'}

# OPERATORS >> RAYCASTSELECT ( FILE )
# requires:
#     CALLBACKOPTS


# REGISTRY ( FOLDER ) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def register():
    [bpy.utils.register_class(icla) for icla in CLASS_LIST]
    
    bpy.types.Scene.cs_overall_VG_ = bpy.props.PointerProperty(type=ControlSettingsTotal_VG_)
    
    object_init()
    

def object_init():
    bpy.types.Object.material_pairs = bpy.props.CollectionProperty(type=MaterialPairProperties)
    
    bpy.types.Object.cs_individual_VG_ = bpy.props.PointerProperty(type=ControlSettingsObject_VG_)

def unregister():
    [bpy.utils.unregister_class(icla) for icla in CLASS_LIST]


if __name__ == "__main__":
    
    global_variable_init_preregistration()
    
    register()
    
    global_variable_init_postregistration()
