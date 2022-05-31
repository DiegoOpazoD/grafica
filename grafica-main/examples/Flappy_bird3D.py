#Flappy_bird3D

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
from ModeloTarea3D import *
from ControladorTarea3D import Controller
import numpy as np

if __name__ == "__main__":
    if not glfw.init():
        glfw.set_window_should_close(window, True)
    
    width = 600
    height = 600

    window = glfw.create_window(width, height, "Flappy_bird", None, None)

    if not window:
        glfw.terminate()
        glfw.make_context_current(window, True)

    #we will use the global controller as communication with the callback function
    controlador = Controller()
    
    glfw.make_context_current(window)

    glfw.set_key_callback(window, Controller.on_key)

    #diferentes shader programs para diferentes iluminaciones, despues elije una
    #flatpipeline = ls.SimpleFlatShaderProgram()
    #gourdaudipeline = ls.SimpleGouraudShaderProgram()
    pipeline = ls.SimplePhongShaderProgram()
    #este shader no considera iluminacion
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    #color de la pantalla
    glClearColor(0.15,0.15,0.15,1.0)

    #que parte esta adelante y cual atras
    glEnable(GL_DEPTH_TEST)

    t0 = glfw.get_time()
    camera_theta = np.pi/4

    #modelos
    
    #axis
    gpuAxis = createGPUShape(bs.createAxis(4), mvpPipeline)

    tubos = tuberia(pipeline)

    controlador.set_tuberias(tubos)

    while not glfw.window_should_close(window):

        #Se usa GLFW para ver si hay input events
        glfw.poll_events()

        if (controlador.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        #toma la diferencia de timepo entre iteracions
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        #despejando la escena tanto de color y profundidad
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #camera

        projection = tr.ortho(-1, 1, -1, 1, 0.1, 100)
        projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

        camX = 3 * np.sin(camera_theta)
        camY = 3 * np.cos(-camera_theta)

        camX2 = 3 * np.sin(camera_theta*2)
        camY2 = 3 * np.cos(camera_theta*2)

        viewPos = np.array([0,camY,2]) #detras del personaje
        viewPos = np.array([camX2,camY2,0]) #modo 2d 

        viewPos = np.array([2,2,2])

        view = tr.lookAt(
            viewPos,
            np.array([0,0,0]),
            np.array([0,0,1])
        )

        axis = np.array([1,-1,1])
        #axis = np.array([0,0,1])
        axis = axis / np.linalg.norm(axis)
        model = tr.identity()

        #se dibuja el axis sin efectos de luz
        if controlador.showAxis:
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawCall(gpuAxis, GL_LINES)

        #lights

        glUseProgram(pipeline.shaderProgram)

        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

        # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.6, 0.6, 0.6)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.5, 0.7, 0.7)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

        
        # White light in all components: ambient, diffuse and specular. #luz de noche
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 0.2, 0.4, 0.6)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 0.2, 0.4, 0.6)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 0.2, 0.4, 0.6)

                # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.9)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)


        #lo se arriva se cambia para cmabiar las luces

        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), -5, -5, 5)
        glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 100)
        
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, model)



        #se dibujan las figuras
        tubos.drawn(pipeline)



        glfw.swap_buffers(window)

        #print(tubos.pos_x)
    glfw.terminate()