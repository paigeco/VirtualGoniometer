from bpy.types import Operator
from bpy import context as C
from bpy.ops.object import mode_set

# OPERATORS >> PERFORMVERTEXSELECT( FILE )
class PerformFaceSelect(Operator):
    """Run a side differentiation and select the center point of a region by face"""
    bl_idname = "view3d.face_select_pair"
    bl_label = "Face Select Operator"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        save_mode = context.active_object.mode
        if save_mode == 'OBJECT':
            pass
        elif save_mode == 'EDIT':
            mode_set(mode='OBJECT')
        override = find_3d_view_override(context)
        bpy.ops.view3d.raycast_select_pair(override, 'INVOKE_DEFAULT')
        return {'FINISHED'}