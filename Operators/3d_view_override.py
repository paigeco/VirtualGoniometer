import bpy

def find_3d_view_override(context):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {'window': window, 'screen': screen, 'area': area, 'region':region}
                        return override