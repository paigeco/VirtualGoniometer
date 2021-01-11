import bpy
def move_cursor(scene, context, click_location,fi):
    scene.cursor.location = bpy.context.active_object.data.polygons[fi].center

def run_by_selection(scene, context, click_location, fi):
    mps = material_pair_manager.return_active_material_pairs()
    if not any([True for mpair in mps if mpair.check_index==fi]):    
        seperate_angles(selected_polygon_pointers = [bpy.context.active_object.data.polygons[ fi ]])
    else:
        print("SKIPPED DUE TO RERUNNING")