import bpy

'''
def get_objects_len(self):
    return len(material_pair_manager.return_active_material_pairs())
'''
class ControlSettingsTotal_VG_(bpy.types.PropertyGroup):
    
    accesibility_level: bpy.props.IntProperty(name='Accesibility Level',
        soft_min=0, soft_max=3, step=1, default=3)
        
    number_of_nearest_neighbors: bpy.props.IntProperty(name='Number of Points',
        soft_min=0, soft_max=5000, step=10, default=500)
        
    number_of_random_projections: bpy.props.IntProperty(name='Number of Iterations',
        soft_min=0, soft_max=100, step=1, default=10)
    
    default_base_color: bpy.props.FloatVectorProperty(name = 'Default Base Color', default = (0.0,0.0,0.0))
