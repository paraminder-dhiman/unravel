import bpy


class UNRAVEL_PT_main(bpy.types.Panel):
    bl_label = "Unrave"
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
        self.layout.label(text="Holes, thickness and fraying")


class UNRAVEL_PT_strands(bpy.types.Panel):
    bl_label = "Strands"
    bl_idname = "UNRAVEL_PT_strands"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Unravel"
    bl_parent_id = "UNRAVEL_PT_main"

    def draw(self, context):
        self.layout.label(text="Threads drawn along curves")


classes = (UNRAVEL_PT_main, UNRAVEL_PT_tears, UNRAVEL_PT_strands)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)