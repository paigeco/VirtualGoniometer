from csv import reader, QUOTE_MINIMAL
import datetime

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator

from ..AngleMeasurement.SeperateAngles import create_from_coordinates
from ..VolatileStorage import CacheInstance as ci

# Read from a csv
############################################
def read_some_data(context, filepath):

    print("running read_some_data...")
    
    with open(filepath, 'r', newline='') as data_file:
        
        csv_reader = reader(data_file, delimiter=',', quotechar='"', quoting=QUOTE_MINIMAL)
        
        data = [row for i, row in enumerate(csv_reader) if i]
        
        for row in data:
            center = tuple([float(r) for r in row[9:12]])
            p = create_from_coordinates(center, int(row[7]), int(row[3]))[0]
            p.created_since_epoch = datetime.datetime.strptime(row[1], '%c').now().timestamp()
            
            color = row[4].split("/")
            c1 = tuple([c/255 for c in ci.TranslateColor.get_tuple_from_color_name(color[0])]+[1])
            c2 = tuple([c/255 for c in ci.TranslateColor.get_tuple_from_color_name(color[1])]+[1])
            
            p.bsp.patch_A.default_color = c1[:-1]
            p.bsp.patch_B.default_color = c2[:-1]
            p.bsp.patch_A.material.diffuse_color = c1
            p.bsp.patch_B.material.diffuse_color = c2
            
            p.bsp.flavor_text = row[5]
            
        
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
