# QUESTIONABLE PACKAGES
try:
    import scipy.io as sio
    from sklearn.neighbors import NearestNeighbors
    import sklearn.decomposition as decomp
    
except ImportError:
    pass

def register():
    [bpy.utils.register_class(icla) for icla in CLASS_LIST]
    
    bpy.types.Scene.cs_overall_VG_ = bpy.props.PointerProperty(type=ControlSettingsTotal_VG_)
    
    object_init()
    

def object_init():
    bpy.types.Object.material_pairs = bpy.props.CollectionProperty(type=MaterialPairProperties)
    
    bpy.types.Object.cs_individual_VG_ = bpy.props.PointerProperty(type=ControlSettingsObject_VG_)

def unregister():
    [bpy.utils.unregister_class(icla) for icla in CLASS_LIST]


if __name__ == "__main__":
    
    global_variable_init_preregistration()
    
    register()
    
    global_variable_init_postregistration()
