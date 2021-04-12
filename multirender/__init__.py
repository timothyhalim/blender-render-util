import bpy

from .operator import MultiRender_OT_GetScenes, MultiRender_OT_RenderScenes
from .panel import MultiRender_PT_Panel, MultiRender_UL_List, Render_Property

classes = (MultiRender_OT_GetScenes, MultiRender_OT_RenderScenes, MultiRender_PT_Panel, MultiRender_UL_List, Render_Property)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.renderable = bpy.props.BoolProperty(default=True)
    bpy.types.WindowManager.render_property = bpy.props.CollectionProperty(type=Render_Property)
    bpy.types.WindowManager.render_index = bpy.props.IntProperty()

def unregister():
    del bpy.types.Scene.renderable
    del bpy.types.WindowManager.render_property
    del bpy.types.WindowManager.render_index

    for cls in classes:
        bpy.utils.unregister_class(cls)