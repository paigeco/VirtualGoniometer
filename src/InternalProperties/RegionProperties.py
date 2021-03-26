from bpy.types import Material, Object, PropertyGroup
from bpy.props import StringProperty, PointerProperty, FloatVectorProperty, IntProperty
import bpy

from ..VolatileStorage import CacheInstance as ci

def local_material_index(self):
    for i, slot in enumerate(bpy.context.active_object.material_slots):
        if slot.name == self.material.name_full:
            #self.material_index = i
            return i
    return 2147483647 #returns the largest number in an int

def global_material_index(self):
    for i, slot in enumerate(bpy.data.materials):
        if slot.name == self.material.name_full:
            #self.material_index = i
            return i
    return 2147483647 #returns the largest number in an int

def material_color_name(self):
    return ci.TranslateColor.get_color_name_from_tuple(self.default_color)

class MaterialRegion(PropertyGroup):    
    """[ Material Region ]"""
    name: StringProperty(default='Patch')
    
    global_material_index: IntProperty(get=global_material_index)
    
    local_material_index: IntProperty(get=local_material_index)
    
    material: PointerProperty(type=Material)
    
    default_color: FloatVectorProperty(default=(1.0, 1.0, 1.0))
    
    color_name: StringProperty(get=material_color_name)
    
    context_object: PointerProperty(type=Object)
