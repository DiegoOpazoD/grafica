
#contorlador

from modeloTrarea import *
import glfw
import sys
from typing import Union


class Controller(object):
    model: Union["bird", None]
    tuberias: Union["TuberiasCreator", None]
    GameO: Union["GameOver", None]
    win: Union["PantallaGanar", None]
    fondo1: Union["Fondo1", None]
    fondo2: Union["Fondo2", None]

    def __init__(self):
        self.model = None
        self.tuberias = None
        self.Suelo = None
        self.GameO = None
        self.win = None
        self.fondo1 = None
        self.fondo2 = None
        self.colicion = False
    
    def set_model(self, m):
        self.model = m
    
    def set_tuberias(self, e):
        self.tuberias = e
    
    def set_GameO(self, g):
        self.GameO = g
    
    def set_win(self, w):
        self.win = w
    
    def set_fondo1(self, f1):
        self.fondo1 = f1
    
    def set_fondo2(self, f2):
        self.fondo2 = f2

    
    def on_key(self, window, key, scancode, action, mods):
        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return
        
        if key == glfw.KEY_ESCAPE:
            sys.exit()
        
        elif key == glfw.KEY_UP and action == glfw.PRESS:
            self.model.move_up()
            
        else:
            print("Unknown key")
