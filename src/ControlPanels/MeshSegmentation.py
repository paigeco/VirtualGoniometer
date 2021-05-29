"""[ Main Properties Panel ]
"""
from bpy.types import Panel
from ..MaterialManagers import ManagerInstance as mi

class MeshSegmentationControlPanel(Panel):
    """Creates the Mesh Segmentation Panel in the scene context of the properties editor"""
    bl_label = "Mesh Segmentation"
    bl_idname = "SCENE_PT_meshsegmentation"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    
    
    ANGLE_PRECISION = 1
    def draw(self, context):
        layout = self.layout
        
        if context.active_object is not None and context.active_object.type == 'MESH':
            
            cpi = context.active_object.cs_individual_VG_

            base = mi.Material_Group_Manager.return_active_object_entries('BaseColor')
            
            layout.label(text='Base Color Selector:')
            row = layout.row()
            
            
            if base is not None:
                row.prop(
                    cpi.base_region.material,
                    "diffuse_color",
                    text="Base Color"
                    )
            else:
                layout.label(text="Take a Measurement to Change Base Color", icon="ADD")
                #original_area = bpy.context.area.type
                #bpy.context.area.type = 'VIEW_3D'
                
                #override = overide_to_3d_view(context=context)
                #O.view3d.recreate_base_material(override) # pylint: disable=no-member

                #bpy.context.area.type = original_area
                        
            row = layout.row()
            row.scale_y = 3.0
            row.operator("object.segment_mesh")#, icon_value=cicons["measure"].icon_id)

        else:
            # Prompt the user to first add an object
            layout.label(text='Please select an object')
