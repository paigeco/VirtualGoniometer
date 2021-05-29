#from bpy import ops
from bpy.types import Operator


#from ..MaterialManagers import ManagerInstance as mi
from ..MeshSegmentation.ClusteringDriver import segment_mesh
# OPERATORS >> CLEARSELECTION ( FILE )
class SegmentMesh(Operator):
    """Segment Mesh"""
    bl_idname = "object.segment_mesh"
    bl_label = "Segment Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Log the current mode so we can return to it
        segment_mesh(context)
        return {'FINISHED'}
