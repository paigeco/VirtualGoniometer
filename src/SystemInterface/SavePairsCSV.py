from csv import writer, QUOTE_MINIMAL

from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty


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
def write_some_data(context, filepath, data_input):
    print("running write_some_data...")
    with open(filepath, 'w', newline='') as data_file:
        data_writer = writer(data_file, delimiter=',', quotechar='"', quoting=QUOTE_MINIMAL)
        data_writer.writerow(COLUMNS)
        
        if not data_input is None:
            for row in data_input:
                if float(row['hue'])>0.5:
                    hue2 = float(row['hue'])-0.5
                else:
                    hue2 = float(row['hue'])+0.5
                data_writer.writerow([
                    "Angle "+str(row['k']+1),
                    row['theta'],
                    row['hue'],
                    str(hue2),
                    'NA'])

    return {'FINISHED'}

class ExportSomeData(Operator, ExportHelper):
    """Exports virtual goniometer data as a CSV"""
    bl_idname = "export.some_data"  # important since its how bpy.ops.import_test.some_data
    bl_label = "Export to CSV"

    # ExportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        return write_some_data(context, self.filepath, )
