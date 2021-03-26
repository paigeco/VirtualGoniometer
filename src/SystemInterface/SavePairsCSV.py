from csv import writer, QUOTE_MINIMAL
import datetime

from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from bpy.types import Operator



COLUMNS = [
    'Mesh Name',
    'Date',
    'Measurement #',
    'Break #',
    'Colors',
    'User Data',
    'Angle',
    'Number of Vertices',
    'Radius',
    'x',
    'y',
    'z',
    'fit',
    'SegParam'
]

# Write to a CSV
############################################
def write_some_data(context, filepath):

    print("running write_some_data...")
    
    pairs = context.active_object.cs_individual_VG_.material_pairs
    
    with open(filepath, 'w', newline='') as data_file:
        
        data_writer = writer(data_file, delimiter=',', quotechar='"', quoting=QUOTE_MINIMAL)
        data_writer.writerow(COLUMNS)
        for pair in pairs:
            data_writer.writerow([
                str(pair.context_object.name), # Mesh Name
                datetime.datetime.fromtimestamp(pair.created_since_epoch).strftime('%c'),
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
            ])

    return {'FINISHED'}

class ExportSomeData(Operator, ExportHelper):
    """Exports virtual goniometer data as a CSV"""
    bl_idname = "export.all_pairs"  # important since its how bpy.ops.import_test.some_data
    bl_label = "Export Measurements to CSV"

    # ExportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        return write_some_data(context, self.filepath) # pylint: disable=no-member
