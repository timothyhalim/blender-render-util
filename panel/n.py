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

        layout.operator('renderutils.getscenes', text="Reload Scenes")
        layout.template_list(
                "Scene_UL_List", 
                "", 
                context.window_manager , 
                "render_property", 
                context.window_manager , 
                "render_index")
        layout.operator('renderutils.renderscenes', text="Render Scenes")
