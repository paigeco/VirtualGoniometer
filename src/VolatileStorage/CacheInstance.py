from .PolyCache import FaceCache
def construct_mgm():
    global Cache # pylint: disable=global-variable-undefined
    Cache = FaceCache()
