import bpy

from .module.blender import Command

class RenderUtil_OT_RemoveAsset(bpy.types.Operator):
    bl_idname = "renderutils.removeasset"
    bl_label = "Remove Selected Asset"
    bl_description = "Remove Selected Asset"

    def execute(self, context):
        if context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        selection = context.selected_objects
        for object in selection:
            Command.remove_asset_using_object(context, object)

        return {'FINISHED'}

class RenderUtil_OT_CleanVisibilityKey(bpy.types.Operator):
    bl_idname = "renderutils.cleanvisibilitykey"
    bl_label = "Clean Selected Object Visibility Animation"
    bl_description = "Clean Selected Object Visibility Animation"

    def execute(self, context):
        if context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        selection = context.selected_objects
        for object in selection:
            Command.clear_object_animation(object, 'hide_viewport')
            Command.clear_object_animation(object, 'hide_render')
                    

        return {'FINISHED'}