"""[summary]

Returns:
    [type]: [description]
"""


from bpy import ops as O
from bpy import context as C
from bpy.types import Operator

# OPERATORS >> CENTERSAMPLE ( FILE )
class CenterSample(Operator):
    """Center Sample"""
    bl_idname = "object.center_sample"
    bl_label = "Center Sample"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        save_mode = C.active_object.mode
        O.object.mode_set(mode='OBJECT')
        #base_material.attempt_recovery()
        O.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        O.object.location_clear()
        O.object.mode_set(mode=save_mode)
        return {'FINISHED'}
