import bpy


axis_x = True
axis_y = True
axis_z = False


class ToggleGrid(bpy.types.Operator):
    bl_idname = "machin3.toggle_grid"
    bl_label = "Toggle Grid"
    bl_description = "Toggle Grid, distinguish between the grid in regular views and orthographic side views"
    bl_options = {'REGISTER'}

    def execute(self, context):
        global axis_x, axis_y, axis_z

        view = context.space_data
        overlay = view.overlay
        perspective_type = view.region_3d.view_perspective

        mode = "GRID" if perspective_type == "ORTHO" and view.region_3d.is_orthographic_side_view else "FLOOR"

        if mode == "FLOOR":
            if overlay.show_floor:
                # get axes states
                axis_x = overlay.show_axis_x
                axis_y = overlay.show_axis_y
                axis_z = overlay.show_axis_z

                # turn grid OFF
                overlay.show_floor = False

                # turn axes OFF
                overlay.show_axis_x = False
                overlay.show_axis_y = False
                overlay.show_axis_z = False

            else:
                # turn grid ON
                overlay.show_floor = True

                # turn axes ON (according to previous states)
                overlay.show_axis_x = axis_x
                overlay.show_axis_y = axis_y
                overlay.show_axis_z = axis_z

        elif mode == "GRID":
            overlay.show_ortho_grid = not overlay.show_ortho_grid

        return {'FINISHED'}


class ToggleWireframe(bpy.types.Operator):
    bl_idname = "machin3.toggle_wireframe"
    bl_label = "Toggle Wireframe"
    bl_options = {'REGISTER'}

    @classmethod
    def description(cls, context, properties):
        if context.mode == 'OBJECT':
            return "Toggle Wireframe display for the selected objects\nNothing Selected: Toggle Wireframe Overlay, affecting all objects"
        elif context.mode == 'EDIT_MESH':
            return "Toggle X-Ray, resembling how edit mode wireframes worked in Blender 2.79"

    def execute(self, context):
        overlay = context.space_data.overlay

        if context.mode == "OBJECT":
            sel = context.selected_objects

            if sel:
                for obj in sel:
                    obj.show_wire = not obj.show_wire
                    obj.show_all_edges = obj.show_wire
            else:
                overlay.show_wireframes = not overlay.show_wireframes


        elif context.mode == "EDIT_MESH":
            context.scene.M3.show_edit_mesh_wire = not context.scene.M3.show_edit_mesh_wire

        return {'FINISHED'}


class ToggleOutline(bpy.types.Operator):
    bl_idname = "machin3.toggle_outline"
    bl_label = "Toggle Outline"
    bl_description = "Toggle Object Outlines"
    bl_options = {'REGISTER'}

    def execute(self, context):
        shading = context.space_data.shading

        shading.show_object_outline = not shading.show_object_outline

        return {'FINISHED'}


class ToggleCavity(bpy.types.Operator):
    bl_idname = "machin3.toggle_cavity"
    bl_label = "Toggle Cavity"
    bl_description = "Toggle Cavity (Screen Space Ambient Occlusion)"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene

        scene.M3.show_cavity = not scene.M3.show_cavity

        return {'FINISHED'}


class ToggleCurvature(bpy.types.Operator):
    bl_idname = "machin3.toggle_curvature"
    bl_label = "Toggle Curvature"
    bl_description = "Toggle Curvature (Edge Highlighting)"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene

        scene.M3.show_curvature = not scene.M3.show_curvature

        return {'FINISHED'}
