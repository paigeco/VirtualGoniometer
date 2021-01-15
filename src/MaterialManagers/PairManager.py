"""[ Pair Manager ]"""
import bpy
import mathutils
from ..CustomMath.CalculateAngle import get_angle
from ..CustomMath.RP1DClustering import ClusteringMeanRP1D
from ..VolatileStorage.ColorManager import ColorPairs
from .RegionManager import RegionManager
from . import ManagerInstance


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
        self.material_index_2 = 0
    
    def add_pair_to_blender_storage(self):
        # add a new item to the list
        self.bsp = bpy.context.active_object.material_pairs.add()  
        
    def load_from_backup(self, backup_pointer):
        self.bsp = backup_pointer
                
        self.material_1 = RegionManager(self.bsp.patchA)
        self.material_2 = RegionManager(self.bsp.patchA)

    def construct_new(self, c_polygon_pointer=None):
        #self.add_pair_to_blender_storage()
        if c_polygon_pointer is None:
            # give the coordinates of the center of the pair
            #self.check_index = 0
            pass
        else:
            # Pass in the center poly pointer
            #self.c_polygon_pointer = c_polygon_pointer
            #self.check_index = c_polygon_pointer.index
            self.bsp.center = list(c_polygon_pointer.center)

        #self.add_pair_to_blender_storage()

        self.bsp.name = "Patch (" + str(self.bsp.index+1) + ")"
        self.bsp.context_object = bpy.context.active_object
        
        self.create_new_material_pair()

    def create_new_material_pair(self):
        # set the color objects from the pair list
        o_color1, o_color2 = self.generate_color_objects()
        
        self.bsp.patchA.default_color = list(o_color1)
        self.bsp.patchB.default_color = list(o_color2)
        
        self.bsp.patchA.name = str(self.bsp.name + " Face (1)")
        self.bsp.patchB.name = str(self.bsp.name + " Face (2)")
        # create the materials
        self.material_1 = RegionManager(self.bsp.patchA)
        self.material_2 = RegionManager(self.bsp.patchB)
        
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
        self.material_1.update_faces_with_material()
        self.material_2.update_faces_with_material()

    def get_angle(self):
        # refresh the face data
        self.get_current_face_data()
        
        # get the Normals and Centroids
        self.material_1.get_face_mathematical_components()
        self.material_2.get_face_mathematical_components()
        
        # get the angle
        self.bsp.theta, self.patch_normal_1, self.patch_normal_2 = get_angle(
            self.material_1.centers, self.material_2.centers,
            self.material_1.normals, self.material_2.normals)
    
    def apply_to_face_pair_by_indexes(self, F1, F2):
        self.material_1.apply_to_faces_by_face_index(F1)
        self.material_2.apply_to_faces_by_face_index(F2)

    def apply_pair_within_region(self, CNs, J):
        #Virtual goniometer
        #   P = nx3 numpy array of vertices of points in patch
        #   N = nx3 array of vertex normals
        #   Can also use N as face normals, and P as face centroids
        #   T = Number of random projections to use (default T=100)
        P = CNs[J,0] #mx3 array of x,y,z coordinates for all m vertices in patch
        N = CNs[J,1]  #mx3 array of x,y,z coordinates of unit outward normal vectors to vertices in patch
        T = int(self.bso.number_of_random_projections)
        #Output:f
        #   C = Clusters (C==1 and C==2 are the two detected clusters)
        C,self.n1, self.n2, self.bsp.theta = ClusteringMeanRP1D(P,N,T)
        #P1 = P[C==1,:]     #P2 = P[C==2,:]
        J1 = J[C==1]
        J2 = J[C==2]
        
        self.apply_to_face_pair_by_indexes(J1,J2)

        print(self.bsp.name + " has a theta of " +str(self.bsp.theta))

    
    def destroy(self):
        co = bpy.context.active_object
        i = self.bsp.index
        
        self.material_1.destroy()
        self.material_2.destroy()
        
        co.material_pairs.remove(i)
        ManagerInstance.Material_Group_Manager.destroy_by_index(i, 'Pairs', destroy=False)

