import bpy

class MaterialRegion(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(default = 'Patch')
    material: bpy.props.PointerProperty(type=bpy.types.Material)
    original_color: bpy.props.FloatVectorProperty(default = (0.0,0.0,0.0))
    context_object: bpy.props.PointerProperty(type=bpy.types.Object)

