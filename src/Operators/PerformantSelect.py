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