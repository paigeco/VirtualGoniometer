"""[ summary ]"""

from bpy.types import Operator
from bpy.props import IntProperty

class DeletePatch(Operator):
    """Deletes this specific patch"""
    bl_idname = 'object.deletepatch'
    bl_label = 'Delete Patch'
    bl_description = 'Deletes this specific patch'
    bl_options = {'REGISTER', 'UNDO'}

    patch_int: IntProperty(default=0)

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
