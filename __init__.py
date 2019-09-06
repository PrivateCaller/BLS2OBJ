bl_info = {
    "name": "Blockland save (.bls) format",
    "author": "siba, adapted for 2.8 by Ahead",
    "blender": (2, 80, 0),
    "version": (0, 2, 1),
    "location": "File > Import",
    "description": "Import Blockland saves",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": 'COMMUNITY',
    "category": "Import-Export"}

if "bpy" in locals():
    import imp
    if "import_blb" in locals():
        imp.reload(import_bls)
else:
    import bpy

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from os.path import basename, dirname
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator, AddonPreferences


class BLSAddonPreferences(AddonPreferences):
    bl_idname = basename(dirname(__file__))

    filepath: StringProperty(
        name="Blockland Directory",
        subtype='FILE_PATH',
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "filepath")

class Import_bls_class(Operator, ImportHelper):
    """Load a Blockland save (.bls) file"""
    bl_idname = "import_mesh.bls"
    bl_label = "Import BLS"

    # ImportHelper mixin class uses this
    filename_ext = ".bls"

    filter_glob = StringProperty(
            default="*.bls",
            options={'HIDDEN'},
            )

    joinbricks = BoolProperty(
            name="Join Brick Meshes",
            description="Join every brick mesh one by one (possible performance improvement?)",
            default=True,
            )

    normalmap = BoolProperty(
            name="Use Normal Maps",
            description="For aesthetic purposes",
            default=False,
            )

    centerz = BoolProperty(
            name="Center Z",
            description="Center Z axis of loaded build",
            default=False,
            )

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        from . import import_bls
        import_bls.ImportBLS(addon_prefs.filepath, self.filepath, self.joinbricks, self.normalmap, self.centerz)
        return {'FINISHED'}

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(Import_bls_class.bl_idname, text="Blockland save (.bls)")

classes = (
    BLSAddonPreferences,
    Import_bls_class,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
