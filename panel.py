import bpy

class RenderUtil_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the Properties window"""
    bl_label = "Render Utilities"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Render"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('renderutils.removeasset', text="Remove Selected Asset")
        row = layout.row()
        row.operator('renderutils.cleanvisibilitykey', text="Clean Selected Visibility Key")


        # row.prop(context.scene, "maya_batch", text="Batch")

        # row.operator('assetqc.autorun', text="Autorun")

        # row = layout.row().split(factor=0.59)
        # col1 = row.column()
        # col2 = row.column()

        # row1 = col1.row()
        # row1.label(text="Blend")
        # row1.label(text="Name")
        
        # row2 = col2.row()
        # row2.label(icon="NODETREE")
        # row2.label(text="Type", icon="NODE")
        # row2.label(text="Vertex", icon="VERTEXSEL")
        # row2.label(text="UV", icon="UV_VERTEXSEL")

        # layout.template_list("AssetQC_UL_List", "", context.scene, "col", context.scene, "col_idx")
