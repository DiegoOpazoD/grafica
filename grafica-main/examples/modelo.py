"""
Este archivo generaría todos los modelos que tiene la aplicación. En programas más complicados
tendríamos una cosa así:

src/models/actor/chansey.py
src/models/actor/egg.py
src/models/factory/eggcreator.py

...
Y este archivo sería algo como
src/models/model.py --> sólo importaría los objetos que usa el resto de la aplicación, sin tocar el detalle mismo

from src.models.actor.chansey import Chansey
from src.models.actor.factory import EggCreator
...

Pero aquí, como nuestra app es sencilla, definimos todas las clases aquí mismo.
1. Chansey
2. Los huevos
"""

import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es

from OpenGL.GL import glClearColor, GL_STATIC_DRAW
import random
from typing import List


def create_gpu(shape, pipeline):
    gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpu)
    gpu.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpu


class Chansey(object):

    def __init__(self, pipeline):
        # Figuras básicas
        gpu_body_quad = create_gpu(bs.createColorQuad(1, 0.8, 0.8), pipeline)  # rosado
        gpu_leg_quad = create_gpu(bs.createColorQuad(1, 0.5, 1), pipeline)  # rosado fuerte
        gpu_eye_quad = create_gpu(bs.createColorQuad(1, 1, 1), pipeline)  # blanco

        body = sg.SceneGraphNode('body')
        body.transform = tr.uniformScale(1)
        body.childs += [gpu_body_quad]

        # Creamos las piernas
        leg = sg.SceneGraphNode('leg')  # pierna generica
        leg.transform = tr.scale(0.25, 0.25, 1)
        leg.childs += [gpu_leg_quad]

        # Izquierda
        leg_izq = sg.SceneGraphNode('legLeft')
        leg_izq.transform = tr.translate(-0.5, -0.5, 0)  # tr.matmul([])..
        leg_izq.childs += [leg]

        leg_der = sg.SceneGraphNode('legRight')
        leg_der.transform = tr.translate(0.5, -.5, 0)
        leg_der.childs += [leg]

        # Ojitos
        eye = sg.SceneGraphNode('eye')
        eye.transform = tr.scale(0.25, 0.25, 1)
        eye.childs += [gpu_eye_quad]

        eye_izq = sg.SceneGraphNode('eyeLeft')
        eye_izq.transform = tr.translate(-0.3, 0.5, 0)
        eye_izq.childs += [eye]

        eye_der = sg.SceneGraphNode('eyeRight')
        eye_der.transform = tr.translate(0.3, 0.5, 0)
        eye_der.childs += [eye]

        # Ensamblamos el mono
        mono = sg.SceneGraphNode('chansey')
        mono.transform = tr.matmul([tr.scale(0.4, 0.4, 0), tr.translate(0, -1.25, 0)])
        mono.childs += [body, leg_izq, leg_der, eye_izq, eye_der]

        transform_mono = sg.SceneGraphNode('chanseyTR')
        transform_mono.childs += [mono]

        self.model = transform_mono
        self.pos = 0  # -1, 0, 1
        self.x = 0  # Variable que indica la posicion visual de chansey (-0.7, 0.7)
        self.alive = True

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

    def modifymodel(self):
        # Transforma la geometria del modelo segun las variables internas
        # Podria ser una funcion hiper gigante
        self.model.transform = tr.translate(self.x, 0, 0)

    def update(self, dt):
        """
        Modifica x tal que satisfaga las constantes internas del modelo.
        x-->f(dt,self.pos)
        dt: incrementar/decrementar la variable (+sumo, -resto) *2dt, 3dt....
        self.pos ---> -1 ---> x->0.7
        self.pos ---> 0 ----> x =0
        self.pos ---> 1---->x = 0.7
        """
        dt *= 10
        if self.pos == 1:
            self.x += dt  # no lineal, cos(...)
            if self.x > 0:
                self.x = min(0.7, self.x)
        elif self.pos == 0:
            if abs(self.x) < 0.05:
                self.x = 0
            else:
                if self.x < 0:
                    self.x += dt
                elif self.x > 0:
                    self.x -= dt
        elif self.pos == -1:
            self.x -= dt
            self.x = max(-0.7, self.x)
        # modificar de manera constante al modelo
        # aqui deberia llamar a tr.translate
        self.modifymodel()

    def move_left(self):
        if not self.alive:
            return
        self.pos = -1

    def move_right(self):
        if not self.alive:
            return
        self.pos = 1

    def move_center(self):
        if not self.alive:
            return
        self.pos = 0

    def collide(self, eggs: 'EggCreator'):
        if not eggs.on:  # Si el jugador perdió, no detecta colisiones
            return

        deleted_eggs = []
        for e in eggs.eggs:
            if e.pos_y < -0.7 and e.pos_x != self.pos:
                print('MUERE, GIT GUD')  # YOU D   I   E   D, GIT GUD
                """
                En este caso, podríamos hacer alguna pestaña de alerta al usuario,
                cambiar el fondo por alguna textura, o algo así, en este caso lo que hicimos fue
                cambiar el color del fondo de la app por uno rojo.
                """
                eggs.die()  # Básicamente cambia el color del fondo, pero podría ser algo más elaborado, obviamente
                self.alive = False
            elif -0.25 >= e.pos_y >= -0.7 and self.pos == e.pos_x:
                # print('COLISIONA CON EL HUEVO')
                deleted_eggs.append(e)
        eggs.delete(deleted_eggs)


class Egg(object):

    def __init__(self, pipeline):
        gpu_egg = create_gpu(bs.createColorQuad(0.7, .7, .7), pipeline)

        egg = sg.SceneGraphNode('egg')
        egg.transform = tr.scale(0.1, 0.2, 1)
        egg.childs += [gpu_egg]

        egg_tr = sg.SceneGraphNode('eggTR')
        egg_tr.childs += [egg]

        self.pos_y = 1
        self.pos_x = random.choice([-1, 0, 1])  # LOGICA
        self.model = egg_tr

    def draw(self, pipeline):
        self.model.transform = tr.translate(0.7 * self.pos_x, self.pos_y, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def update(self, dt):
        self.pos_y -= dt


class EggCreator(object):
    eggs: List['Egg']

    def __init__(self):
        self.eggs = []
        self.on = True

    def die(self):  # DARK SOULS
        glClearColor(1, 0, 0, 1.0)  # Cambiamos a rojo
        self.on = False  # Dejamos de generar huevos, si es True es porque el jugador ya perdió

    def create_egg(self, pipeline):
        if len(self.eggs) >= 10 or not self.on:  # No puede haber un máximo de 10 huevos en pantalla
            return
        if random.random() < 0.01:
            self.eggs.append(Egg(pipeline))

    def draw(self, pipeline):
        for k in self.eggs:
            k.draw(pipeline)

    def update(self, dt):
        for k in self.eggs:
            k.update(dt)

    def delete(self, d):
        if len(d) == 0:
            return
        remain_eggs = []
        for k in self.eggs:  # Recorro todos los huevos
            if k not in d:  # Si no se elimina, lo añado a la lista de huevos que quedan
                remain_eggs.append(k)
        self.eggs = remain_eggs  # Actualizo la lista
