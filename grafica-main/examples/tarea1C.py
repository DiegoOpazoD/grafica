
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
import sira

sys.argv
print(sys.argv[0])
# numeros de la cuadricula sys.argv[1]
# archivo pallete.json sys.argv[2]
    # tengo que poder transformar de rgb en porcentaje 0-1 a rgb en base 255
# sys.argv[3] nombre como lo quiero guardar

if __name__ == "__main__":

    #windowSize = (600,600)

    S = 50
    W = 16 + 6 #sys.argv[1]
    H = 16 #sys.argv[1]
    windowSize = (W*S, H*S)

    colorPalette = np.ndarray((4,3), dtype=np.uint8)
    colorPalette[0] = np.array([255,0,50], dtype=np.uint8)
    colorPalette[1] = np.array([59,59,59], dtype=np.uint8)

    imgData = np.ndarray((W,H), dtype = np.uint8)
    imgData[:,0:16] = 0
    imgData[16:22] = 1
    imgData[16:22] 

    display = sira.IndirectRGBRasterDisplay(windowSize, (W,H),"Indirect RGB Raster Display")
    display.setColorPalette(colorPalette)
    display.setMatrix(imgData)


    blueQuad = bs.createColorQuad(0,0,1)

    def createGPUColorQuad(r,g,b):
       shapeQuad = bs.createColorQuad(r,g,b)
       gpuQuad = es.GPUShape().initBuffers()
       pipeline.setupVAO(gpuQuad)
       gpuQuad.fillBuffers(shapeQuad.vertices, shapeQuad.indices, GL_STATIC_DRAW)
       return gpuQuad

    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

    t0 = glfw.get_time()
    while not glfw.window_should_close(window):
        t1 = glfw.get_time
        dt = t1 - t0
        t0 = t1

        glfw.poll_events()
        
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
    display.draw()

        




