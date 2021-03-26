from ..MaterialManagers import ManagerInstance as mi
from ..CustomMath.SeperateAngles import seperate_angles

def move_cursor(scene, context, click_location, fi, bn=None): # pylint: disable=unused-argument
    #print(context, click_location, bn)
    scene.cursor.location = context.active_object.data.polygons[fi].center

def run_by_selection(scene, context, click_location, fi, bn=None): # pylint: disable=unused-argument
    mps = mi.Material_Group_Manager.return_active_object_entries('Pairs')
    if not any([True for mpair in mps if mpair.check_index == fi]):    
        seperate_angles([context.active_object.data.polygons[fi]],
                        break_index=bn)
    else:
        print("SKIPPED DUE TO RERUNNING")
