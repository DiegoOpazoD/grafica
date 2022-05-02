
#modelo
from turtle import shape
from grafica.assets_path import getAssetPath
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import sys ,os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np

from OpenGL.GL import *
import random
from typing import List


array = sys.argv
#Nmax = array[1]
Nmax = 10 
N = 0

#ubicacion de las texturas
thisFilePath = os.path.abspath(__file__)
thisFolderPath = os.path.dirname(thisFilePath)
spritesDirectory = os.path.join(thisFolderPath, "texturas")
spritePathUfo = os.path.join(spritesDirectory, "ufo.png")

thisFilePath = os.path.abspath(__file__)
thisFolderPath = os.path.dirname(thisFilePath)
spritesDirectory = os.path.join(thisFolderPath, "texturas")
spritePathTArriba = os.path.join(spritesDirectory, "tuberiaArriba.png")


def create_gpu(shape, pipeline):
    gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpu)
    gpu.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpu

def create_gpu2(shape,pipeline):
    bs.scaleVertices(shape,5,[2,2,1])
    gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpu)
    gpu.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpu


class bird(object):

    def __init__(self, pipeline):
        gpu_body_quad = create_gpu(bs.createTextureQuad(1,1),pipeline)
        gpu_body_quad.texture = es.textureSimpleSetup(spritePathUfo, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)


        body = sg.SceneGraphNode("body")

        body.transform = tr.uniformScale(0.25)
        body.childs += [gpu_body_quad]

        eye = sg.SceneGraphNode("eye")
        eye.transform = tr.scale(0.125,0.125,0.5)
 
        personaje = sg.SceneGraphNode("bird")
        personaje.transform = tr.matmul([tr.scale(0.4, 0.4, 0), tr.translate(-0.7, 1, 0)])
        personaje.childs += [body, eye]

        transform_personaje = sg.SceneGraphNode("birdTR")
        transform_personaje.childs += [personaje]

        self.model = transform_personaje
        self.pos = -0.25
        self.y = 0.75
        self.alive = True
        self.victoria = False
        self.pasoTuberia = False
    
    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
    
    def modifymodel(self):
        # Trasforma la geometria del modelo segun las variables internas
        self.model.transform = tr.translate(self.pos,self.y,0)
    
    def update(self, dt):
        #actualiza las posicion del modelo cada instante
        self.y -= 0.5*dt
        self.modifymodel()

    def move_up(self):
        if not self.alive:
            return
        self.y += 0.15
    
    def collide(self, tuberias: "TuberiasCreator"):
        deleted_tubos = []

        for t in tuberias.tuberias:
            self.pasoTuberia = False
            #Elimina tuberias despues de pasar cierta posicion y añade un 1 al contador
            if t.pos_x < -1.3:
                deleted_tubos.append(t)
  
            elif -0.301 < t.pos_x < -0.3:
                global N
                N += 1
                if N == Nmax:
                    self.victoria = True

            #Detecta las colicions con el "techo" y en el "suelo"
            elif self.y > 1.3 or self.y < -1.3:
                self.alive = False

        tuberias.delete(deleted_tubos)


def areColliding(pa: "bird", tubos: "Tubo"):
    #Detecta coliciones con los tubos
    return pa.y + 0.25> tubos.borde_arriba - 0.1 or pa.y + 0.25 < tubos.borde_abajo - 0.1 


