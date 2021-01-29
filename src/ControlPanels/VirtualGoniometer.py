"""[ Main Properties Panel ]
"""

import bpy
from bpy.types import Panel
from ..MaterialManagers import ManagerInstance as mi

class VirtualGoniometerControlPanel(Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Virtual Goniometer"
    bl_idname = "SCENE_PT_virtualgoniometer"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    ANGLE_PRECISION = 1
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        if bpy.context.active_object is not None:
            
            cpi = bpy.context.active_object.cs_individual_VG_
            
            base = mi.Material_Group_Manager.return_active_object_entries('BaseColor')
            pairs = mi.Material_Group_Manager.return_active_object_entries('Pairs')
            
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
                
            # Big render button
            layout.label(text="Perform Angle Measurement:")
            row = layout.row()
            row.scale_y = 3.0
            row.operator("view3d.run_optimal_select")#, icon_value=cicons["measure"].icon_id)
            

            # Different sizes in a row
            layout.label(text="Export Data to File:")
            row = layout.row(align=True)
            #layout.operator("export.some_data", icon_value=cicons["csv_out"].icon_id)
            
            # Clear Data
            layout.label(text="Edit Selection:")
            col = layout.column(align=True)
            #col.operator("object.show_selection_circle")
            #col.operator("object.simplify_mesh")
            col.operator("object.center_sample")
            #, icon_value=co_arrays.custom_icons["center"].icon_id)
            #col.operator("object.undo_last_point", icon_value=custom_icons["undo"].icon_id)
            col.operator("object.clear_selection")
            #, icon_value=co_arrays.custom_icons["reset"].icon_id)
            
            data_box = layout.box()
            data_box.label(text='Angle Data:')
            
            if bpy.context.active_object is not None:
                
                if len(pairs) == 0:
                    data_box.label(text="Selected Angles Will Be Shown Here", icon="ADD")
                    
                else:
                    
                    for i, pair in enumerate(pairs):
                        #print(patch)
                        side_colors = data_box.row(align=True)
                        side_colors.scale_x = 0.22
                        
                        side_colors.prop(pair.bsp.patchA.bsp.material, "diffuse_color", text="")
                        side_colors.prop(pair.bsp.patchB.bsp.material, "diffuse_color", text="")
                        
                        sub = side_colors.row(align=True)
                        
                        

                        sub.prop(pair.bsp, 'name', text="")
                        sub.label(text='( '+str(round(pair.theta, self.ANGLE_PRECISION))+'° )')
                        
                        edits = sub.row(align=True)
                        edits.scale_x = 0.45
                        
                        d = cpi.depressed
                        edits.operator("view3d.editside", text='1', depress=d[0]).options = (1, i)
                        edits.operator("view3d.editside", text='2', depress=d[1]).options = (2, i)
                        
                        delp = sub.row(align=True)
                        delp.scale_x = 0.4
                        delp.operator("object.deletepatch", text=" ", icon="CANCEL").patch_int = i
                        #delp.label(text=" ")
                     
            else:
                data_box.label(text='Please add an object')
            
            #row.operator("render.render")
        else:
            layout.label(text='Please select an object')
