
from turtle import width
from matplotlib.transforms import Transform
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es

from OpenGL.GL import glClearColor, GL_STATIC_DRAW
import random
from typing import List
from typing import Union #controlador
 
# agergar en otro archivo si se hace muy largo

import glfw
import sys
from OpenGL.GL import *
import grafica.easy_shaders as es
#from controlador import Controller
#from modelos import ave

# agergar en otro archivo si se hace muy largo


class Controller(object):
    model: Union["bird", None]  # Con esto queremos decir que el tipo de modelo es 'bird' (nuestra clase) ó None

    def __init__(self):
        self.model = None
    
    def set_model(self, m):
        self.model = m

    def on_key(self, window, key, scancode, action, mods):
        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return
        if key == glfw.KEY_ESCAPE:
            sys.exit()

if __name__ == "__main__":
    if not glfw.init():
        sys.exit()
    #hacemos la ventana
    width, height = 600, 600
    window = glfw.create_window(width, height, "ave", None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)

    #hacemos el controlador
    controller = Controller()
    glfw.set_key_callback(window, controller.on_key)

    #pipeline
    pipeline = es.SimpleTransformShaderProgram()
    glUseProgram(pipeline.shaderProgram)
    glClearColor(0.85, 0.85, 0.85, 1)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    #modelos
    ave = bird(pipeline)

    #Pasamos los modelos al controlador
    ave = ave 

    # While
    t0 = glfw.get_time()
    while not glfw.window_should_close(window):  # Mientras no se cierre la ventana

        ti = glfw.get_time()
        dt = ti - t0  # dt: Tiempo que paso entre dos cuadros del juego
        t0 = ti

        # Atrapamos los eventos
        glfw.poll_events()

        # Actualizamos los modelos
        ave.update(dt)

        # Dibujamos los modelos
        glClear(GL_COLOR_BUFFER_BIT)
        ave.drawn(pipeline)
        glfw.swap_buffers(window)

    # Terminamos la app
    glfw.terminate()

#cambiar de archivo si es muy largo CONTROLADOR

def create_gpu(shape, pipeline):
    gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpu)
    gpu.fillBuffers(shape.vertives, shape.indices, GL_STATIC_DRAW)
    return gpu

class bird(object):
    
    def __int__(self, pipeline):
        gpu_body_quad = create_gpu(bs.createColorQuad(1,1,0),pipeline)
        gpu_eyes_quad = create_gpu(bs.createColorQuad(0,0,0), pipeline)

        body = sg.SceneGraphNode("body")
        body.transform = tr.uniformScale(1)
        body.childs += [gpu_body_quad]

        eyes = sg.SceneGraphNode("eyes")
        eyes.transform = tr.scale(0,25,-0,25,1)
        
        #ensablee del pajaro
        ave = sg.SceneGraphNode("ave")
        ave.transform = tr.matmul([tr.scale(0.4, 0.4, 0), tr.translate(0, -1.25, 0)])
        ave.childs += [body, eyes]

        transform_ave = sg.SceneGraphNode("aveTR")
        transform_ave.childs += [ave]

        self.model = transform_ave
        self.pos = 0
        self.y = 0 #Variable que indica la posicion visual del pajaro
        self.alive = True
    def drawn(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
    
    def modifymodel(self):
        # Transforma la geometria del modelo segun las variables internas
        # Podria ser una funcion hiper gigante
        self.model.transform = tr.translate(0, self.y, 0)
    
    def update(self, dt):
        dt *= 10
        g = 9,8
        self.pos -= dt**2*g
        self.modifymodel()
    
    def move_up(self):
        if not self.alive:
            return
        self.pos += 20


#cambiar de archivo si es muy largo VISTA


        









    
    
