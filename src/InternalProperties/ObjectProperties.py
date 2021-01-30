""" [ Object Properties ] """
from bpy.props import IntProperty, BoolVectorProperty, PointerProperty
from bpy.props import BoolProperty, CollectionProperty
from bpy.types import PropertyGroup, Object
from .PairProperties import MaterialPair
from .RegionProperties import MaterialRegion

def get_bpairs_len(self):
    return len(self.material_pairs)

def get_bregion_len(self):
    return len(self.material_regions)

class VirtualGoniometerObject_VG_(PropertyGroup):
    """[ Object  ]"""
    cp_index: IntProperty(default=0)
    
    pair_list_length: IntProperty(get=get_bpairs_len)
    
    region_list_length: IntProperty(get=get_bregion_len)
    
    # add the object pointer
    object: PointerProperty(type=Object)
    
    base_region: PointerProperty(type=MaterialRegion)

    material_regions: CollectionProperty(type=MaterialRegion) # pylint: disable=assignment-from-no-return
    
    material_pairs: CollectionProperty(type=MaterialPair) # pylint: disable=assignment-from-no-return 
    
    
    # Control Panel variables
    depressed: BoolVectorProperty(default=(False, False), size=2)
    
    is_patch_editor_active: BoolProperty(default=False)
    
    is_side_one_active: BoolProperty(default=True)
    
    active_patch_index: IntProperty(default=0)
    