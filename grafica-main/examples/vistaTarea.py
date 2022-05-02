
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

    #trasparencia
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    pajaro = bird(pipeline)
    tubos = TuberiasCreator()
    win = PantallaGanar(pipeline)
    fondo1 = Fondo1(pipeline)
    fondo2 = Fondo2(pipeline)
    GameO = GameOver(pipeline)


    controlador.set_model(pajaro)
    controlador.set_tuberias(tubos)
    controlador.set_win(win)
    controlador.set_fondo1(fondo1)
    controlador.set_fondo2(fondo2)
    controlador.set_GameO(GameO)

    #crear texturas con los caracteres
    textBitsTexture = tx.generateTextBitsTexture()
    #mover las texturas a la gpu
    gpuText3DTexture = tx.toOpenGLTexture(textBitsTexture)


    # contador en pantalla
    textpipeline = tx.TextureTextRendererShaderProgram()
    headerText = "N"
    headerCharSize = 0.1
    headerCenterX = headerCharSize * len(headerText) / 2
    headershape = tx.textToShape(headerText, headerCharSize, headerCharSize)
    gpuHeader= es.GPUShape().initBuffers()
    textpipeline.setupVAO(gpuHeader)
    gpuHeader.fillBuffers(headershape.vertices, headershape.indices, GL_STATIC_DRAW)
    gpuHeader.texture = gpuText3DTexture
    headerTransform = tr.translate(0, 0, 0)



    #crea las tuberias
    for i in range(0,Nmax+2):
        tubos.create_tuberia(pipeline)

    t0 = 0
    while not glfw.window_should_close(window):

        ti = glfw.get_time()
        dt = ti - t0
        t0 = ti


        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)


        #glUseProgram(textpipeline.shaderProgram)
        #glUniform4f(glGetUniformLocation(textpipeline.shaderProgram, "fontColor"), 1,1,1,0)
        #glUniform4f(glGetUniformLocation(textpipeline.shaderProgram, "backColor"), 0,0,0,1)
        #glUniformMatrix4fv(glGetUniformLocation(textpipeline.shaderProgram, "transform"), 1, GL_TRUE, headerTransform)
        textpipeline.drawCall(gpuHeader)

        for i in range(0,len(tubos.tuberias)):
            if i == 0:
                tubos.tuberias[i].update(0.5*dt)

            else:
                if tubos.tuberias[i-1].pos_x < 0:
                    tubos.tuberias[i].update(0.5*dt)
                       
           

        fondo1.drawn(pipeline)
        fondo1.update(0.25*dt)
        if fondo1.pos_x < -2:
            fondo1.pos_x = 2
        
        fondo2.drawn(pipeline)
        fondo2.update(0.25*dt)
        if fondo2.pos_x < -2:
            fondo2.pos_x = 2

        pajaro.draw(pipeline)
        pajaro.update(0.75*dt)
        pajaro.collide(tubos)

        tubos.draw(pipeline, 1)


        for i in tubos.tuberias:
            if abs(pajaro.pos - i.pos_x) <0.025:
                if areColliding(pajaro,i):
                    pajaro.alive = False

        if not pajaro.alive:
            GameO.draw(pipeline)

        if pajaro.victoria == True:
            win.drawn(pipeline)
        

        glfw.swap_buffers(window)
    
    glfw.terminate()




    
