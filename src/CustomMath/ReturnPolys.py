import bpy
from numpy import array
from .Neighbors3D import NearestNeighbors3D
from ..VolatileStorage import CacheInstance as ci

def get_data_from_selected_object(selected_polygon_pointers):
    # TODOO REMOVE THIS! THIS IS A GLITCHY HOTFIX THAT FORCES
    # THE USER INTO FACE EDIT MODE
    '''
    if(bpy.context.tool_settings.mesh_select_mode[0] == True):
        bpy.context.tool_settings.mesh_select_mode = (False,False,True)
    elif(bpy.context.tool_settings.mesh_select_mode[2] == True):
        pass
        print("ALL GOOD")
    '''
    all_centers_and_normals = []
    all_selected_centers = []
    
    if bpy.context.active_object.mode == 'EDIT':
        # get the selected object
        #obj = bpy.context.active_object
        # IN DEVELOPMENT, TODOO MAKE IT WORK IN VERTEX MODE FOR THE HEATHENS
        
        # this works only in edit mode,
        #bm = bmesh.from_edit_mesh(obj.data)
        #bpy.ops.mesh.remove_doubles(threshold=0.01, use_unselected = True)
        # get the selected vertexes
        #SVs = [list(sv.co) for sv in bm.verts if sv.select]
        # get all vertexes and normals
        #all_centers_and_normals = np.array(list(map(lambda p: [p.center,p.normal], bm.faces)))
        #co_arrays.V = [vert.co.to_tuple() for face in ]
        #co_arrays.VN = [norm.normal for norm in bm.verts]
        
        all_centers_and_normals = []
        all_selected_centers = []
        
    elif bpy.context.active_object.mode == 'OBJECT':
        # if face mode:
        # get all vertexes and normals
        all_centers_and_normals = ci.Cache.get_centers_and_normals()
        all_selected_centers = array(list(map(lambda p: p.center, selected_polygon_pointers)))
    
    num_neigbors = int(bpy.context.scene.cs_overall_VG_.number_of_nearest_neighbors)
    local_patch_indexes = NearestNeighbors3D(all_centers_and_normals[:, 0],
                                             all_selected_centers,
                                             num_neigbors
                                             )
    
    return all_centers_and_normals, all_selected_centers, local_patch_indexes
