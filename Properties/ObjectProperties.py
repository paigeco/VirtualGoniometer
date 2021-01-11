import bpy

def get_bpairs_len(self):
    return len(bpy.context.active_object.material_pairs)

class ControlSettingsObject_VG_(bpy.types.PropertyGroup):
    cp_index: bpy.props.IntProperty(default=0)
    
    pair_list_length: bpy.props.IntProperty(get=get_bpairs_len)
    
    depressed: bpy.props.BoolVectorProperty(default = (False, False), size = 2)
    # add the object pointer
    object: bpy.props.PointerProperty(type=bpy.types.Object)
    
    base_material: bpy.props.PointerProperty(type=bpy.types.Material)
    
    is_patch_editor_active: bpy.props.BoolProperty(default=False)
    
    is_side_one_active: bpy.props.BoolProperty(default=True)
    
    active_patch_index: bpy.props.IntProperty(default=0)