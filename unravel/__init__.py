import bpy
import os
import random

ASSET_FILE = os.path.join(os.path.dirname(__file__), "assets", "unravel_nodes.blend")
HELP_FILE = os.path.join(os.path.dirname(__file__), "Help.txt")
GROUP_NAMES = ("Unravel Tears", "Unravel Threads", "Unravel Strand")


TEAR_INPUTS = ("Hole Size", "Edge Noise", "Noise Scale", "Edge Smoothing", "Detail", "Seed")
THICKNESS_INPUTS = ("Thickness", "Lip Width", "Whole Cloth")
THREAD_SHAPE_INPUTS = ("Density", "Length", "Length Random", "Root Width", "Tip Width")
THREAD_STYLE_INPUTS = ("Clumping", "Direction Random", "Curl Radius", "Curl Turns", "Frizz", "Frizz Waves",
                       "Droop", "Resolution", "Seed")
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
    "Direction Random": 0.3,
}


PRESETS = {
    "BURLAP": {
        "Unravel Tears": {"Edge Noise": 0.7, "Noise Scale": 9.0, "Edge Smoothing": 8, "Thickness": 0.006,
                          "Lip Width": 0.05},
        "Unravel Fray": {"Density": 220.0, "Length": 0.06, "Length Random": 0.8, "Root Width": 0.0022,
                         "Tip Width": 0.0012, "Clumping": 0.55, "Direction Random": 0.45,
                         "Curl Radius": 0.0012, "Curl Turns": 6.0, "Frizz": 0.55, "Frizz Waves": 1.5,
                         "Droop": 0.15, "Resolution": 16},
        "Unravel Strays": {"Density": 120.0, "Length": 0.28, "Length Random": 0.7, "Root Width": 0.0018,
                           "Tip Width": 0.0012, "Clumping": 0.15, "Direction Random": 0.35,
                           "Curl Radius": 0.0012, "Curl Turns": 12.0, "Frizz": 0.75, "Frizz Waves": 1.6,
                           "Droop": 0.05, "Resolution": 48},
    },
    "CANVAS": {
        "Unravel Tears": {"Edge Noise": 0.55, "Noise Scale": 11.0, "Edge Smoothing": 10, "Thickness": 0.003,
                          "Lip Width": 0.03},
        "Unravel Fray": {"Density": 420.0, "Length": 0.035, "Length Random": 0.7, "Root Width": 0.0012,
                         "Tip Width": 0.0007, "Clumping": 0.45, "Direction Random": 0.3,
                         "Curl Radius": 0.0006, "Curl Turns": 4.0, "Frizz": 0.3, "Frizz Waves": 1.3,
                         "Droop": 0.05, "Resolution": 12},
        "Unravel Strays": {"Density": 70.0, "Length": 0.2, "Length Random": 0.6, "Root Width": 0.0012,
                           "Tip Width": 0.0008, "Clumping": 0.1, "Direction Random": 0.2,
                           "Curl Radius": 0.0008, "Curl Turns": 8.0, "Frizz": 0.4, "Frizz Waves": 1.3,
                           "Droop": 0.05, "Resolution": 40},
    },
    "DENIM": {
        "Unravel Tears": {"Edge Noise": 0.6, "Noise Scale": 40.0, "Edge Smoothing": 8, "Thickness": 0.0012,
                          "Lip Width": 0.006},
        "Unravel Fray": {"Density": 1500.0, "Length": 0.008, "Length Random": 0.8, "Root Width": 0.0005,
                         "Tip Width": 0.0003, "Clumping": 0.6, "Direction Random": 0.45,
                         "Curl Radius": 0.0003, "Curl Turns": 4.0, "Frizz": 0.55, "Frizz Waves": 1.5,
                         "Droop": 0.1, "Resolution": 10},
        "Unravel Strays": {"Density": 350.0, "Length": 0.06, "Length Random": 0.5, "Root Width": 0.0005,
                           "Tip Width": 0.0004, "Clumping": 0.25, "Direction Random": 0.22,
                           "Curl Radius": 0.0004, "Curl Turns": 10.0, "Frizz": 0.4, "Frizz Waves": 1.5,
                           "Droop": 0.08, "Resolution": 40},
    },
    "TWEED": {
        "Unravel Tears": {"Edge Noise": 0.65, "Noise Scale": 35.0, "Edge Smoothing": 5, "Thickness": 0.003,
                          "Lip Width": 0.008},
        "Unravel Fray": {"Density": 1400.0, "Length": 0.012, "Length Random": 0.85, "Root Width": 0.0007,
                         "Tip Width": 0.00025, "Clumping": 0.3, "Direction Random": 0.65,
                         "Curl Radius": 0.0003, "Curl Turns": 4.0, "Frizz": 0.7, "Frizz Waves": 2.5,
                         "Droop": 0.15, "Resolution": 14},
        "Unravel Strays": {"Density": 200.0, "Length": 0.03, "Length Random": 0.7, "Root Width": 0.0006,
                           "Tip Width": 0.00025, "Clumping": 0.1, "Direction Random": 0.65,
                           "Curl Radius": 0.0004, "Curl Turns": 5.0, "Frizz": 0.75, "Frizz Waves": 2.5,
                           "Droop": 0.2, "Resolution": 28},
    },
    "LINEN": {
        "Unravel Tears": {"Edge Noise": 0.55, "Noise Scale": 45.0, "Edge Smoothing": 8, "Thickness": 0.0008,
                          "Lip Width": 0.005},
        "Unravel Fray": {"Density": 1800.0, "Length": 0.009, "Length Random": 0.8, "Root Width": 0.0004,
                         "Tip Width": 0.0002, "Clumping": 0.4, "Direction Random": 0.4,
                         "Curl Radius": 0.0003, "Curl Turns": 5.0, "Frizz": 0.45, "Frizz Waves": 2.0,
                         "Droop": 0.25, "Resolution": 10},
        "Unravel Strays": {"Density": 220.0, "Length": 0.045, "Length Random": 0.7, "Root Width": 0.00035,
                           "Tip Width": 0.0002, "Clumping": 0.1, "Direction Random": 0.4,
                           "Curl Radius": 0.0004, "Curl Turns": 8.0, "Frizz": 0.55, "Frizz Waves": 2.0,
                           "Droop": 0.2, "Resolution": 32},
    },
    "COTTON": {
        "Unravel Tears": {"Edge Noise": 0.5, "Noise Scale": 50.0, "Edge Smoothing": 8, "Thickness": 0.0005,
                          "Lip Width": 0.004},
        "Unravel Fray": {"Density": 2200.0, "Length": 0.006, "Length Random": 0.8, "Root Width": 0.0003,
                         "Tip Width": 0.00015, "Clumping": 0.3, "Direction Random": 0.55,
                         "Curl Radius": 0.0002, "Curl Turns": 4.0, "Frizz": 0.65, "Frizz Waves": 2.5,
                         "Droop": 0.25, "Resolution": 10},
        "Unravel Strays": {"Density": 260.0, "Length": 0.025, "Length Random": 0.7, "Root Width": 0.00025,
                           "Tip Width": 0.00015, "Clumping": 0.1, "Direction Random": 0.55,
                           "Curl Radius": 0.0003, "Curl Turns": 6.0, "Frizz": 0.75, "Frizz Waves": 2.5,
                           "Droop": 0.3, "Resolution": 24},
    },
    "SILK": {
        "Unravel Tears": {"Edge Noise": 0.35, "Noise Scale": 40.0, "Edge Smoothing": 12, "Thickness": 0.0003,
                          "Lip Width": 0.003},
        "Unravel Fray": {"Density": 2600.0, "Length": 0.012, "Length Random": 0.7, "Root Width": 0.0002,
                         "Tip Width": 0.00012, "Clumping": 0.5, "Direction Random": 0.2,
                         "Curl Radius": 0.0001, "Curl Turns": 2.0, "Frizz": 0.12, "Frizz Waves": 1.0,
                         "Droop": 0.5, "Resolution": 14},
        "Unravel Strays": {"Density": 260.0, "Length": 0.035, "Length Random": 0.6, "Root Width": 0.00018,
                           "Tip Width": 0.00012, "Clumping": 0.15, "Direction Random": 0.3,
                           "Curl Radius": 0.0002, "Curl Turns": 2.0, "Frizz": 0.22, "Frizz Waves": 1.2,
                           "Droop": 0.4, "Resolution": 40},
    },
    "GAUZE": {
        "Unravel Tears": {"Edge Noise": 0.75, "Noise Scale": 30.0, "Edge Smoothing": 6, "Thickness": 0.0004,
                          "Lip Width": 0.003},
        "Unravel Fray": {"Density": 700.0, "Length": 0.012, "Length Random": 0.8, "Root Width": 0.00035,
                         "Tip Width": 0.0002, "Clumping": 0.1, "Direction Random": 0.45,
                         "Curl Radius": 0.0003, "Curl Turns": 4.0, "Frizz": 0.4, "Frizz Waves": 1.5,
                         "Droop": 0.35, "Resolution": 14},
        "Unravel Strays": {"Density": 200.0, "Length": 0.05, "Length Random": 0.7, "Root Width": 0.0003,
                           "Tip Width": 0.0002, "Clumping": 0.0, "Direction Random": 0.45,
                           "Curl Radius": 0.0004, "Curl Turns": 6.0, "Frizz": 0.45, "Frizz Waves": 1.5,
                           "Droop": 0.3, "Resolution": 32},
    },
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
        modifier.id_data.update_tag()


def get_cloth(obj):
    if obj is None:
        return None
    if obj.type == 'MESH' and "Unravel Tears" in obj.modifiers:
        return obj
    if obj.type in {'CURVES', 'CURVE'} and obj.parent and "Unravel Tears" in obj.parent.modifiers:
        return obj.parent
    return None


def get_threads(cloth):
    for child in cloth.children:
        if child.type == 'CURVES' and "Unravel Fray" in child.modifiers:
            return child
    return None

THREAD_MATERIAL_NAME = "Unravel Thread"


def get_thread_material():
    material = bpy.data.materials.get(THREAD_MATERIAL_NAME)
    if material is None:
        material = bpy.data.materials.new(THREAD_MATERIAL_NAME)
        material.use_nodes = True
        bsdf = material.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (0.45, 0.36, 0.25, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.85
        material.diffuse_color = (0.45, 0.36, 0.25, 1.0)
    return material


def apply_thread_material(cloth):
    threads = get_threads(cloth)
    if threads is None:
        return
    thread_material = get_thread_material()
    use_cloth = cloth.unravel_cloth_colour and cloth.active_material is not None
    for modifier in threads.modifiers:
        if modifier.type != 'NODES' or modifier.node_group is None:
            continue
        if modifier.node_group.name == "Unravel Threads":
            set_input(modifier, "Material", cloth.active_material if use_cloth else thread_material)
        elif modifier.node_group.name == "Unravel Strand":
            set_input(modifier, "Material", thread_material)
    sync_material_slots(threads)


def sync_material_slots(threads):
    materials = []
    for modifier in threads.modifiers:
        socket = find_input(modifier, "Material") if modifier.type == 'NODES' and modifier.node_group else None
        if socket is not None and socket.value is not None and socket.value not in materials:
            materials.append(socket.value)
    threads.data.materials.clear()
    for material in materials:
        threads.data.materials.append(material)


def update_cloth_colour(self, context):
    apply_thread_material(self)


def draw_inputs(layout, modifier, names):
    col = layout.column()
    col.use_property_split = True
    col.use_property_decorate = False
    for name in names:
        socket = find_input(modifier, name)
        if socket is None:
            continue
        if name == "Seed":
            row = col.row(align=True)
            row.prop(socket, "value", text=name)
            row.operator(UNRAVEL_OT_randomize_seed.bl_idname, text="", icon='FILE_REFRESH').modifier_name = modifier.name
        else:
            col.prop(socket, "value", text=name)


class UNRAVEL_OT_make(bpy.types.Operator):
    bl_idname = "unravel.make"
    bl_label = "Make Unravel"
    bl_description = "Set up tears and threads on the selected cloth"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and "Unravel Tears" not in obj.modifiers

    def execute(self, context):
        cloth = context.active_object
        if not cloth.data.polygons:
            self.report({'ERROR'}, cloth.name + " needs faces to tear")
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

        apply_thread_material(cloth)

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

class UNRAVEL_OT_add_strand(bpy.types.Operator):
    bl_idname = "unravel.add_strand"
    bl_label = "Unravel Strand"
    bl_description = "Draw a loose thread strand on an Unravel cloth"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        cloth = get_cloth(context.active_object)
        return context.mode == 'OBJECT' and cloth is not None and get_threads(cloth) is not None

    def execute(self, context):
        cloth = get_cloth(context.active_object)
        threads = get_threads(cloth)
        load_node_groups()

        curve = bpy.data.curves.new("Strand Path", 'CURVE')
        curve.dimensions = '3D'
        path = bpy.data.objects.new("Strand Path", curve)
        for collection in cloth.users_collection:
            collection.objects.link(path)
        path.parent = cloth

        strand = threads.modifiers.new("Unravel Strand", 'NODES')
        strand.node_group = bpy.data.node_groups["Unravel Strand"]
        set_input(strand, "Path", path)
        apply_thread_material(cloth)

        for obj in context.selected_objects:
            obj.select_set(False)
        path.select_set(True)
        context.view_layer.objects.active = path
        bpy.ops.object.mode_set(mode='EDIT')
        context.scene.tool_settings.curve_paint_settings.depth_mode = 'SURFACE'
        try:
            bpy.ops.wm.tool_set_by_id(name="builtin.draw")
        except RuntimeError:
            pass
        self.report({'INFO'}, "Draw on the cloth, then press Tab when you are done")
        return {'FINISHED'}


class UNRAVEL_OT_help(bpy.types.Operator):
    bl_idname = "unravel.help"
    bl_label = "Unravel Help"
    bl_description = "Open the Unravel guide in your text editor"

    def execute(self, context):
        bpy.ops.wm.path_open(filepath=HELP_FILE)
        return {'FINISHED'}


class UNRAVEL_OT_randomize_seed(bpy.types.Operator):
    bl_idname = "unravel.randomize_seed"
    bl_label = "Randomize Seed"
    bl_description = "Pick a new random seed"
    bl_options = {'REGISTER', 'UNDO'}

    modifier_name: bpy.props.StringProperty()

    def execute(self, context):
        cloth = get_cloth(context.active_object)
        if cloth is None:
            return {'CANCELLED'}
        modifier = cloth.modifiers.get(self.modifier_name)
        if modifier is None:
            threads = get_threads(cloth)
            modifier = threads.modifiers.get(self.modifier_name) if threads else None
        if modifier is None:
            return {'CANCELLED'}
        set_input(modifier, "Seed", random.randint(0, 9999))
        return {'FINISHED'}

class UNRAVEL_OT_apply_preset(bpy.types.Operator):
    bl_idname = "unravel.apply_preset"
    bl_label = "Apply Preset"
    bl_description = "Set the tears and threads to look like a type of cloth"
    bl_options = {'REGISTER', 'UNDO'}

    preset: bpy.props.EnumProperty(
        name="Preset",
        items=(
            ('BURLAP', "Burlap", "Coarse, loose weave with thick hairy threads"),
            ('CANVAS', "Canvas", "Tight, stiff weave with short neat threads"),
            ('DENIM', "Denim", "Sturdy twill with short, bunched threads"),
            ('TWEED', "Tweed", "Thick wool with fuzzy, frizzy threads"),
            ('LINEN', "Linen", "Fine, soft weave with thin wispy threads"),
            ('COTTON', "Cotton", "Light shirting with short fine threads"),
            ('SILK', "Silk", "Very fine and smooth, with long slippery threads"),
            ('GAUZE', "Gauze", "Thin open weave with sparse loose threads"),
        ),
    )

    @classmethod
    def poll(cls, context):
        return get_cloth(context.active_object) is not None

    def execute(self, context):
        cloth = get_cloth(context.active_object)
        threads = get_threads(cloth)
        for modifier_name, values in PRESETS[self.preset].items():
            modifier = cloth.modifiers.get(modifier_name)
            if modifier is None and threads is not None:
                modifier = threads.modifiers.get(modifier_name)
            if modifier is None:
                continue
            for name, value in values.items():
                set_input(modifier, name, value)
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
            row = layout.row()
            row.label(text="Select a cloth object", icon='INFO')
            row.operator(UNRAVEL_OT_help.bl_idname, text="", icon='HELP')
            layout.operator(UNRAVEL_OT_make.bl_idname, icon='MOD_CLOTH')
            return
        row = layout.row()
        row.label(text=cloth.name, icon='MOD_CLOTH')
        row.operator_menu_enum(UNRAVEL_OT_apply_preset.bl_idname, "preset", text="Presets", icon='PRESET')
        row.operator(UNRAVEL_OT_help.bl_idname, text="", icon='HELP')
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
        draw_inputs(layout, modifier, ("Viewport Density",))
        layout.separator()
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

class UNRAVEL_PT_material(bpy.types.Panel):
    bl_label = "Thread Material"
    bl_idname = "UNRAVEL_PT_material"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unravel"
    bl_parent_id = "UNRAVEL_PT_main"

    @classmethod
    def poll(cls, context):
        return get_cloth(context.active_object) is not None

    def draw(self, context):
        layout = self.layout
        cloth = get_cloth(context.active_object)
        layout.prop(cloth, "unravel_cloth_colour")
        if cloth.unravel_cloth_colour and cloth.active_material is not None:
            layout.label(text="Using " + cloth.active_material.name, icon='MATERIAL')
            return
        if cloth.unravel_cloth_colour:
            layout.label(text="The cloth has no material", icon='INFO')
        material = get_thread_material()
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        if bsdf is None:
            layout.label(text="Edit " + material.name + " in the Shading tab", icon='MATERIAL')
            return
        col = layout.column()
        col.use_property_split = True
        col.use_property_decorate = False
        col.prop(bsdf.inputs["Base Color"], "default_value", text="Colour")
        col.prop(bsdf.inputs["Roughness"], "default_value", text="Roughness")


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
        layout.operator(UNRAVEL_OT_add_strand.bl_idname, text="Add Strand", icon='CURVE_BEZCURVE')
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


class UNRAVEL_MT_object(bpy.types.Menu):
    bl_label = "Unravel"
    bl_idname = "UNRAVEL_MT_object"

    def draw(self, context):
        layout = self.layout
        layout.operator(UNRAVEL_OT_make.bl_idname, icon='MOD_CLOTH')
        layout.operator(UNRAVEL_OT_paint_tears.bl_idname, icon='BRUSH_DATA')
        layout.operator(UNRAVEL_OT_add_strand.bl_idname, text="Add Strand", icon='CURVE_BEZCURVE')
        layout.operator_menu_enum(UNRAVEL_OT_apply_preset.bl_idname, "preset", text="Presets", icon='PRESET')
        layout.separator()
        layout.operator(UNRAVEL_OT_help.bl_idname, icon='HELP')


def draw_object_submenu(self, context):
    self.layout.separator()
    self.layout.menu(UNRAVEL_MT_object.bl_idname, icon='MOD_CLOTH')


def draw_add_menu(self, context):
    self.layout.operator(UNRAVEL_OT_add_strand.bl_idname, icon='CURVE_BEZCURVE')


def draw_object_menu(self, context):
    if not UNRAVEL_OT_make.poll(context):
        return
    self.layout.separator()
    self.layout.operator(UNRAVEL_OT_make.bl_idname, icon='MOD_CLOTH')

classes = (
    UNRAVEL_OT_make,
    UNRAVEL_OT_paint_tears,
    UNRAVEL_OT_add_strand,
    UNRAVEL_OT_help,
    UNRAVEL_OT_randomize_seed,
    UNRAVEL_OT_apply_preset,
    UNRAVEL_MT_object,
    UNRAVEL_PT_main,
    UNRAVEL_PT_tears,
    UNRAVEL_PT_fray,
    UNRAVEL_PT_strays,
    UNRAVEL_PT_material,
    UNRAVEL_PT_strands,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.unravel_cloth_colour = bpy.props.BoolProperty(
        name="Take Colour from Cloth",
        description="Threads use the cloth's own material, coloured by where each thread grows from",
        default=True,
        update=update_cloth_colour,
    )
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_object_menu)
    bpy.types.VIEW3D_MT_object.append(draw_object_submenu)
    bpy.types.VIEW3D_MT_add.append(draw_add_menu)


def unregister():
    bpy.types.VIEW3D_MT_add.remove(draw_add_menu)
    bpy.types.VIEW3D_MT_object.remove(draw_object_submenu)
    del bpy.types.Object.unravel_cloth_colour
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_object_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)