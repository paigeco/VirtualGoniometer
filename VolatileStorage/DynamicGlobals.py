"""[ Sets up the common dynamically sto]
"""

from VolatileStorage.ColorManager import ColorPairs
from VolatileStorage.PolyCache import FaceCache
from MaterialManagers.ObjectManager import MaterialGroupManager



def init_dynamic_globals():

    CLASS_LIST = [
        MaterialPairProperties, PerformOptimalSelect, ClearSelection, CenterSample,
        ControlSettingsObject_VG_, ControlSettingsTotal_VG_, PerformRaycastSelect,
        PerformFaceSelect, VirtualGoniometerControlPanel, DeletePatch, EditSide
    ]
    poly_cache = FaceCache()
    color_manager = ColorPairs()
    object_region_manager = MaterialGroupManager()
