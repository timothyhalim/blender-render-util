import bpy

class MultiRender_OT_GetScenes(bpy.types.Operator):
    bl_idname = "renderutils.getscenes"
    bl_label = "Get Scenes"
    bl_description = "Get Scenes"

    def execute(self, context):
        context.window_manager.render_property.clear()
        for scene in bpy.data.scenes:
            render = context.window_manager.render_property.add()
            render.scene = scene

        return {'FINISHED'}

class MultiRender_OT_RenderScenes(bpy.types.Operator):
    bl_idname = "renderutils.renderscenes"
    bl_label = "Render Scenes"
    bl_description = "Render Scenes"

    # Define some variables to register
    _timer = None
    scene = None
    stop = None
    rendering = None
    original_output = None
    use_file_extension = None
    render_job = []

    def pre(self, x, y, **kwargs):
        self.rendering = True

        # Restore
        self.scene.render.filepath = self.original_output
        self.scene.render.use_file_extension = self.use_file_extension
        
        print("\n"*2)
        print(f"Rendering {self.scene.name}")
        print("\n"*2)

    def post(self, x, y, **kwargs):
        self.render_job.remove(self.scene) # This is just to render the next
                          # image in another path
        self.rendering = False
        print("\n"*2)
        print(f"Finished Rendering {self.scene.name}")
        print(f'Job Left: {[scene.name for scene in self.render_job]}')
        print("\n"*2)

    def cancelled(self, x, y, **kwargs):
        print("\n"*2)
        print(f"Canceled")
        print("\n"*2)
        # Restore
        self.scene.render.filepath = self.original_output
        self.scene.render.use_file_extension = self.use_file_extension
        
        self.stop = True
        
    def set_render_slot(self, name = None):
        if name is None:
            name = self.scene.name if self.scene else None
        if name:
            render_slot = next((rs for rs in bpy.data.images["Render Result"].render_slots if rs.name == name), None)
            if render_slot is None:
                render_slot = bpy.data.images["Render Result"].render_slots.new(name=name)  

            index = [rs for rs in bpy.data.images["Render Result"].render_slots].index(render_slot)
            bpy.data.images["Render Result"].render_slots.active_index = index

    def execute(self, context):
        self.stop = False
        self.rendering = False

        bpy.app.handlers.render_pre.append(self.pre)
        bpy.app.handlers.render_post.append(self.post)
        bpy.app.handlers.render_cancel.append(self.cancelled)

        # The timer gets created and the modal handler
        # is added to the window manager
        self._timer = context.window_manager.event_timer_add(0.5, window=context.window)
        context.window_manager.modal_handler_add(self)

        scenes = context.window_manager.render_property
        self.render_job = [scene.scene for scene in scenes if scene.renderable]
        self.frame = context.scene.frame_current

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type == 'TIMER': # This event is signaled every half a second
                                  # and will start the render if available

            # If cancelled or no more shots to render, finish.
            if self.stop or len(self.render_job) == 0: 
                # We remove the handlers and the modal timer to clean everything
                bpy.app.handlers.render_pre.remove(self.pre)
                bpy.app.handlers.render_post.remove(self.post)
                bpy.app.handlers.render_cancel.remove(self.cancelled)
                context.window_manager.event_timer_remove(self._timer)

                return {"FINISHED"} # I didn't separate the cancel and finish
                                    # events, because in my case I don't need to,
                                    # but you can create them as you need

            elif not self.rendering: # Nothing is currently rendering.
                                          # Proceed to render.
                self.scene = self.render_job[0]

                # Backup
                self.original_output = self.scene.render.filepath
                self.use_file_extension = self.scene.render.use_file_extension

                # Set Frame and filepath
                self.scene.frame_set(self.frame)
                context.scene.frame_set(self.frame)
                # self.set_render_slot()
                self.scene.render.filepath = self.scene.render.frame_path(frame=self.frame)
                self.scene.render.use_file_extension = False
                
                bpy.ops.render.view_show("INVOKE_DEFAULT") # Open Render window
                # bpy.context.window.scene = self.scene # Change current scene
                bpy.ops.render.render("INVOKE_DEFAULT", write_still = True, scene=self.scene.name)
        
        return {"PASS_THROUGH"}
        # This is very important! If we used "RUNNING_MODAL", this new modal function
        # would prevent the use of the X button to cancel rendering, because this
        # button is managed by the modal function of the render operator,
        # not this new operator!