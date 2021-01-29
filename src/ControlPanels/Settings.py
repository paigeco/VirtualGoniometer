#import bpy
from bpy.types import Panel


class SettingsPanel(Panel):
    """Creates a Panel in the scene context of the properties editor
    which is used to control the settings of the VirtualGoniometer and
    mesh segmenter"""
    bl_info = "Controls the settings for the AMAAZE Plugin"
    bl_label = "Settings Panel"
    bl_idname = "SCENE_PT_settings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        layout.label(text='Virtual Goniometer Settings:')
        
        vg_settings = layout.box()
        # Create an alligned column
        vg_settings.label(text=" Projection Controls:")
        #col = layout.row(align=True)
        
        nonn_text = 'Points to include in auto-generated region'
        
        vg_settings.prop(scene.cs_overall_VG_, 'number_of_nearest_neighbors', text=nonn_text)
        vg_settings.prop(scene.cs_overall_VG_, 'number_of_random_projections')
