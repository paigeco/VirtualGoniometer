from csv import reader, QUOTE_MINIMAL
import datetime

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator

from ..CustomMath.SeperateAngles import create_from_coordinates

# Read from a csv
############################################
def read_some_data(context, filepath):

    print("running read_some_data...")
    
    with open(filepath, 'r', newline='') as data_file:
        
        csv_reader = reader(data_file, delimiter=',', quotechar='"', quoting=QUOTE_MINIMAL)
        
        data = [row for i, row in enumerate(csv_reader) if i]
        print(data)
        
        for row in data:
            #print((row[9:12]), row[7], row[3])
            create_from_coordinates(tuple([float(r) for r in row[9:12]]), int(row[7]), int(row[3]))
        #center_faces = 
        
        #seperate_angles(selected_polygon_pointers=[context.active_object.data.polygons[1]],
        #    break_index=1)
        """[
            str(pair.context_object.name), # Mesh Name
            datetime.datetime.fromtimestamp(pair.created_since_epoch).strftime('%c')[:-5],
            str(pair.measurement_index),
            str(pair.break_index),
            "{}/{}".format(pair.patch_A.color_name, pair.patch_B.color_name),
            str(pair.flavor_text), # User Data
            str(pair.theta), # Angle
            str(pair.number_of_points), # Number of Verticies
            str(pair.radius), # Radius
            str(pair.center[0]), # x
            str(pair.center[1]), # y
            str(pair.center[2]), # z
            str("fill"),
            str(2)
        ]"""

    return {'FINISHED'}


class ImportSomeData(Operator, ImportHelper):
    """Imports virtual goniometer measurements from a file"""
    bl_idname = "import.all_pairs"
    bl_label = "Import Measurements from CSV"

    # ImportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        return read_some_data(context, self.filepath) # pylint: disable=no-member
