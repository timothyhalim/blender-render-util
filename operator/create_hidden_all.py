import bpy

from ..module.blender import Command

class RenderUtil_OT_CreateHiddenAllCollection(bpy.types.Operator):
    bl_idname = "renderutils.createhiddenall"
    bl_label = "Hidden All Collection"
    bl_description = "Create Hidden All Collection"

    def execute(self, context):
        name = "Hidden_All"
        hidden_all = Command.create_collection(name)
        all = Command.create_collection("ALL")

        Command.parent(hidden_all, all)

        Command.set_collection_settings(hidden_all, exclude=True)
                    
        return {'FINISHED'}
