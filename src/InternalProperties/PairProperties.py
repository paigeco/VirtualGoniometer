from bpy.props import StringProperty, IntProperty, PointerProperty, FloatVectorProperty
from bpy.props import FloatProperty

from bpy.types import PropertyGroup, Object
from .RegionProperties import MaterialRegion

def return_index_in_struct(self):
    try:
        b = self.path_from_id()
        return int("".join(filter(str.isdigit, b)))
    except ValueError:
        print("error")
        return 2147483647
    

def get_measurement_index(self):
    count = 1
    pairs = self.context_object.cs_individual_VG_.material_pairs
    for pair in pairs:
        if pair.break_index == self.break_index:
            if pair.patch_A == self.patch_A and pair.patch_B == self.patch_B:
                break
            count += 1
    return count

def get_name(self):
    return 'Break ({}) - M({})'.format(self.break_index, self.measurement_index)

class MaterialPair(PropertyGroup):
    flavor_text: StringProperty(default="")
    
    break_index: IntProperty(default=0)

    # Save the angle
    theta: FloatProperty(default=0.0)
    
    # Number of points
    number_of_points: IntProperty()
    
    created_since_epoch: IntProperty()
    # Radius
    radius: FloatProperty()
    
    # The centerpoint translation
    center: FloatVectorProperty(default=(0.0, 0.0, 0.0))
    
    # Set the pair name
    name: StringProperty(get=get_name)
    index: IntProperty(get=return_index_in_struct)
    measurement_index: IntProperty(get=get_measurement_index)
    
    # add the object pointer
    context_object: PointerProperty(type=Object)
    
    # patches
    patch_A: PointerProperty(type=MaterialRegion)    
    patch_B: PointerProperty(type=MaterialRegion)
