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
            bpy.ops.object.mode_set(mode='OBJECT')
        override = find_3d_view_override(context)
        bpy.ops.view3d.raycast_select_pair(override, 'INVOKE_DEFAULT')
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
