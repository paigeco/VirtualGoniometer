from bpy.props import IntProperty, BoolVectorProperty, PointerProperty, BoolProperty, CollectionProperty
from .PairProperties import MaterialPair
from .RegionProperties import MaterialRegion

def get_bpairs_len(self):
    return len(self.material_pairs)

class VirtualGoniometerObject_VG_(bpy.types.PropertyGroup):
    cp_index: bpy.props.IntProperty(default=0)
    
    pair_list_length: bpy.props.IntProperty(get=get_bpairs_len)
    
    depressed: bpy.props.BoolVectorProperty(default=(False, False), size=2)
    # add the object pointer
    object: bpy.props.PointerProperty(type=bpy.types.Object)
    
    base_material: PointerProperty(type=bpy.types.Material)
    
    is_patch_editor_active: BoolProperty(default=False)
    
    is_side_one_active: BoolProperty(default=True)
    
    active_patch_index: IntProperty(default=0)
    
    material_regions: 
    
    material_pairs: CollectionProperty(type=MaterialPair) # pylint: disable=assignment-from-no-return


snake_case_looks_like_this

ClassesAreLikeThis

