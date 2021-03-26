from .PolyCache import FaceCache
from .ColorManager import ColorPairs

def construct_cache():
    global Cache # pylint: disable=global-variable-undefined
    Cache = FaceCache()
    global TranslateColor # pylint: disable=global-variable-undefined
    TranslateColor = ColorPairs()
