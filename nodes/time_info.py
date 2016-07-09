import bpy
from node_tree import .

class CMTimeInfoNode(bpy.types.Node, CMNode):
    bl_idname = "CMTimeInfoNode"
    bl_label = "Time Info"
    searchTags = ["Frame"]

    def create(self):
        self.newInput("Scene", "Scene", "scene", hide = True)
        self.newOutput("Float", "Frame", "frame")
        self.newOutput("Float", "Start Frame", "startFrame", hide = True)
        self.newOutput("Float", "End Frame", "endFrame", hide = True)
        self.newOutput("Float", "Frame Rate", "frameRate", hide = True)

    def edit(self):
        inputSocket = self.inputs[0]
        origin = inputSocket.dataOrigin
        if origin is None: return
        if origin.dataType != "Scene":
            inputSocket.removeLinks()
            inputSocket.hide = True

    def getExecutionCode(self):
        isLinked = self.getLinkedOutputsDict()
        if not any(isLinked.values()): return

        yield "if scene is not None:"
        if isLinked["frame"]:      yield "    frame = scene.frame_current_final"
        if isLinked["startFrame"]: yield "    startFrame = scene.frame_start"
        if isLinked["endFrame"]:   yield "    endFrame = scene.frame_end"
        if isLinked["frameRate"]:  yield "    frameRate = scene.render.fps"
        yield "else:"
        yield "    frame, startFrame, endFrame, frameRate = 0, 0, 0, 0"

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)