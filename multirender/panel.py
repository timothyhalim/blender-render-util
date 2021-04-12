import bpy

class MultiRender_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the Properties window"""
    bl_label = "Multi Render"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Render"

    
    @classmethod
    def poll(cls, context):
        registered_scenes = sorted((scene.scene for scene in context.window_manager.render_property if scene != None), key= lambda k: k.name if k else "")
        file_scenes = sorted((scene for scene in bpy.data.scenes), key= lambda k: k.name)
        if registered_scenes != file_scenes:
            # Update Scene List
            context.window_manager.render_property.clear()
            for scene in bpy.data.scenes:
                render = context.window_manager.render_property.add()
                render.scene = scene
        
        return True

    def draw(self, context):
        layout = self.layout
        
        layout.template_list(
                "MultiRender_UL_List", 
                "", 
                context.window_manager , 
                "render_property", 
                context.window_manager , 
                "render_index")
        row = layout.row()
        row.operator('renderutils.renderscenes', text="Render Scenes")
        row.operator('render.view_show', text="", icon="WINDOW")

class MultiRender_UL_List(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index, flt_flag):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=f"{item.name}")
            layout.prop(item, "renderable", text="", toggle=True, icon="RESTRICT_RENDER_OFF" if item.renderable else "RESTRICT_RENDER_ON")

        elif self.layout_type in {'GRID'}:
            pass

class Render_Property(bpy.types.PropertyGroup):
    def get_name(self):
        return getattr(self.scene, "name", "")
        
    def get_renderable(self):
        return getattr(self.scene, "renderable", True)

    def set_renderable(self, value):
        self.scene.renderable = value

    scene : bpy.props.PointerProperty(type=bpy.types.Scene)
    name : bpy.props.StringProperty(get=get_name)
    renderable : bpy.props.BoolProperty(default=True, get=get_renderable, set=set_renderable, )