class Tubo(object):

    def __init__(self, pipeline):
        gpu_tubo = create_gpu(bs.createTextureQuad(1,1), pipeline)
        gpu_tubo.texture = es.textureSimpleSetup(spritePathTArriba, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)


        tubo = sg.SceneGraphNode("tubo")
        a = random.randint(20,250)
        tubo.transform = tr.scale(0.25,a/100,1)
        tubo.childs += [gpu_tubo]

        tubo_ar = sg.SceneGraphNode("tuboArriva")
        tubo_ar.childs += [tubo]

        tubo_ab = sg.SceneGraphNode("tuboAbajo")
        h = a/100 + 0.5 + 4.5*(a/100)
        tubo_ab.transform = tr.matmul([tr.translate(0,-h,0),tr.scale(1,-10,1)])
        tubo_ab.childs += [tubo]

        parTubos = sg.SceneGraphNode("Partubos")
        parTubos.childs = [tubo_ar, tubo_ab]

        self.model = parTubos
        self.pos_x = 1.5
        self.pos_y = 1
        self.borde_arriba = self.pos_y - a/200
        self.borde_abajo = self.pos_y - h + 10*a/200
        

    def drawn(self, pipeline, dx):
        #self.pos_x += dx
        self.model.transform = tr.translate(self.pos_x, self.pos_y, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def update(self, dt):
        self.pos_x -= dt


class TuberiasCreator(object):
    tuberias: List['Tubo']

    def __init__(self):
        self.tuberias = []
        self.on = True

    def die(self):
        self.on = False

    def create_tuberia(self, pipeline):
        self.tuberias.append(Tubo(pipeline))

    def draw(self, pipeline, dx):
        for k in self.tuberias:
            k.drawn(pipeline, dx*self.tuberias.index(k))

    def update(self, dt):
        #Mueve las tuberias hacia la izquierda
        for k in self.tuberias:
            k.update(dt)

    def delete(self, d):
        if len(d) == 0:
            return
        remain_tuberias = []
        for k in self.tuberias:
            if k not in d:
                remain_tuberias.append(k)
        self.tuberias = remain_tuberias


#lugar de la imagen
thisFilePath = os.path.abspath(__file__)
thisFolderPath = os.path.dirname(thisFilePath)
spritesDirectory = os.path.join(thisFolderPath, "texturas")
spritePathGameOver = os.path.join(spritesDirectory, "gameover.jpg")

#pantalla que aparece cuando pierdes
class GameOver(object):

    def __init__(self, pipeline):
        gpu_GameO = create_gpu(bs.createTextureQuad(1,1), pipeline)
        gpu_GameO.texture = es.textureSimpleSetup(
            spritePathGameOver, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST)

        GameO = sg.SceneGraphNode("GameOver")
        GameO.transform = tr.uniformScale(2.5)
        GameO.childs += [gpu_GameO]

        self.model = GameO

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")



#
thisFilePath = os.path.abspath(__file__)
thisFolderPath = os.path.dirname(thisFilePath)
spritesDirectory = os.path.join(thisFolderPath, "texturas")
spritePathWin = os.path.join(spritesDirectory, "ganaste.jpg")

class PantallaGanar(object):
    def __init__(self, pipeline):
        gpu_win = create_gpu(bs.createTextureQuad(1,1), pipeline)
        gpu_win.texture = es.textureSimpleSetup(
            spritePathWin, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST
        )
        win = sg.SceneGraphNode("winscreen")
        win.transform = tr.uniformScale(2.5)
        win.childs += [gpu_win]

        self.model = win

    def drawn(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "transform")


# fondo del juego
thisFilePath = os.path.abspath(__file__)
thisFolderPath = os.path.dirname(thisFilePath)
spritesDirectory = os.path.join(thisFolderPath, "texturas")
spritePathFondo = os.path.join(spritesDirectory, "fondo4.jpg")

class Fondo1(object):
    def __init__(self, pipeline):
        shapefondo1 = bs.createTextureQuad(1,1)
        gpu_fondo1 = create_gpu2(shapefondo1, pipeline)
        gpu_fondo1.texture = es.textureSimpleSetup(
           spritePathFondo, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST 
        )
        fondo1 = sg.SceneGraphNode("Fondo1")
        fondo1.transform = tr.uniformScale(2.5)
        fondo1.childs += [gpu_fondo1]

        self.model = fondo1
        self.pos_x = 0

    
    def drawn(self, pipeline):
        self.model.transform = tr.translate(self.pos_x,0,0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
    
    def update(self, dt):
        self.pos_x -= dt

class Fondo2(object):
    def __init__(self, pipeline):
        shapefondo2 = bs.createTextureQuad(1,1)
        gpu_fondo2 = create_gpu2(shapefondo2, pipeline)
        gpu_fondo2.texture = es.textureSimpleSetup(
           spritePathFondo, GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_NEAREST, GL_NEAREST 
        )
        fondo2 = sg.SceneGraphNode("Fondo1")
        fondo2.transform = tr.scale(2,2,2)
        
        fondo2.childs += [gpu_fondo2]

        self.model = fondo2
        self.pos_x = 2

    
    def drawn(self, pipeline):
        self.model.transform = tr.translate(self.pos_x,0,0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")
    
    def update(self, dt):
        self.pos_x -= dt






















