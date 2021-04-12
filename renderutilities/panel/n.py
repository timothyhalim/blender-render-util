import bpy

class RenderUtil_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the Properties window"""
    bl_label = "Render Utilities"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Render"

    def draw(self, context):
        layout = self.layout
        
        layout.operator('renderutils.removeasset', text="Remove Selected Asset")
        layout.operator('renderutils.cleanvisibilitykey', text="Clean Selected Visibility Key")
        layout.operator('renderutils.createhiddenall', text="Create Hidden All Collection")
