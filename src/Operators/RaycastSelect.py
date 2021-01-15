""" [ raycast select module ] """
from bpy.types import Operator
import bpy
from bpy import ops as O

from .RaycastFunctions.DoRaycast import do_raycast
from .RaycastFunctions.CallbackOptions import move_cursor, run_by_selection


class PerformRaycastSelect(Operator):
    """Run a side differentiation and select the points by raycast"""
    bl_idname = "view3d.raycast_select_pair"
    bl_label = "RayCast Select Operator"
    bl_options = {'REGISTER', 'UNDO'}
    save_mode = None
    def modal(self, context, event):
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            # allow navigation
            return {'PASS_THROUGH'}
        elif event.type == 'MOUSEMOVE':
            do_raycast(context, event, move_cursor)
            return {'RUNNING_MODAL'}
        elif event.type == 'LEFTMOUSE':
            do_raycast(context, event, run_by_selection)
            return {'RUNNING_MODAL'}
        elif event.type in {'RIGHTMOUSE', 'ESC'} or context.active_object.mode != 'OBJECT':
            bpy.context.space_data.overlay.show_cursor = False
            O.object.mode_set(mode=self.save_mode)
            return {'CANCELLED'}
            
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):        
        if context.space_data.type == 'VIEW_3D':
            self.save_mode = context.active_object.mode
            bpy.context.space_data.overlay.show_cursor = True
            if self.save_mode != 'OBJECT':
                O.object.mode_set(mode='OBJECT')
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}
