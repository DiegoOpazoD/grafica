# coding=utf-8
"""Textures and transformations in 3D"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.scene_graph as sg
from grafica.assets_path import getAssetPath

import modelo

SPEED = 0.2

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.posicion_x = 0.0
        self.posicion_y = 0.0
        self.theta = 1.0
        self.eye = np.array([self.posicion_x, self.posicion_y, 0.0])
        self.at = np.array([np.cos(self.theta), np.sin(self.theta), 0.0])

    def process_input(self, dt):
        if (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
            controller.theta += SPEED * dt

        if (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
            controller.theta -= SPEED * dt

        # x, y 
        forward = (controller.at - controller.eye) * 10

        if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS):
            # Cómo defino moverme hacia adelante?
            controller.eye += forward * dt * SPEED
            controller.at += forward * dt * SPEED

        if (glfw.get_key(window, glfw.KEY_S) == glfw.PRESS):
            # Cómo defino moverme hacia adelante?
            controller.eye -= forward * dt * SPEED
            controller.at -= forward * dt * SPEED

# global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS and action != glfw.REPEAT:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Dice", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colors
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()

    # Le decimos a OpenGL que usaremos este ShaderProgram
    glUseProgram(textureShaderProgram.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    skybox = modelo.create_skybox(textureShaderProgram)
    floor = modelo.create_floor(textureShaderProgram)

    # Creamos matriz de proyección
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)
    glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)

    t0 = glfw.get_time()
    camera_theta = -3 * np.pi / 4

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    t1 = glfw.get_time()
    t1 = glfw.get_time()

    # Cada ciclo es un frame, esto que se ve como un video fluido
    # son aproximadamente 30 frames por segundo
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Si quiero moverme en el plano XY
        # Me conviene usar coordenadas polares
        # X = cos(phi) * R
        # Y = sin(phi) * R

        # VELOCIDAD
        AMPLITUD_Z = 2

        controller.process_input(dt) # Acá modifico matemáticamente los vectores con el input

        # Acá estoy seteando la matriz de vista
        controller.at[0], controller.at[1] = np.cos(controller.theta), np.sin(controller.theta)
        # Sin embargo, se verá como que estamos viendo en torno a un mismo punto
        # Si queremos que el punto al que vemos se mueva con nosotros, debemos agregarle
        # controller.eye, así cuando se mueve el eye, también se mueve el at
        controller.at[0] += controller.eye[0]
        controller.at[1] += controller.eye[1]
        view = tr.lookAt(
            np.array([controller.eye[0], controller.eye[1], 1.0]),  # eye 
            np.array([controller.at[0], controller.at[1], 0.0]),  # at
            np.array([0.0, 0.0, 1.0]),  # up
        )
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)


        sg.drawSceneGraphNode(skybox, textureShaderProgram, "model")
        sg.drawSceneGraphNode(floor, textureShaderProgram, "model")       

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
