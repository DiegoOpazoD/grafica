#ControladorTarea3D

from ModeloTarea3D import *
import glfw
import sys
from typing import Union

LIGHT_FLAT = 0

class Controller(object):
    tuberias: Union["tuberiasCreator", None]


    def __init__(self):
        self.tuberias = None
        #lights
        self.lightModel = LIGHT_FLAT
        #muestra el axis
        self.showAxis = True
        
        self.fillPolygon = True
    
    def set_tuberias(self,e):
        self.tuberias = e

    def on_key(self, window, key, scancode, action, mods):
        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return
        
        if key == glfw.KEY_ESCAPE:
            sys.exit()
        