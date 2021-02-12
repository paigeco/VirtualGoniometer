"""[ Pair Manager ]"""
import bpy
import mathutils
from ..CustomMath.CalculateAngle import get_angle
from ..CustomMath.RP1DClustering import ClusteringMeanRP1D
from ..VolatileStorage.ColorManager import ColorPairs
from .RegionManager import RegionManager


class PairManager(object):
    def __init__(self, backup_pointer):
        self.context = bpy.context
        self.bso = bpy.context.scene.cs_overall_VG_
        self.bsa = bpy.context.active_object.cs_individual_VG_
        self.bsp = backup_pointer
        self.material_1 = None
        self.material_2 = None
        self.n1, self.n2, self.patch_normal_1, self.patch_normal_2 = None, None, None, None
        self.material_index_1 = 0
        self.check_index = 0
        self.material_index_2 = 0
        
    def load_from_backup(self, backup_pointer):
        self.bsp = backup_pointer
                
        self.material_1 = RegionManager(self.bsp.patch_A)
        self.material_2 = RegionManager(self.bsp.patch_B)

    def construct_new(self, c_polygon_pointer=None):
        #self.add_pair_to_blender_storage()
        if c_polygon_pointer is None:
            # give the coordinates of the center of the pair
            self.check_index = 0
        else:
            # Pass in the center poly pointer
            #self.c_polygon_pointer = c_polygon_pointer
            self.check_index = c_polygon_pointer.index
            self.bsp.center = list(c_polygon_pointer.center)

        #self.add_pair_to_blender_storage()
        self.bsp.context_object = bpy.context.active_object
        
        self.create_new_material_pair()
    
    def set_name(self, break_index):
        self.bsp.break_index = break_index

    def create_new_material_pair(self):
        # set the color objects from the pair list
        o_color1, o_color2 = self.generate_color_objects()
        
        self.bsp.context_object = self.context.active_object
        
        self.bsp.patch_A.context_object = self.context.active_object
        self.bsp.patch_B.context_object = self.context.active_object
        
        self.bsp.patch_A.default_color = list(o_color1)
        self.bsp.patch_B.default_color = list(o_color2)
        
        self.bsp.patch_A.name = str(self.bsp.name + " Face (1)")
        self.bsp.patch_B.name = str(self.bsp.name + " Face (2)")
        # create the materials
        self.material_1 = RegionManager(self.bsp.patch_A)
        self.material_2 = RegionManager(self.bsp.patch_B)
        
        
        self.bsp.side_1_material = self.material_1.bsp.material
        self.bsp.side_2_material = self.material_2.bsp.material
    
    def generate_color_objects(self):
        #TODOO: FIX THIS SO IT NO LONGER REQUIRES ACTIVE CONTEXT

        # Create color 1 & color 2
        cp = ColorPairs()
        col1 = mathutils.Color(cp.return_active_pairs()[self.bsa.cp_index][0])
        col2 = mathutils.Color(cp.return_active_pairs()[self.bsa.cp_index][1])
        # Increment the counter
        self.bsa.cp_index += 1
        return col1, col2

    def refresh_material_indexes(self):
        # refresh material indexes.
        self.material_index_1 = self.material_1.get_material_index()
        self.material_index_2 = self.material_2.get_material_index()
        return self.material_index_1, self.material_index_2
    
    def get_current_face_data(self):
        # get the Faces
        faces1 = self.material_1.update_faces_with_material()
        faces2 = self.material_2.update_faces_with_material()
        return faces1, faces2
    
    def get_angle(self):
        # get the Normals and Centroids
        center1, normal1 = self.material_1.get_face_mathematical_components()
        center2, normal2 = self.material_2.get_face_mathematical_components()
        
        # get the angle
        self.bsp.theta, self.patch_normal_1, self.patch_normal_2 = get_angle(
            center1, center2,
            normal1, normal2)
    
    def apply_to_face_pair_by_indexes(self, F1, F2):
        self.material_1.apply_to_faces_by_face_index(F1)
        self.material_2.apply_to_faces_by_face_index(F2)

    def apply_pair_within_region(self, CNs, J):
        #Virtual goniometer
        #   P = nx3 numpy array of vertices of points in patch
        #   N = nx3 array of vertex normals
        #   Can also use N as face normals, and P as face centroids
        #   T = Number of random projections to use (default T=100)
        P = CNs[0, J] #mx3 array of x,y,z coordinates for all m vertices in patch
        N = CNs[1, J] #mx3 array of x,y,z coordinates of
        # unit outward normal vectors to vertices in patch
        T = int(self.bso.number_of_random_projections)
        #Output:f
        #   C = Clusters (C==1 and C==2 are the two detected clusters)
        C, self.n1, self.n2, self.bsp.theta = ClusteringMeanRP1D(P, N, T)
        #P1 = P[C==1,:]     #P2 = P[C==2,:]
        J1 = J[C == 1]
        J2 = J[C == 2]
        
        self.apply_to_face_pair_by_indexes(J1, J2)
        

        print(self.bsp.name + " has a theta of " +str(self.bsp.theta))

    
    def destroy(self):
        
        self.material_1.destroy()
        self.material_2.destroy()
        self.bsa.material_pairs.remove(self.bsp.index)
