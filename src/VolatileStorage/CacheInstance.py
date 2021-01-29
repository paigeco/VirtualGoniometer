from .PolyCache import FaceCache

def construct_cache():
    global Cache # pylint: disable=global-variable-undefined
    Cache = FaceCache()
