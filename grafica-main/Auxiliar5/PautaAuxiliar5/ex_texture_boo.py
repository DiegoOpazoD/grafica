# coding=utf-8
"""
Textures and transformations in 2D.
"""

from grafica.assets_path import getAssetPath
import grafica.easy_shaders as es
import grafica.basic_shapes as bs
import grafica.transformations as tr
from grafica.gpu_shape import GPUShape
import glfw
from OpenGL.GL import *
import numpy as np
import sys
import os.path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

__author__ = "Daniel Calderon"
__license__ = "MIT"


def createQuad():

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions
        -0.5, -0.5,
        0.5, -0.5,
        0.5,  0.5,
        -0.5,  0.5, ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return bs.Shape(vertices, indices)


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True

        #####################################################################################################

        self.actual_sprite = 1
        self.x = 0.0

        #####################################################################################################


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

    #####################################################################################################

    elif key == glfw.KEY_RIGHT:
        if controller.x <= 1 - 0.25:
            controller.x += 0.05
            controller.actual_sprite = (controller.actual_sprite + 1) % 10

    elif key == glfw.KEY_LEFT:
        if controller.x >= -1 + 0.25:
            controller.x -= 0.05
            controller.actual_sprite = (controller.actual_sprite - 1) % 10

    #####################################################################################################

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

    ##################################################################################

    # A simple shader program with position and texture coordinates as inputs.
    pipeline = es.ShaderPregunta2()

    ##################################################################################

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    ######################################################################################################

    # Creating shapes on GPU memory

    shapeKnight = createQuad()

    gpuKnight = GPUShape().initBuffers()
    pipeline.setupVAO(gpuKnight)

    # Definimos donde se encuentra la textura
    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    spritesDirectory = os.path.join(thisFolderPath, "Sprites")
    spritePath = os.path.join(spritesDirectory, "sprites.png")

    gpuKnight.texture = es.textureSimpleSetup(
        spritePath, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

    gpuKnight.fillBuffers(shapeKnight.vertices,
                          shapeKnight.indices, GL_STATIC_DRAW)

    ###################################################################################

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        theta = glfw.get_time()
        tx = 0.7 * np.sin(0.5 * theta)
        ty = 0.2 * np.sin(5 * theta)

        # derivative of tx give us the direction
        dtx = 0.7 * 0.5 * np.cos(0.5 * theta)
        if dtx > 0:
            reflex = tr.identity()
        else:
            reflex = tr.scale(-1, 1, 1)

        ##############################################################################################################

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.translate(controller.x, 0, 0),
            tr.uniformScale(0.5)
        ]))

        glUniform1f(glGetUniformLocation(pipeline.shaderProgram,
                    "texture_index"), controller.actual_sprite)

        pipeline.drawCall(gpuKnight)

        ##############################################################################################################

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuKnight.clear()

    glfw.terminate()
