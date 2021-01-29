import bpy
from .src.MaterialManagers.ManagerInstance import construct_mgm
from .src.VolatileStorage.CacheInstance import construct_cache
from .src.InternalProperties.SceneProperties import ControlSettingsTotal_VG_
from .src.InternalProperties.ObjectProperties import VirtualGoniometerObject_VG_
from .src.VolatileStorage.PolyCache import FaceCache

def load_m():
    bpy.types.Scene.cs_overall_VG_ = bpy.props.PointerProperty(type=ControlSettingsTotal_VG_) # pylint: disable=assignment-from-no-return
    bpy.types.Object.cs_individual_VG_ = bpy.props.PointerProperty(type=VirtualGoniometerObject_VG_) # pylint: disable=assignment-from-no-return
    construct_mgm()
    construct_cache()
