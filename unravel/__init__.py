import bpy
import os


ASSET_FILE = os.path.join(os.path.dirname(__file__), "assets", "unravel_nodes.blend")
GROUP_NAMES = ("Unravel Tears", "Unravel Threads", "Unravel Strand")


STRAY_VALUES = {
    "Density": 40.0,
    "Length": 0.07,
    "Length Random": 0.5,
    "Root Width": 0.001,
    "Tip Width": 0.0003,
    "Resolution": 16,
    "Clumping": 0.0,
    "Curl Radius": 0.002,
    "Curl Turns": 1.5,
    "Frizz": 0.6,
    "Droop": 0.6,
    "Seed": 1,
}


def load_node_groups():
    missing = [name for name in GROUP_NAMES if name not in bpy.data.node_groups]
    if not missing:
        return
    with bpy.data.libraries.load(ASSET_FILE, link=False) as (data_from, data_to):
        data_to.node_groups = [name for name in data_from.node_groups if name in missing]


def set_input(modifier, name, value):
    for item in modifier.node_group.interface.items_tree:
        if item.item_type == 'SOCKET' and item.in_out == 'INPUT' and item.name == name:
            getattr(modifier.properties.inputs, item.identifier).value = value
            return


class UNRAVEL_OT_make(bpy.types.Operator):
    bl_idname = "unravel.make"
    bl_label = "Make Unravel"
    bl_description = "Set up tears and threads on the selected cloth"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH'

    def execute(self, context):
        cloth = context.active_object
        if "Unravel Tears" in cloth.modifiers:
            self.report({'INFO'}, cloth.name + " already uses Unravel")
            return {'CANCELLED'}

        load_node_groups()

        if "Tears" not in cloth.vertex_groups:
            cloth.vertex_groups.new(name="Tears")

        tears = cloth.modifiers.new("Unravel Tears", 'NODES')
        tears.node_group = bpy.data.node_groups["Unravel Tears"]

        name = cloth.name + " Threads"
        threads = bpy.data.objects.new(name, bpy.data.hair_curves.new(name))
        for collection in cloth.users_collection:
            collection.objects.link(threads)
        threads.parent = cloth

        uv_name = cloth.data.uv_layers.active.name if cloth.data.uv_layers.active else "UVMap"

        fray = threads.modifiers.new("Unravel Fray", 'NODES')
        fray.node_group = bpy.data.node_groups["Unravel Threads"]
        set_input(fray, "Cloth", cloth)
        set_input(fray, "UV Map", uv_name)

        strays = threads.modifiers.new("Unravel Strays", 'NODES')
        strays.node_group = bpy.data.node_groups["Unravel Threads"]
        set_input(strays, "Cloth", cloth)
        set_input(strays, "UV Map", uv_name)
        for input_name, value in STRAY_VALUES.items():
            set_input(strays, input_name, value)

        self.report({'INFO'}, "Unravel is ready. Paint the Tears vertex group to cut holes")
        return {'FINISHED'}


class UNRAVEL_PT_main(bpy.types.Panel):
    bl_label = "Unravel"
    bl_idname = "UNRAVEL_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unravel"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        if obj is None:
            layout.label(text="Select a cloth object", icon='INFO')
        else:
            layout.label(text=obj.name, icon='OBJECT_DATA')


class UNRAVEL_PT_tears(bpy.types.Panel):
    bl_label = "Tears"
    bl_idname = "UNRAVEL_PT_tears"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unravel"
    bl_parent_id = "UNRAVEL_PT_main"

    def draw(self, context):
        self.layout.operator(UNRAVEL_OT_make.bl_idname, icon='MOD_CLOTH')


class UNRAVEL_PT_strands(bpy.types.Panel):
    bl_label = "Strands"
    bl_idname = "UNRAVEL_PT_strands"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unravel"
    bl_parent_id = "UNRAVEL_PT_main"

    def draw(self, context):
        self.layout.label(text="Threads drawn along curves")


def draw_object_menu(self, context):
    self.layout.separator()
    self.layout.operator(UNRAVEL_OT_make.bl_idname, icon='MOD_CLOTH')

classes = (UNRAVEL_OT_make, UNRAVEL_PT_main, UNRAVEL_PT_tears, UNRAVEL_PT_strands)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_object_menu)


def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_object_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)