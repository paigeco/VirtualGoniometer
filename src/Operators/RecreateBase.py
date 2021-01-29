"""[ Face Select]"""
from bpy.types import Operator
#from bpy import ops as O
from ..MaterialManagers import ManagerInstance as mi
# OPERATORS >> PERFORMVERTEXSELECT( FILE )
class RecreateBase(Operator):
    """Recreate the Base """
    bl_idname = "view3d.recreate_base_material"
    bl_label = "Recreate Base Material"
    bl_options = {'REGISTER'}
    def execute(self, context):
        mi.Material_Group_Manager.create_base_color(context)
        #override = overide_to_3d_view(context=context)
        #O.view3d.raycast_select_pair(override, 'INVOKE_DEFAULT') # pylint: disable=no-member
        return {'FINISHED'}
