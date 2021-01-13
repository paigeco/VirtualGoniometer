"""[ generates context overrides ]"""
from bpy import context as C

def overide_to_3d_view(context=None) -> 'dict':
    """[summary]

    Args:
        context ([type], optional): [description]. Defaults to None.

    Returns:
        [dict]: [returns the override dict for the main 3d view]
    """
    if context is None:
        context = C
    
    for window in context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {'window': window,
                                    'screen': screen,
                                    'area': area,
                                    'region':region
                                    }
                        return override
    return {}
