"""[ contains the edit side operator ]"""

from bpy.props import StringProperty, IntVectorProperty, BoolVectorProperty

from bpy.types import Operator
from bpy import ops as O
import bmesh

from ..MaterialManagers import ManagerInstance

class EditSide(Operator):
    """[ allows the editing of one specific side of a mesh ]"""
    bl_idname = 'view3d.editside'
    bl_label = 'Edit Side'
    bl_description = 'Edit Side'
    bl_options = {'REGISTER', 'UNDO'}
    
    save_mode: StringProperty(default='OBJECT')
    options: IntVectorProperty(name='side edit options',
                               description='[ Side Integer (1 or 2), Material Pair Integer (i)]',
                               default=(0, 0),
                               size=2)
    select_type: BoolVectorProperty(default=(False, False, False), size=3)
    
    def execute(self, context):
        # Log the current mode so we can return to it
        cpi = context.active_object.cs_individual_VG_
        
        #Handle material pairs
        pairs = ManagerInstance.Material_Group_Manager.return_active_object_entries('Pairs')
        base = context.active_object.cs_individual_VG_.base_region
        active_pair = pairs[int(self.options[1])]
        
        m1, m2 = active_pair.refresh_material_indexes()
        
        base_index = base.local_material_index
        
        #Toggle the variables for the active sides   
        if self.options[0] == 1:
            mi = m1
            cpi.is_side_one_active = True
            cpi.depressed = (True, False)
        else:
            mi = m2
            cpi.is_side_one_active = False
            cpi.depressed = (False, True)
        

        #Save the patch changes
        if cpi.is_patch_editor_active:
            
            # Reset all the flags
            cpi.is_patch_editor_active = False
            cpi.depressed = (False, False)
            
            # Skips saving changes if the user switched out of Edit mode
            if context.active_object.mode != 'EDIT':
                return {'FINISHED'}
            
            # Create a new bmesh
            bm = bmesh.new() # pylint: disable=assignment-from-no-return
            bm = bmesh.from_edit_mesh(context.active_object.data) # pylint: disable=assignment-from-no-return
            
            
            count = 0
            # Edit said bmesh
            for face in bm.faces:
                if face.select:
                    face.material_index = mi
                    face.select = False
                    count += 1
                    
                elif face.material_index == mi:
                    face.material_index = base_index

            # Skip if none are selected
            if count <= 10:
                return {'FINISHED'}

            bmesh.update_edit_mesh(context.active_object.data)
            bm.free()
            
            context.tool_settings.mesh_select_mode = self.select_type
            # Return to the user's mode

            if context.active_object.mode != self.save_mode:
                O.object.mode_set(mode=self.save_mode)
            
            active_pair.get_angle()

        # Switch to edit mode to make patch changes
        else:
            # Save the mode before beginning the routine
            self.save_mode = str(context.active_object.mode)
            
            # Save the select type
            self.select_type = context.tool_settings.mesh_select_mode
            
            # Set to face settings
            context.tool_settings.mesh_select_mode = (False, False, True)
            
            # Switch to edit mode
            if self.save_mode != 'EDIT':
                O.object.mode_set(mode='EDIT')
            
            # Deselect any selected faces
            O.mesh.select_all(action='DESELECT')
            
            # Select the material patch
            context.active_object.active_material_index = mi
            O.object.material_slot_select()

            
            
            # SET for Embossing
            cpi.active_patch_index = int(self.options[1])
            cpi.is_patch_editor_active = True
            
        return {'FINISHED'}
