# coding=utf-8
"""
Textures and transformations in 2D.
La idea de este ejercicio es mostrar que, teniendo dos estados:
A y B, podemos lograr generar los estados intermedios
con una función de interpolación:
f(t) = A * t + B * (1 - t)
"""

import glfw
from OpenGL.GL import *
import numpy as np
import sys, os.path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grafica.gpu_shape import GPUShape
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
from grafica.assets_path import getAssetPath

__author__ = "Daniel Calderon"
__license__ = "MIT"


LINEAR_INTERPOLATION_INDEX = 0
QUADRATIC_INTERPOLATION_INDEX = 1

ROTATION_WASTED_KEYFRAME_1 = np.pi * 0.25
ROTATION_WASTED_KEYFRAME_2 = np.pi * -0.25

def linear_interpol(t):
    return ROTATION_WASTED_KEYFRAME_1 * t + ROTATION_WASTED_KEYFRAME_2 * (1 - t)

def quadratic_interpol(t):
    return ROTATION_WASTED_KEYFRAME_1 * t ** 2 + ROTATION_WASTED_KEYFRAME_2 * (1 - t) ** 2

INTERPOLATION_TYPES = (linear_interpol, quadratic_interpol)


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.t_index = 0
        self.interpol_type = linear_interpol  # one of INTERPOLATION_TYPES
        self.interpol_index = LINEAR_INTERPOLATION_INDEX

# global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    elif key == glfw.KEY_RIGHT:
        controller.t_index = (controller.t_index - 1) % 10

    elif key == glfw.KEY_LEFT:
        controller.t_index = (controller.t_index + 1) % 10

    elif key == glfw.KEY_I:
        controller.interpol_index = (controller.interpol_index + 1) % (len(INTERPOLATION_TYPES))
        controller.interpol_type = INTERPOLATION_TYPES[controller.interpol_index]
        print(f'Interpolation method changed to: {str(INTERPOLATION_TYPES[controller.interpol_index])}')
    else:
        print('Unknown key')


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Boo!", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # A simple shader program with position and texture coordinates as inputs.
    pipeline = es.SimpleTextureTransformShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Definimos donde se encuentra la textura
    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    spritesDirectory = os.path.join(thisFolderPath, "Sprites")
    spritePath_wasted = os.path.join(spritesDirectory, "wasted.png")

    # Creating shapes on GPU memory
    shapeBoo = bs.createTextureQuad(1, 1)
    gpuBoo = GPUShape().initBuffers()
    pipeline.setupVAO(gpuBoo)
    gpuBoo.fillBuffers(shapeBoo.vertices, shapeBoo.indices, GL_STATIC_DRAW)
    gpuBoo.texture = es.textureSimpleSetup(
        spritePath_wasted, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

    t0 = glfw.get_time()
    t1 = glfw.get_time()


    time_frames = np.arange(0.0, 1.0, 0.0001)
    time_index = 0
    
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        t1 = glfw.get_time()
        dt = t1 - t0

        time_index = (time_index + 1) % (len(time_frames) - 1)

        # Selecting interpolation method
        interpol = controller.interpol_type

        # Drawing the shapes
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, 
            tr.matmul([
                tr.scale(0.5, 0.5, 1.0),
                tr.rotationZ(interpol(time_frames[time_index])),
                # tr.rotationZ(interpol(time_frames[controller.t_index])),
            ])
        )
        pipeline.drawCall(gpuBoo)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
        t0 = glfw.get_time()

    # freeing GPU memory
    gpuBoo.clear()

    glfw.terminate()
