import bpy

from .SceneProperties import ControlSettingsTotal_VG_
from .ObjectProperties import ControlSettingsObject_VG_
from .PairProperties import MaterialPair
from .RegionProperties import MaterialRegion

def construct():
    bpy.types.Scene.cs_overall_VG_ = bpy.props.PointerProperty(type=ControlSettingsTotal_VG_)
    bpy.types.Object.cs_individual_VG_ = bpy.props.PointerProperty(type=ControlSettingsObject_VG_)
    bpy.types.Object.material_pairs = bpy.props.CollectionProperty(type=MaterialPair)
