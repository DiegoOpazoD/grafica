#ModeloTarea3D

import glfw
from grafica.assets_path import getAssetPath
from grafica.gpu_shape import GPUShape
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import sys, os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from OpenGL.GL import *
import random

#fucnion que crea la forma en la GPU
def createGPUShape(shape, pipeline):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

#tuberias
class tuberia(object):
    def __init__(self, pipeline):
        gpu_tubo = createGPUShape(bs.createColorNormalsCube(0,1,0),pipeline)

        tubo = sg.SceneGraphNode("tubo")
        a = random.randint(20,250)
        tubo.transform = tr.scale(0.25,a/100,0.25)
        tubo.childs += [gpu_tubo]

        tubo_ar = sg.SceneGraphNode("tuboArriva")
        tubo_ar.childs += [tubo]

        tubo_ab = sg.SceneGraphNode("tuboAbajo")
        h = a/100 +0.5+4.5*(a/100)
        tubo_ab.transform = tr.matmul([tr.translate(0,-h,0),tr.scale(1,-10,1)])
        tubo_ab.childs += [tubo]

        parTubos = sg.SceneGraphNode("Partubos")
        parTubos.childs = [tubo_ar, tubo_ab]

        self.model  = parTubos
        self.pos_x = 1.5
        self.pos_y = 1

    def drawn(self, pipeline): #agregar otra coma y un dx
        transform = tr.translate(self.pos_x, self.pos_y, 0)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"),1, GL_TRUE, transform)
        #self.model.transform = tr.translate(self.pos_x, self.pos_y, 0)
        sg.drawSceneGraphNode(self.model,pipeline, "transform")



