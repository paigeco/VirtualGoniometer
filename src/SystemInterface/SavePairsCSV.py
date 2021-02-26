from csv import writer, QUOTE_MINIMAL
import datetime

from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

from ..VolatileStorage.ColorManager import ColorPairs
from ..MaterialManagers import ManagerInstance



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
def write_some_data(context, filepath, use_some_setting):
    cp = ColorPairs()
    
    print("running write_some_data...")
    
    pairs = ManagerInstance.Material_Group_Manager.return_active_object_entries('Pairs')
    
    with open(filepath, 'w', newline='') as data_file:
        data_writer = writer(data_file, delimiter=',', quotechar='"', quoting=QUOTE_MINIMAL)
        data_writer.writerow(COLUMNS)
        for pair in pairs:
            data_writer.writerow([
                str(pair.bsp.context_object.name), # Mesh Name
                datetime.datetime.now().strftime('%c'), #TODOO fix this bodge
                str(pair.bsp.measurement_index),
                str(pair.bsp.break_index),
                "{}/{}".format(
                    cp.get_color_name_from_tuple(tuple(pair.bsp.patch_A.default_color)),
                    cp.get_color_name_from_tuple(tuple(pair.bsp.patch_B.default_color))),
                str(pair.bsp.flavor_text), # User Data
                str(pair.bsp.theta), # Angle
                str(pair.bsp.number_of_points), # Number of Verticies
                str(pair.bsp.radius), # Radius
                str(pair.bsp.center[0]), # x
                str(pair.bsp.center[1]), # y
                str(pair.bsp.center[2]), # z
                str("fill"),
                str(2)
            ])

    return {'FINISHED'}

class ExportSomeData(Operator, ExportHelper):
    """Exports virtual goniometer data as a CSV"""
    bl_idname = "export.all_pairs"  # important since its how bpy.ops.import_test.some_data
    bl_label = "Export to CSV"

    # ExportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    
    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        return write_some_data(context, self.filepath, self.use_setting) # pylint: disable=no-member
