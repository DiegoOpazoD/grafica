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
from typing import List
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from OpenGL.GL import *
import random
import numpy as np

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

    def drawn(self, pipeline, dx): #agregar otra coma y un dx
        transform = tr.translate(self.pos_x, self.pos_y, 0)
        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"),1, GL_TRUE, transform) no se que hace esto en realidad
        self.model.transform = tr.translate(self.pos_x, self.pos_y, 0)
        sg.drawSceneGraphNode(self.model,pipeline, "transform")
    
    def update(self, dt):
        self.pos_x -= dt

class tuberiasCreator(object):
    tuberiasList: List['tuberia']

    def __init__(self):
        self.tuberiasList = []
        self.on = True
    
    def die(self):
        self.on = False
    
    def create_tuberias(self, pipeline):
        self.tuberiasList.append(tuberia(pipeline))
    
    def draw(self, pipeline, dx):
        for k in self.tuberiasList:
            k.drawn(pipeline, dx*self.tuberiasList.index(k))
    
    def update(self, dt):
        #mueve las tuverias hacia la izquierda
        for k in self.tuberiasList:
            k.update(dt)
    
    def delete(self, d):
        if len(d) == 0:
            return
        remain_tuberias = []
        for k in self.tuberiasList:
            if k not in d:
                remain_tuberias.append(k)
        self.tuberiasList = remain_tuberias
    
#el fondo del juego
"""def create_skybox(pipeline):
    shapeSkybox = bs.createTextureCube()
    gpuSkybox = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuSkybox)
    gpuSkybox.fillBuffers(shapeSkybox.vertices, shapeSkybox.indices, GL_STATIC_DRAW)
    gpuSkybox.texture = es.textureSimpleSetup(getAssetPath("nombre del archivo"),GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    skybox = sg.SceneGraphNode("skybox")
    skybox.transform = tr.matmul([tr.translate(0,0,0.3), tr.uniformScale(2)])#puede ser que sea nesesario cambiar los valores numericos
    skybox.childs += [gpuSkybox]

    return skybox

def create_floor(pipeline):
    shapeFloor = bs.createTextureQuad(8,8)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)
    gpuFloor.texture = es.textureSimpleSetup(getAssetPath("nommbre del archivo"),GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    floor = sg.SceneGraphNode("floor")
    floor.transform = tr.matmul([tr.translate(0,0,0), tr.scale(2,2,1)])#puede sere que sea nesesario cambiar los numeros
    floor.childs += [gpuFloor]

def create_sky(pipeline):
    shapeSky = bs.createTextureQuad(8,8)
    gpuSky = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuSky)
    gpuSky.fillBuffers(shapeSky.vertices, shapeSky.indices, GL_STATIC_DRAW)
    gpuSky.texture = es.textureSimpleSetup(getAssetPath("nommbre del archivo"),GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    floor = sg.SceneGraphNode("floor")
    floor.transform = tr.matmul([tr.translate(0,2,0), tr.scale(2,2,1)])#puede sere que sea nesesario cambiar los numeros
    floor.childs += [gpuSky]"""







