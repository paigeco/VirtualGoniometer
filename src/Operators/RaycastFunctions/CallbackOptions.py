import bpy
from src.MaterialManagers import ManagerInstance as mi
from src.CustomMath.SeperateAngles import seperate_angles

def move_cursor(scene, context, click_location,fi):
    scene.cursor.location = bpy.context.active_object.data.polygons[fi].center

def run_by_selection(scene, context, click_location, fi):
    mps = mi.Material_Group_Manager.return_active_object_entries('Pairs')
    if not any([True for mpair in mps if mpair.check_index == fi]):    
        seperate_angles(selected_polygon_pointers=[bpy.context.active_object.data.polygons[fi]])
    else:
        print("SKIPPED DUE TO RERUNNING")
