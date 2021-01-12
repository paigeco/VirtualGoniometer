from bpy import context as C
from bpy.types import Operator
from bpy.ops.object import mode_set

# OPERATORS >> CLEARSELECTION ( FILE )
class ClearSelection(Operator):
    """Clear Selected Patches"""
    bl_idname = "object.clear_selection"
    bl_label = "Clear Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Log the current mode so we can return to it
        save_mode = C.active_object.mode
        
        # Chcange over to object mode so we can change materials
        #mode_set(mode = 'OBJECT')
        
        # Initialize scene, mats & obj for EOU
        cpi = C.active_object.cs_individual_VG_
        ms = C.active_object.data.materials
        
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

        C.active_object.material_pairs.clear()
        material_pair_manager.clear_active_material_pairs()
        
        # Return to the user's mode
        if C.active_object.mode != save_mode:
            mode_set(mode = save_mode)
        
        return {'FINISHED'}
