"""[ contains the edit side operator ]"""

from bpy.props import StringProperty, IntVectorProperty
from bpy.types import Operator
from bpy import context as C
from bpy.ops.object import material_slot_select, mode_set, material_slot_assign
from bpy.ops.mesh import select_all
import bmesh

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
    def execute(self, context):
        # Log the current mode so we can return to it
        cpi = C.active_object.cs_individual_VG_
        
        #Handle material pairs
        pairs = material_pair_manager.return_active_material_pairs()
        active_pair = pairs[int(self.options[1])]
        
        m1, m2 = active_pair.refresh_material_indexes()
        
        baseindex = base_material.active_base_material().get_material_index()
                    
        if self.options[0] == 1:
            mi = m1
            cpi.is_side_one_active = True
            cpi.depressed = (True, False)
        else:
            mi = m2
            cpi.is_side_one_active = False
            cpi.depressed = (False, True)
        

        if cpi.is_patch_editor_active:
            cpi.is_patch_editor_active = False
            cpi.depressed = (False, False)
            if self.save_mode != 'OBJECT':

                if self.save_mode != 'EDIT':
                    mode_set(mode='EDIT')
                
                v_temp = []
                
                bm = bmesh.new() # pylint: disable=assignment-from-no-return
                bm.from_mesh(C.active_object.data)
                for v in bm.faces:
                    if v.select:
                        v_temp.append(v)
                
                bmesh.update_edit_mesh(C.active_object.data)
                
                C.active_object.active_material_index = baseindex
                material_slot_select()
                
                C.active_object.active_material_index = mi
                material_slot_select()
                
                C.active_object.active_material_index = baseindex
                material_slot_assign()
                
                select_all(action='DESELECT')
                
                for v in v_temp:
                    v.select = True
                    print(v.normal)
                bmesh.update_edit_mesh(C.active_object.data)
                
                C.active_object.active_material_index = mi
                material_slot_assign()
                
                #active_pair.get_angle()
                
                
                #bpy.ops.mesh.select_all(action = 'DESELECT')
            elif self.save_mode == 'OBJECT':
                select_all(action='DESELECT')
                #APPLY PATCH CHANGES
                # Set to object mode
                mode_set(mode='OBJECT')
                
                for po in C.active_object.data.polygons:
                    if po.select:
                        po.material_index = mi
                        #po.select = False
                
               # active_pair.get_angle()
            # Return to the user's mode
            if C.active_object.mode != self.save_mode:
                mode_set(mode=self.save_mode)

        else:
            self.save_mode = str(C.active_object.mode)
            # HIGHLIGHT_PATCH
            if self.save_mode != 'EDIT':
                mode_set(mode='EDIT')
            
            select_all(action='DESELECT')
            C.active_object.active_material_index = mi
            material_slot_select()

            # SET for Embossing
            cpi.active_patch_index = int(self.options[1])
            cpi.is_patch_editor_active = True
        return {'FINISHED'}
