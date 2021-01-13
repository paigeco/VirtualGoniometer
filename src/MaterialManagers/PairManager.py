"""[ Pair Manager ]"""
import bpy
import mathutils
from ..CustomMath.CalculateAngle import get_angle
from ..CustomMath.RP1DClustering import ClusteringMeanRP1D
from ..VolatileStorage.ColorManager import ColorPairs

from .RegionManager import MaterialManager


class PairManager(object):
    def __init__(self):
        self.context = bpy.context
        self.bso = bpy.context.scene.cs_overall_VG_
        self.bsa = bpy.context.active_object.cs_individual_VG_
        self.bsp = None
        self.material_1, self.material_2 = None, None
    
    def add_pair_to_blender_storage(self):
        # add a new item to the list
        self.bsp = bpy.context.active_object.material_pairs.add()  
        
    def load_from_backup(self, backup_pointer):
        self.bsp = backup_pointer
                
        self.material_1 = MaterialManager(material = self.bsp.side_1_material)
        self.material_2 = MaterialManager(material = self.bsp.side_2_material)

    def construct_new(self, c_polygon_pointer=None):
        self.add_pair_to_blender_storage()
        if c_polygon_pointer is None:
            # give the coordinates of the center of the pair
            #self.check_index = 0
            pass
        else:
            # Pass in the center poly pointer
            self.c_polygon_pointer = c_polygon_pointer
            #self.check_index = c_polygon_pointer.index
            self.bsp.center = list(c_polygon_pointer.center)

        self.add_pair_to_blender_storage()

        self.bsp.name = "Patch (" + str(self.bsp.index+1) + ")"
        self.bsp.context_object = bpy.context.active_object
        
        self.create_new_material_pair()
        self.add_to_m_list()

    def create_new_material_pair(self):
        # set the color objects from the pair list
        self.bsp.o_color_1, self.bsp.o_color_2 = self.generate_color_objects()
        
        # create the materials
        self.material_1 = MaterialManager(name=str(self.bsp.name + " Face (1)"), color=mathutils.Color(list(self.bsp.o_color_1)))
        self.material_2 = MaterialManager(name=str(self.bsp.name + " Face (2)"), color=mathutils.Color(list(self.bsp.o_color_2)))
        
        self.bsp.side_1_material = self.material_1.material
        self.bsp.side_2_material = self.material_2.material
    
    def generate_color_objects(self):
        #TODO: FIX THIS SO IT NO LONGER REQUIRES ACTIVE CONTEXT

        # Create color 1 & color 2
        col1 = mathutils.Color(ColorPairs.return_active_pairs()[self.bsa.cp_index][0])
        col2 = mathutils.Color(ColorPairs.return_active_pairs()[self.bsa.cp_index][1])
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
            self.material_1.normals, self.material_2.normals )
    
    def apply_to_face_pair_by_indexes(self,F1,F2):
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
        C,self.n1,self.n2, self.bsp.theta = ClusteringMeanRP1D(P,N,T)
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
        material_pair_manager.destroy_by_index(i, destroy = False)
        
    def add_to_m_list(self):
        material_pair_manager.add_material_pair_to_object(bpy.context.active_object, self)
