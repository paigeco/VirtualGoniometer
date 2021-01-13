import bpy
bpy.types.Scene.cs_overall_VG_ = bpy.props.PointerProperty(type=ControlSettingsTotal_VG_)
bpy.types.Object.material_pairs = bpy.props.CollectionProperty(type=MaterialPairProperties)
bpy.types.Object.cs_individual_VG_ = bpy.props.PointerProperty(type=ControlSettingsObject_VG_)