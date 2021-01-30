"""[ summary ]"""

from bpy.types import Operator
from bpy.props import IntProperty
from ..MaterialManagers import ManagerInstance as mi

class DeletePatch(Operator):
    """Deletes this specific patch"""
    bl_idname = 'object.deletepatch'
    bl_label = 'Delete Patch'
    bl_description = 'Deletes this specific patch'
    bl_options = {'REGISTER', 'UNDO'}

    patch_int: IntProperty(default=0)

    def execute(self, context):
        print(self.patch_int)
        pairs = mi.Material_Group_Manager.return_active_object_entries('Pairs')
        pairs[self.patch_int].destroy()
        mi.Material_Group_Manager.remove_item('Pairs', self.patch_int, context=context)
        mi.Material_Group_Manager.resync(context_object=context.active_object)
        
        # Log the current mode so we can return to it
        #save_mode = bpy.context.active_object.mode
        
        #bpy.ops.object.mode_set(mode = 'OBJECT')  

        # Return to the user's mode
        #if bpy.context.active_object.mode != save_mode:
            #bpy.ops.object.mode_set(mode = save_mode)

        return {'FINISHED'}
