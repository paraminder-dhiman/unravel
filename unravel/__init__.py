import bpy
import os


ASSET_FILE = os.path.join(os.path.dirname(__file__), "assets", "unravel_nodes.blend")
GROUP_NAMES = ("Unravel Tears", "Unravel Threads", "Unravel Strand")


TEAR_INPUTS = ("Hole Size", "Edge Noise", "Noise Scale", "Detail", "Seed")
THICKNESS_INPUTS = ("Thickness", "Lip Width", "Whole Cloth")
THREAD_SHAPE_INPUTS = ("Density", "Length", "Length Random", "Root Width", "Tip Width")
THREAD_STYLE_INPUTS = ("Clumping", "Curl Radius", "Curl Turns", "Frizz", "Droop", "Resolution", "Seed")
CONTACT_INPUTS = ("Surface Contact", "Contact Offset", "Contact Depth")
STRAND_INPUTS = ("Path", "Fibers", "Fiber Spread", "Twist", "Tip Flare", "Root Width", "Tip Width",
                 "Curl Radius", "Curl Turns", "Frizz", "Point Spacing", "Seed")


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


def find_input(modifier, name):
    for item in modifier.node_group.interface.items_tree:
        if item.item_type == 'SOCKET' and item.in_out == 'INPUT' and item.name == name:
            return getattr(modifier.properties.inputs, item.identifier)
    return None


def set_input(modifier, name, value):
    socket = find_input(modifier, name)
    if socket is not None:
        socket.value = value


def get_cloth(obj):
    if obj is None:
        return None
    if obj.type == 'MESH' and "Unravel Tears" in obj.modifiers:
        return obj
    if obj.type == 'CURVES' and obj.parent and "Unravel Tears" in obj.parent.modifiers:
        return obj.parent
    return None


def get_threads(cloth):
    for child in cloth.children:
        if child.type == 'CURVES' and "Unravel Fray" in child.modifiers:
            return child
    return None


def draw_inputs(layout, modifier, names):
    col = layout.column()
    col.use_property_split = True
    col.use_property_decorate = False
    for name in names:
        socket = find_input(modifier, name)
        if socket is not None:
            col.prop(socket, "value", text=name)


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


class UNRAVEL_OT_paint_tears(bpy.types.Operator):
    bl_idname = "unravel.paint_tears"
    bl_label = "Paint Tears"
    bl_description = "Switch to Weight Paint on the cloth's Tears group"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return get_cloth(context.active_object) is not None

    def execute(self, context):
        cloth = get_cloth(context.active_object)
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        for obj in context.selected_objects:
            obj.select_set(False)
        cloth.select_set(True)
        context.view_layer.objects.active = cloth
        cloth.vertex_groups.active_index = cloth.vertex_groups["Tears"].index
        bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
        return {'FINISHED'}


class UNRAVEL_PT_main(bpy.types.Panel):
    bl_label = "Unravel"
    bl_idname = "UNRAVEL_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unravel"

    def draw(self, context):
        layout = self.layout
        cloth = get_cloth(context.active_object)
        if cloth is None:
            layout.label(text="Select a cloth object", icon='INFO')
            layout.operator(UNRAVEL_OT_make.bl_idname, icon='MOD_CLOTH')
            return
        layout.label(text=cloth.name, icon='MOD_CLOTH')
        if not cloth.data.uv_layers:
            box = layout.box()
            box.label(text="This cloth has no UVs", icon='ERROR')
            box.label(text="Threads need UVs to follow the weave")
        if context.mode == 'PAINT_WEIGHT':
            box = layout.box()
            box.label(text="Paint red where the cloth tears", icon='BRUSH_DATA')
            draw_inputs(box, cloth.modifiers["Unravel Tears"], ("Hole Size", "Edge Noise"))
            box.operator("object.mode_set", text="Done Painting", icon='CHECKMARK').mode = 'OBJECT'


class UNRAVEL_PT_tears(bpy.types.Panel):
    bl_label = "Tears"
    bl_idname = "UNRAVEL_PT_tears"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unravel"
    bl_parent_id = "UNRAVEL_PT_main"

    @classmethod
    def poll(cls, context):
        return get_cloth(context.active_object) is not None

    def draw(self, context):
        layout = self.layout
        tears = get_cloth(context.active_object).modifiers["Unravel Tears"]
        layout.operator(UNRAVEL_OT_paint_tears.bl_idname, icon='BRUSH_DATA')
        draw_inputs(layout, tears, TEAR_INPUTS)
        layout.separator()
        draw_inputs(layout, tears, THICKNESS_INPUTS)


class ThreadsPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unravel"
    bl_parent_id = "UNRAVEL_PT_tears"
    bl_options = {'DEFAULT_CLOSED'}
    modifier_name = ""

    @classmethod
    def get_modifier(cls, context):
        cloth = get_cloth(context.active_object)
        threads = get_threads(cloth) if cloth else None
        if threads is None:
            return None
        return threads.modifiers.get(cls.modifier_name)

    @classmethod
    def poll(cls, context):
        return cls.get_modifier(context) is not None

    def draw_header(self, context):
        self.layout.prop(self.get_modifier(context), "show_viewport", text="")

    def draw(self, context):
        layout = self.layout
        modifier = self.get_modifier(context)
        layout.enabled = modifier.show_viewport
        draw_inputs(layout, modifier, THREAD_SHAPE_INPUTS)
        layout.separator()
        draw_inputs(layout, modifier, THREAD_STYLE_INPUTS)
        layout.separator()
        draw_inputs(layout, modifier, CONTACT_INPUTS)


class UNRAVEL_PT_fray(ThreadsPanel, bpy.types.Panel):
    bl_label = "Fray Threads"
    bl_idname = "UNRAVEL_PT_fray"
    modifier_name = "Unravel Fray"


class UNRAVEL_PT_strays(ThreadsPanel, bpy.types.Panel):
    bl_label = "Stray Threads"
    bl_idname = "UNRAVEL_PT_strays"
    modifier_name = "Unravel Strays"


class UNRAVEL_PT_strands(bpy.types.Panel):
    bl_label = "Strands"
    bl_idname = "UNRAVEL_PT_strands"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unravel"
    bl_parent_id = "UNRAVEL_PT_main"

    @classmethod
    def poll(cls, context):
        return get_cloth(context.active_object) is not None

    def draw(self, context):
        layout = self.layout
        threads = get_threads(get_cloth(context.active_object))
        strands = [m for m in threads.modifiers if m.node_group and m.node_group.name == "Unravel Strand"] if threads else []
        if not strands:
            layout.label(text="No drawn strands yet", icon='INFO')
            return
        for modifier in strands:
            box = layout.box()
            row = box.row()
            row.prop(modifier, "show_viewport", text="")
            row.label(text=modifier.name)
            col = box.column()
            col.enabled = modifier.show_viewport
            draw_inputs(col, modifier, STRAND_INPUTS)


def draw_object_menu(self, context):
    self.layout.separator()
    self.layout.operator(UNRAVEL_OT_make.bl_idname, icon='MOD_CLOTH')

classes = (
    UNRAVEL_OT_make,
    UNRAVEL_OT_paint_tears,
    UNRAVEL_PT_main,
    UNRAVEL_PT_tears,
    UNRAVEL_PT_fray,
    UNRAVEL_PT_strays,
    UNRAVEL_PT_strands,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_object_menu)


def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_object_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)