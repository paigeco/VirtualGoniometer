import bpy
from ..MaterialManagers import ManagerInstance as mi
from .ReturnPolys import get_data_from_selected_object

def seperate_angles(selected_polygon_pointers=None, center=(0, 0, 0), break_index=None):
    #
    ao = bpy.context.active_object
    #
    bi = break_index if break_index is not None else ao.cs_individual_VG_.breaks
    
    if selected_polygon_pointers is None:
        selected_polygon_pointers = [p for p in ao.data.polygons if p.select]
    
    
    CNs, SVs, LPIs, Ds = get_data_from_selected_object(selected_polygon_pointers)
    
    nCNs = CNs.shape[1] # Number of points in mesh
    nLPIs = LPIs.shape[1] # Number of points in area
    
    # k is which of the selected faces we are on
    for k in range(len(SVs)):
        
        # Retrive indices of nearest neighbor vertices
        J = LPIs[k] # Indices of verices in neighborhood patch
        p = mi.Material_Group_Manager.add_pair_to_active(cp=selected_polygon_pointers[k])
        p.set_name(bi)
        p.apply_pair_within_region(CNs, J)
        p.bsp.radius = Ds.tolist()[0][-1]
        p.bsp.number_of_points = nLPIs
