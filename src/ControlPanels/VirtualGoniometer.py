"""[ Main Properties Panel ]
"""
from bpy.types import Panel
from ..MaterialManagers import ManagerInstance as mi

class VirtualGoniometerControlPanel(Panel):
    """Creates the main Virtual Goniometer Panel in the scene context of the properties editor"""
    bl_label = "Virtual Goniometer"
    bl_idname = "SCENE_PT_virtualgoniometer"
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
                
            # Big render button
            layout.label(text="Perform Angle Measurement:")
            row = layout.row()
            row.scale_y = 3.0
            row.operator("view3d.run_optimal_select")#, icon_value=cicons["measure"].icon_id)
            

            # Different sizes in a row
            layout.label(text="File Operations:")
            io_column = layout.column(align=True)
            io_column.operator("export.all_pairs")#, icon_value=cicons["csv_out"].icon_id)
            io_column.operator("import.all_pairs")
            
            # Clear Data
            layout.label(text="Edit Selection:")
            col = layout.column(align=True)
            #col.operator("object.simplify_mesh")
            col.operator("object.center_sample")
            #, icon_value=co_arrays.custom_icons["center"].icon_id)
            #col.operator("object.undo_last_point", icon_value=custom_icons["undo"].icon_id)
            col.operator("object.clear_selection")
            #, icon_value=co_arrays.custom_icons["reset"].icon_id)
            
            data_box = layout.box()
            data_box.label(text='Angle Data:')
            
            if context.active_object is not None:
                
                if len(cpi.material_pairs) == 0:
                    data_box.label(text="Selected Angles Will Be Shown Here", icon="ADD")
                    
                else:
                    for i, pair in enumerate(cpi.material_pairs):
                        
                        # Show pointer areas to the two object materials.
                        side_colors = data_box.row(align=True)
                        side_colors.scale_x = 0.22
                        
                        side_colors.prop(pair.patch_A.material, "diffuse_color", text="")
                        side_colors.prop(pair.patch_B.material, "diffuse_color", text="")
                        
                        # Setup the name fields
                        sub = side_colors.row(align=True)
                        #    Show the name
                        sub.label(text=str(pair.name))
                        #    Show the angle theta
                        sub.label(text='( '+str(round(pair.theta, self.ANGLE_PRECISION))+'° )') 
                        
                        # Setup the editing field
                        edits = sub.row(align=True)
                        edits.scale_x = 0.45
                        
                        #    Set whether the button should be depressed or not
                        dep = cpi.depressed if i == cpi.active_patch_index else (False, False)
                        
                        #    Set the depressions and show the edit side buttons
                        edits.operator("view3d.editside", text='1', depress=dep[0]).options = (1, i)
                        edits.operator("view3d.editside", text='2', depress=dep[1]).options = (2, i)
                        
                        # Setup and show the delete patch button
                        dbutto = sub.row(align=True)
                        dbutto.scale_x = 0.4
                        dbutto.operator("object.deletepatch", text=" ", icon="CANCEL").patch_int = i
                        #delp.label(text=" ")
                     
            else:
                # Prompt the user to first add an object
                data_box.label(text='Please add an object')
        else:
            # Prompt the user to first add an object
            layout.label(text='Please select an object')
