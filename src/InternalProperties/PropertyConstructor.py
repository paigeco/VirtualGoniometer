"""[  ]"""
from bpy import types as T
from bpy.props import PointerProperty, CollectionProperty

from .SceneProperties import ControlSettingsTotal_VG_
from .ObjectProperties import ControlSettingsObject_VG_


def construct_extras():
    """[ summary ]"""
    T.Scene.cs_overall_VG_ = PointerProperty(type=ControlSettingsTotal_VG_) # pylint: disable=assignment-from-no-return
    T.Object.cs_individual_VG_ = PointerProperty(type=ControlSettingsObject_VG_) # pylint: disable=assignment-from-no-return