import bpy
from math import degrees

bl_info = {
    "name": "Export Transform To Csv",
    "author": "Ludvig Ström",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "File > Export > Export Transform (.csv)",
    "warning": "",
    "description": "Exports the transform for each frame in the active timeline of a selected object",
    "category": "Import-Export",
    "wiki_url": ""
}


def write_some_data(context, filepath):
    print("Exporting CSV animation...")
    
    # get the current selection
    selection = context.selected_objects
    scene = context.scene
    startFrame = scene.frame_start
    endFrame = scene.frame_end
    currentFrame = scene.frame_current
    
    f = open(filepath, 'w', encoding='utf-8')

    for sel in selection:
        for i in range(endFrame-startFrame+1):
            frame = i + startFrame
            scene.frame_set(frame)
            rot = sel.rotation_euler
            f.write("%f, %f, %f, %f, %f, %f;\n" % ( sel.location[0], sel.location[1], sel.location[2], degrees(rot.x), degrees(rot.y), degrees(rot.z)))
    
    f.close()
    scene.frame_set(currentFrame)

    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportTransformToCsv(Operator, ExportHelper):
    bl_idname = "export.transform_to_csv"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Selected Animation (.csv)"

    # ExportHelper mixin class uses this
    filename_ext = ".csv"

    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        return write_some_data(context, self.filepath)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportTransformToCsv.bl_idname, text="Selected Animation (.csv)")


def register():
    bpy.utils.register_class(ExportTransformToCsv)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportTransformToCsv)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.export.transform_to_csv('INVOKE_DEFAULT')