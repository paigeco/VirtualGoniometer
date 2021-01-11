import bpy

class VirtualGoniometerControlPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Virtual Goniometer"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        if bpy.context.active_object != None:
            self.ANGLE_PRECISION = 1
            cpi = bpy.context.active_object.cs_individual_VG_

            # Create an alligned column
            layout.label(text=" Projection Controls:")
            col = layout.row(align=True)
            col.prop(scene.cs_overall_VG_,'number_of_nearest_neighbors', text = 'Points to include in auto-generated region')
            col.prop(scene.cs_overall_VG_, 'number_of_random_projections')
            row = layout.row()
            
            
            if bpy.context.active_object.cs_individual_VG_.base_material is None:
                base_material.attempt_recovery()
            
            row.prop(bpy.context.active_object.cs_individual_VG_.base_material,
                "diffuse_color",text="Base_Color")
                
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
            col.operator("object.center_sample")#, icon_value=co_arrays.custom_icons["center"].icon_id)
            #col.operator("object.undo_last_point", icon_value=co_arrays.custom_icons["undo"].icon_id)
            col.operator("object.clear_selection")#, icon_value=co_arrays.custom_icons["reset"].icon_id)
            
            data_box = layout.box()
            data_box.label(text='Angle Data:')
            
            if not(bpy.context.active_object is None):
                
                if len(active_pairs)==0:
                    data_box.label(text="Selected Angles will show here.",icon="ADD")
                else:
                    for i, pair in enumerate(active_pairs):
                        #print(patch)
                        side_colors = data_box.row(align=True)
                        side_colors.scale_x = 0.22
                        
                        side_colors.prop(pair.material_1.material, "diffuse_color",text="")
                        side_colors.prop(pair.material_2.material, "diffuse_color",text="")
                        
                        sub = side_colors.row(align=True)
                        
                        

                        sub.prop(pair.bsp,'name',text = "")
                        sub.label(text= '( '+str(round(pair.theta, self.ANGLE_PRECISION))+'° )')
                        
                        edits = sub.row(align=True)
                        edits.scale_x = 0.45
                        
                        edits.operator("view3d.editside",text = '1',depress=cpi.depressed[0]).options = (1,i)
                        edits.operator("view3d.editside",text = '2',depress=cpi.depressed[1]).options = (2,i)
                        
                        delp = sub.row(align=True)
                        delp.scale_x = 0.4
                        delp.operator("object.deletepatch",text=" ",icon="CANCEL").patch_int = i
                        #delp.label(text=" ")
                     
            else:
                data_box.label(text='Please add an object')
            
            #row.operator("render.render")
        else:
            layout.label(text='Please select an object')
