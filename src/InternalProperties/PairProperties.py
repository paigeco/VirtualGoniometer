import bpy
from .RegionProperties import MaterialRegion

def return_index_in_struct(self):
    b = self.path_from_id()
    return int("".join(filter(str.isdigit, b)))


class MaterialPair(bpy.types.PropertyGroup):
    # Set the pair name    
    name: bpy.props.StringProperty(default='patch')
    
    index: bpy.props.IntProperty(get=return_index_in_struct)

    # Save the angle
    theta: bpy.props.FloatProperty(default=0.0)
    
    # The centerpoint translation
    center: bpy.props.FloatVectorProperty(default=(0.0, 0.0, 0.0))
    
    # add the object pointer
    context_object: bpy.props.PointerProperty(type=bpy.types.Object)
    
    # patches
    patch_A: bpy.props.PointerProperty(type=MaterialRegion)    
    patch_B: bpy.props.PointerProperty(type=MaterialRegion)
