from bpy.types import Operator
from bpy import ops as O
from .ContextOveride import overide_to_3d_view


# OPERATORS >> PERFORMOPTIMALSELECT( FILE )
class PerformOptimalSelect(Operator):
    """Perform Side Differentiation"""
    bl_idname = "view3d.run_optimal_select"
    bl_label = "Side Differentiation"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        save_mode = context.active_object.mode
        override = overide_to_3d_view(context)
        if save_mode == 'OBJECT':
            O.view3d.raycast_select_pair(override, 'INVOKE_DEFAULT') # pylint: disable=no-member
        elif save_mode == 'EDIT':
            O.view3d.face_select_pair() # pylint: disable=no-member
        return {'FINISHED'}
