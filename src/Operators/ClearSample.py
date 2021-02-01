from bpy import ops
from bpy.types import Operator


from ..MaterialManagers import ManagerInstance as mi



# OPERATORS >> CLEARSELECTION ( FILE )
class ClearSelection(Operator):
    """Clear Selected Patches"""
    bl_idname = "object.clear_selection"
    bl_label = "Clear Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Log the current mode so we can return to it
        save_mode = context.active_object.mode
        
        co = context.active_object
        # Chcange over to object mode so we can change materials
        #mode_set(mode = 'OBJECT')
        
        # Initialize scene, mats & obj for EOU
        cpi = co.cs_individual_VG_
        
        cpi.material_pairs.clear()
        cpi.material_regions.clear()
        
        # Reset status variables to default
        cpi.property_unset('cp_index')
        cpi.property_unset('is_patch_editor_active')
        cpi.property_unset('is_side_one_active')
        cpi.property_unset('breaks')

        # Remove everything from the patches
        mi.Material_Group_Manager.construct_new_object_pair_list(co)
        co.data.materials.clear()
        
        mi.Material_Group_Manager.reset_base_material(context=context)
        
        # Return to the user's mode
        if context.active_object.mode != save_mode:
            ops.object.mode_set(mode=save_mode)
        
        return {'FINISHED'}
