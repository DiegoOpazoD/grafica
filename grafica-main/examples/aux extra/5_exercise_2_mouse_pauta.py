# coding=utf-8
"""
Interactions with keyboard and mouse via GLFW/python.

More information at:
https://www.glfw.org/docs/latest/input_guide.html

How to convert GLFW/C calls to GLFW/python
https://pypi.org/project/glfw/
"""

import glfw
from OpenGL.GL import *
import numpy as np
import sys
import os.path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es

__author__ = "Daniel Calderon"
__license__ = "MIT"

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


class GPUShapeClickableRect(es.GPUShape):
    """
    Mantenemos las posiciones originales para que no se pierdan al
    aplicar transformaciones.
    """
    def __init__(self):
        super(GPUShapeClickableRect, self).__init__()  # inicializa lo de GPUShape
        self.x0, self.y0, self.xf, self.yf = 0, 0, 0, 0
        self.original_pos_0 = np.array([-0.5, -0.5, 0.0, 1.0], dtype=np.float32)
        self.original_pos_1 = np.array([+0.5, +0.5, 0.0, 1.0], dtype=np.float32)

    # Función para ver que pos_x y pos_y están dentro del cuadrado
    # definido por (x0, y0), (xf, yf)
    def inside_rect(self, gl_pos):
        if self.x0 < gl_pos[0] < self.xf and self.y0 < gl_pos[1] < self.yf:
            return True
        return False

    # Aplica una transformación a los puntos del modelo
    # Permitiendo detectar clicks. Esto no afecta a la vista, así que
    # Debemos aplicar la misma transformación a la GPUShape en el shader
    def apply_transform_to_points(self, transform):
        self.x0, self.y0, _, _ = transform @ self.original_pos_0
        self.xf, self.yf, _, _ = transform @ self.original_pos_1

# A class to control the application
class Controller:
    def __init__(self):
        """
        mousePos = Posición del mouse en coordenadas de resolución
        GLMousePos = Posición del mouse en la pantalla en x [-1, 1] e y [-1, 1]
        """
        self.leftClickOn = False
        self.theta = 0.0
        self.mousePos = (0.0, 0.0)
        self.GLMousePos = (0.0, 0.0)  # 2 * (controller.mousePos[0] - width / 2) / width
        self.clickable_quads = []
        self.click_count = 0


# We will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)


def cursor_pos_callback(window, x, y):
    global controller
    controller.mousePos = (x, y)


def mouse_button_callback(window, button, action, mods):
    global controller

    """
    glfw.MOUSE_BUTTON_1: left click
    glfw.MOUSE_BUTTON_2: right click
    glfw.MOUSE_BUTTON_3: scroll click
    """
    
    if (action == glfw.PRESS or action == glfw.REPEAT):
        if (button == glfw.MOUSE_BUTTON_1):
            controller.leftClickOn = True
            # Podemos usar un for para considerar todos los cuadrados
            # for clickable_quad in controller.clickable_quads:
            if controller.clickable_quads[0].inside_rect(controller.GLMousePos):
                print(f"Apretado el cuadro rojo {controller.click_count}")
                controller.click_count += 1

        if (button == glfw.MOUSE_BUTTON_2):
            print("Mouse click - button 2:", (controller.GLMousePos))

        if (button == glfw.MOUSE_BUTTON_3):
            print("Mouse click - button 3")

    elif (action == glfw.RELEASE):
        if (button == glfw.MOUSE_BUTTON_1):
            controller.leftClickOn = False


def scroll_callback(window, x, y):
    print("Mouse scroll:", x, y)


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 600

    window = glfw.create_window(width, height, "Handling mouse events", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Connecting callback functions to handle mouse events:
    # - Cursor moving over the window
    # - Mouse buttons input
    # - Mouse scroll
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)



    # Convenience function to ease initialization
    def createGPUColorQuad(r, g, b, pipeline):
        shapeQuad = bs.createColorQuad(r, g, b)
        gpuQuad = GPUShapeClickableRect().initBuffers()
        pipeline.setupVAO(gpuQuad)
        # Borders
        gpuQuad.x0 = -0.5
        gpuQuad.xf = 0.5
        gpuQuad.y0 = -0.5
        gpuQuad.yf = 0.5

        gpuQuad.fillBuffers(shapeQuad.vertices, shapeQuad.indices, GL_STATIC_DRAW)
        return gpuQuad

    # Creating our shader program and telling OpenGL to use it
    pipeline = es.SimpleTransformShaderProgram()
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Creamos las figuras con color
    redQuad = createGPUColorQuad(1, 0, 0, pipeline)
    yellowQuad = createGPUColorQuad(1, 1, 0, pipeline)
    greenQuad = createGPUColorQuad(0, 1, 0, pipeline)

    controller.clickable_quads = [redQuad, yellowQuad]
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    t0 = glfw.get_time()

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Setting transform and drawing the rotating red quad
        t = glfw.get_time()

        # Getting the mouse location in opengl coordinates
        controller.GLMousePos = (
            2 * (controller.mousePos[0] - width / 2) / width,
            2 * (height / 2 - controller.mousePos[1]) / height
        )

        redQuadTransform = tr.matmul([
            tr.translate(0.5, 0.0, 0.0),
            tr.uniformScale(np.abs(np.sin(t) * 3))
        ])

        redQuad.apply_transform_to_points(redQuadTransform)  # Estoy modificando el modelo para que me marque
        # x0, y0, xf, yf

        # Estoy modificando la vista
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, redQuadTransform)
        pipeline.drawCall(redQuad)


        greenQuadTransform = tr.matmul([
            tr.translate(*controller.GLMousePos, 0),
            tr.uniformScale(0.3)
        ])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, np.matmul(
            tr.translate(*controller.GLMousePos, 0),
            tr.uniformScale(0.3)
        ))
        pipeline.drawCall(greenQuad)


        # Las teclas no presionadas están en el estado glfw.RELEASE
        # Si apretamos KEY_LEFT_CONTROL, el cuadro amarillo deja de dibujarse
        # Pues ya no marca como RELEASE
        if (glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.RELEASE):
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, np.matmul(
                tr.translate(-0.6, 0.6, 0.0),
                tr.uniformScale(0.2)
            ))
            pipeline.drawCall(yellowQuad)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    redQuad.clear()
    yellowQuad.clear()
    greenQuad.clear()

    glfw.terminate()
