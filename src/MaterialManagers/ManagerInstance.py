from .ObjectManager import MaterialGroupManager as mgm

def construct_mgm():
    global Material_Group_Manager # pylint: disable=global-variable-undefined
    Material_Group_Manager = mgm()
