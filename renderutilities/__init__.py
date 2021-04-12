import bpy

from .panel import RenderUtil_PT_Panel

from .operator import RenderUtil_OT_RemoveAsset
from .operator import RenderUtil_OT_CleanVisibilityKey
from .operator import RenderUtil_OT_CreateHiddenAllCollection


classes = (
            RenderUtil_PT_Panel, 
            RenderUtil_OT_RemoveAsset, RenderUtil_OT_CleanVisibilityKey, RenderUtil_OT_CreateHiddenAllCollection
        )

# register, unregister = bpy.utils.register_classes_factory(classes)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
