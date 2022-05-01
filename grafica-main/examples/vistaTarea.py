
#vistaTarea

import glfw
import sys
from OpenGL.GL import *
import OpenGL.GL.shaders
from modeloTrarea import *
from controladorTrarea import Controller
import grafica.text_renderer as tx

if __name__ == "__main__":

    if not glfw.init():
        sys.exit()
    
    widht = 600
    height = 600

    window = glfw.create_window(widht, height, "Ufo", None, None)

    if not window:
        glfw.terminate()
        sys.exit()
    
    glfw.make_context_current(window)

    controlador = Controller()
    
    glfw.set_key_callback(window, controlador.on_key)

    pipeline = es.SimpleTextureTransformShaderProgram()
    

    glUseProgram(pipeline.shaderProgram)

    glClearColor(0.1, 0.1, 0.1, 1.0)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    pajaro = bird(pipeline)
    tubos = TuberiasCreator()
    win = PantallaGanar(pipeline)
    #GameO = GameOver(pipeline)


    controlador.set_model(pajaro)
    controlador.set_tuberias(tubos)
    controlador.set_win(win)
    #controlador.set_GameO(GameO)

     #crear texturas con los caracteres
    textBitsTexture = tx.generateTextBitsTexture()
    #mover las texturas a la gpu
    gpuText3DTexture = tx.toOpenGLTexture(textBitsTexture)

    # contador en pantalla
    textpipeline = tx.TextureTextRendererShaderProgram()
    contador = "N"
    CharSize = 0.1
    headershape = tx.textToShape(contador, CharSize, CharSize)
    gpuHeader= es.GPUShape().initBuffers()
    textpipeline.setupVAO(gpuHeader)
    gpuHeader.fillBuffers(headershape.vertices, headershape.indices, GL_STATIC_DRAW)
    gpuHeader.texture = gpuText3DTexture
    headerTransform = tr.translate(0, 1, 0)



    #fondo
    backgroundShape = bs.createTextureQuad(1,1)
    bs.scaleVertices(backgroundShape, 5, [2,2,1])
    gpuBackground = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBackground)
    gpuBackground.fillBuffers(backgroundShape.vertices, backgroundShape.indices, GL_STATIC_DRAW)
    gpuBackground.texture = es.textureSimpleSetup(
        getAssetPath("torres-del-paine-sq.jpg"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)


    #trasparencia
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    t0 = 0

    while not glfw.window_should_close(window):

        ti = glfw.get_time()
        dt = ti - t0
        t0 = ti


        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        #fondo
        glUseProgram(pipeline.shaderProgram)
        pipeline.drawCall(gpuBackground)

        """glUseProgram(textpipeline.shaderProgram)
        glUniform4f(glGetUniformLocation(textpipeline.shaderProgram, "fontColor"), 1,1,1,0)
        glUniform4f(glGetUniformLocation(textpipeline.shaderProgram, "backColor"), 0,0,0,1)
        glUniformMatrix4fv(glGetUniformLocation(textpipeline.shaderProgram, "transform"), 1, GL_TRUE, headerTransform)
        textpipeline.drawCall(gpuHeader)"""

        tubos.create_tuberia(pipeline, ti)
        tubos.update(0.5*dt)
        
        pajaro.update(0.75*dt)
        pajaro.collide(tubos)

        pajaro.draw(pipeline)

        tubos.draw(pipeline, 1)
        
        #Suelo.draw(pipeline)

        for i in tubos.tuberias:
            if abs(pajaro.pos - i.pos_x) <0.025:
                if areColliding(pajaro,i):
                    pajaro.alive = False

        if not pajaro.alive:
            #GameO.draw(pipeline)
            print("perdiste")
            sys.exit()
        if pajaro.victoria == True:
            win.drawn(pipeline)

        glfw.swap_buffers(window)
    
    glfw.terminate()




    
