"""[ Face Select]"""
from bpy.types import Operator
from bpy.ops.object import mode_set
from bpy.ops import view3d
from Operators.ContextOveride import overide_to_3d_view

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
        override = overide_to_3d_view(context=context)
        view3d.raycast_select_pair(override, 'INVOKE_DEFAULT') # pylint: disable=no-member
        return {'FINISHED'}
