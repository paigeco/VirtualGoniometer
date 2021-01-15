from bpy.types import Material, Object, PropertyGroup
from bpy.props import StringProperty, PointerProperty, FloatVectorProperty, IntProperty
import bpy

def local_material_index(self):
    for i, slot in enumerate(bpy.context.active_object.material_slots):
        if slot.name == self.material.name_full:
            #self.material_index = i
            return i
    return None

def global_material_index(self):
    for i, slot in enumerate(bpy.data.materials):
        if slot.name == self.material.name_full:
            #self.material_index = i
            return i
    return None

class MaterialRegion(PropertyGroup):    
    """[ Material Region ]"""
    name: StringProperty(default='Patch')
    
    global_material_index: IntProperty(get=global_material_index)
    
    object_material_index: IntProperty(get=local_material_index)
    
    #object_region_index: IntProperty(get=)
    
    material: PointerProperty(type=Material)
    
    default_color: FloatVectorProperty(default=(0.0, 0.0, 0.0))
    
    context_object: PointerProperty(type=Object)

