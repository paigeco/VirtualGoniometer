import bpy
from ..MaterialManagers import ManagerInstance as mi
from .ReturnPolys import get_data_from_selected_object

def create_from_coordinates(center, radius, break_index):
    index = bpy.context.active_object.closest_point_on_mesh(center)[-1]
    return seperate_angles([bpy.context.active_object.data.polygons[index]], [radius], break_index)


def seperate_angles(selected_polygon_pointers, radii=None, break_index=None):
    """
    NOTE: Until I fix this only fire in single file as anything else will crash EVERYTHING
    
    [ This is a core piece of this project, and it is completely broken and I have no clue
    how to fix this without writing my own nearest neighbors algorithm which allows accepting an
    array of different radii, which I've tried to do but it was so SLOW it didn't even make sense.
    anyways, if anyone has any suggestions I'm all ears ]

    Parameters
    ----------
    selected_polygon_pointers : [type]
        [description]
    radii : [list], optional
        [description], by default None
    break_index : [type], optional
        [description], by default None

    Returns
    -------
    [list] [returns a list of the created pairs]
    """
    
    # The mythical bodge of a lifetime TODO fix this garbage please
    
    # Active object
    ao = bpy.context.active_object
    
    # Program Settings
    settings = bpy.context.scene.cs_overall_VG_
    
    # Set the radius 
    radii = [int(settings.number_of_nearest_neighbors)
            ]*len(selected_polygon_pointers) if radii is None else radii
    
    # Set the break index
    bi = break_index if break_index is not None else ao.cs_individual_VG_.breaks
    
    if selected_polygon_pointers is None:
        selected_polygon_pointers = [p for p in ao.data.polygons if p.select]
    
    CNs, SVs, LPIs, Ds = get_data_from_selected_object(selected_polygon_pointers, radii[0])
    
    #nCNs = CNs.shape[1] # Number of points in mesh
    nLPIs = LPIs.shape[1] # Number of points in area
    
    pair_list = []
    
    # k is which of the selected faces we are on
    for k in range(len(SVs)):
        
        # Retrive indices of nearest neighbor vertices
        J = LPIs[k] # Indices of verices in neighborhood patch
        p = mi.Material_Group_Manager.add_pair_to_active(cp=selected_polygon_pointers[k])
        p.set_name(bi)
        p.apply_pair_within_region(CNs, J)
        p.bsp.radius = Ds.tolist()[0][-1]
        p.bsp.number_of_points = nLPIs
        pair_list.append(p)

    return pair_list
