#librarys

import glm
import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr

#classes

from entity import Entity, Square, Cube, Sphere
from texture import Texture

class App:

    def __init__(self):

        #initializing python display
        pg.init()

        #add multi-sampling support
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 8) 

        #display customization
        pg.display.set_mode((1000, 750), pg.OPENGL|pg.DOUBLEBUF)
        pg.display.set_caption("Solar system animation")

        self.clock = pg.time.Clock()

        #activating multi-sampling
        glEnable(GL_MULTISAMPLE)

        #initializing openGL
        glClearColor(0, 0, 0, 1)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

        #creating a shader
        self.shader = self.createShader("phong/vertex.txt", "phong/fragment.txt")

        #initializing all meshes for the scene

        self.entities = []

        self.background = Cube(
            [0, 0, 0],
            [0, 0, 0]
        )
            
        self.entities.append(self.background)

        self.stars = Cube(
            [0, 0, 0],
            [0, 0, 0]
        )
            
        self.entities.append(self.stars)
            
        self.mercury = Sphere(
            [0, 0, -5],
            [0, 0, 0]
        )
            
        self.entities.append(self.mercury)
            
        self.venus = Sphere(
            [5, 1, -10],
            [0, 0, 0]
        )
            
        self.entities.append(self.venus)

        self.earth = Sphere(
            [-5, 2, -15],
            [0, 0, 0]
        )
            
        self.entities.append(self.earth)

        #moon position is moon-earth radius

        self.moon = Sphere(
            [0, 0, 2],
            [0, 0, 0]
        )
            
        self.entities.append(self.moon)

        self.mars = Sphere(
            [-10, 3, -20],
            [0, 0, 0]
        )
            
        self.entities.append(self.mars)

        self.jupiter = Sphere(
            [10, 4, -25],
            [0, 0, 0]
        )
            
        self.entities.append(self.jupiter)

        self.saturn = Sphere(
            [-10, 5, -30],
            [0, 0, 0]
        )
            
        self.entities.append(self.saturn)

        self.ring = Square(
            [-10, 5, -30],
            [95, 0, 0]
        )

        self.entities.append(self.ring)

        self.uranus = Sphere(
            [15, 6, -35],
            [0, 0, 0]
        )
            
        self.entities.append(self.uranus)

        self.neptune = Sphere(
            [20, 7, -40],
            [0, 0, 0]
        )
            
        self.entities.append(self.neptune)

        #initializing projection matrix

        self.projection = pyrr.matrix44.create_perspective_projection(
            fovy = 45, aspect = 1000/750,
            near = 0.1, far = 100, dtype=np.float32

            #graphic model becomes inaccurate for big far values???
        )

        #initializing all textures used for the scene
        self.textures = []

        self.earth_tex = Texture("textures/earth.jpg")
        self.textures.append(self.earth_tex)

        self.stars_tex = Texture("textures/stars.jpg")
        self.textures.append(self.stars_tex)

        self.jupiter_tex = Texture("textures/jupiter.jpg")
        self.textures.append(self.jupiter_tex)

        self.mars_tex = Texture("textures/mars.jpg")
        self.textures.append(self.mars_tex)

        self.mercury_tex = Texture("textures/mercury.jpg")
        self.textures.append(self.mercury_tex)

        self.neptune_tex = Texture("textures/neptune.jpg")
        self.textures.append(self.neptune_tex)

        self.saturn_tex = Texture("textures/saturn.jpg")
        self.textures.append(self.saturn_tex)

        self.uranus_tex = Texture("textures/uranus.jpg")
        self.textures.append(self.uranus_tex)

        self.venus_tex = Texture("textures/venus.jpg")
        self.textures.append(self.venus_tex)

        self.ring_tex = Texture("textures/ring.png")
        self.textures.append(self.ring_tex)

        self.moon_tex = Texture("textures/moon.jpg")
        self.textures.append(self.moon_tex)

        self.more_stars_tex = Texture("textures/more_stars.png")
        self.textures.append(self.more_stars_tex)

        self.mainLoop()


    def createShader(self, vertexFilePath, fragmentFilePath):

        """
            Creates a new shader using path.
        """

        with open(vertexFilePath, 'r') as f:
            vertex_src = f.readlines()
        
        with open(fragmentFilePath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader


    def mainLoop(self):
        
        running = True
        camera_eulers = [0, 0, 0]

        while (running):

            #checking events

            keys = pg.key.get_pressed()

            if (keys[pg.K_UP]):
                camera_eulers[0] -= 1

            if (keys[pg.K_DOWN]):
                camera_eulers[0] += 1

            if (keys[pg.K_LEFT]):
                camera_eulers[1] -= 1

            if (keys[pg.K_RIGHT]):
                camera_eulers[1] += 1

            for event in pg.event.get():

                if (event.type == pg.QUIT):
                    running = False
            
                    

            #refreshing screen

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            #refreshing view matrix
            camera_position = glm.vec3(0, 0, 0)
            camera_target = glm.vec3(0, 0, -5)
            camera_up = glm.vec3(0.0, 1.0, 0.0)
            self.view = glm.lookAt(camera_position, camera_target, camera_up)
            self.view = np.array(self.view, dtype=np.float32)

            self.view = pyrr.matrix44.multiply(
            m1=self.view, 
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis = [0, 1, 0],
                theta = np.radians(camera_eulers[1]), 
                dtype = np.float32))
            
            self.view = pyrr.matrix44.multiply(
            m1=self.view, 
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis = [1, 0, 0],
                theta = np.radians(camera_eulers[0]), 
                dtype = np.float32))
            
            #SCENE START

            glUseProgram(self.shader)

            #static uniforms
            glUniformMatrix4fv(glGetUniformLocation(self.shader, "projection"), 1, GL_FALSE, self.projection)
            glUniform1i(glGetUniformLocation(self.shader, "tex"), 0)

            lightPos = [0, 10, 0]
            lightPos = np.array(lightPos, dtype=np.float32)
            glUniform3fv(glGetUniformLocation(self.shader, "lightPos"), 1, lightPos)

            lightColor = [1, 1, 1]
            lightColor = np.array(lightColor, dtype=np.float32)
            glUniform3fv(glGetUniformLocation(self.shader,  "lightColor"), 1, lightColor)
            

            # BACKGROUND

            self.transform(self.background, 50)

            self.setLight(1, 0, [1, 1, 1])
            self.stars_tex.use()
            self.draw(self.background)

            #adding stars

            self.stars.eulers[1] += 0.002
            if self.stars.eulers[1] >= 360:
                self.stars.eulers[1] = 0

            self.transform(self.stars, 45)

            self.setLight(0.9, 0, [1, 1, 1])
            self.more_stars_tex.use()
            self.draw(self.stars)

            
            #MERCURY prograde

            self.mercury.eulers[1] += 1
            if self.mercury.eulers[1] >= 360:
                self.mercury.eulers[1] = 0

            self.transform(self.mercury, 0.3)

            self.setLight(0.2, 0, [1, 1, 0.95])
            self.mercury_tex.use()
            self.draw(self.mercury)
            
            #VENUS retrograde

            self.venus.eulers[1] -= 0.7
            if self.venus.eulers[1] <= -360:
                self.venus.eulers[1] = 0

            self.transform(self.venus, 0.9)

            self.venus_tex.use()
            self.draw(self.venus)

            #EARTH prograde

            self.earth.eulers[1] += 0.5
            if self.earth.eulers[1] >= 360:
                self.earth.eulers[1] = 0

            self.transform(self.earth, 1)

            #trying to achieve glossy earth
            self.setLight(0.2, 1, [1, 1, 0.95])

            self.earth_tex.use()
            self.draw(self.earth)

            #MARS prograde

            self.mars.eulers[1] += 0.4
            if self.mars.eulers[1] >= 360:
                self.mars.eulers[1] = 0

            self.transform(self.mars, 0.5)


            self.setLight(0.2, 0, [1, 1, 0.95])
            self.mars_tex.use()
            self.draw(self.mars)

            #JUPITER prograde

            self.transform(self.jupiter, 4.5)

            self.jupiter.eulers[1] += 0.25
            if self.jupiter.eulers[1] >= 360:
                self.jupiter.eulers[1] = 0

            self.jupiter_tex.use()
            self.draw(self.jupiter)

            #SATURN prograde

            self.saturn.eulers[1] += 0.2
            if self.saturn.eulers[1] >= 360:
                self.saturn.eulers[1] = 0

            self.transform(self.saturn, 3.5)

            self.saturn_tex.use()
            self.draw(self.saturn)

            #adding saturn ring

            self.ring.eulers[1] += 0.2
            if self.ring.eulers[1] >= 360:
                self.ring.eulers[1] = 0

            self.transform(self.ring, 7)

            self.setLight(0.5, 0, [1, 1, 0.95])
            self.ring_tex.use()
            self.draw(self.ring)

            #URANUS retrograde

            self.uranus.eulers[1] -= 0.1
            if self.uranus.eulers[1] <= -360:
                self.uranus.eulers[1] = 0

            self.transform(self.uranus, 3)

            self.setLight(0.2, 0, [1, 1, 0.95])
            self.uranus_tex.use()
            self.draw(self.uranus)

            #NEPTUNE prograde

            self.neptune.eulers[1] += 0.05
            if self.neptune.eulers[1] >= 360:
                self.neptune.eulers[1] = 0

            self.transform(self.neptune, 3)

            self.neptune_tex.use()
            self.draw(self.neptune)

            #adding a moon to to the Earth
            #not using transform function because it's a more complex transformation

            self.moon.eulers[1] += 1
            if self.moon.eulers[1] >= 360:
                self.moon.eulers[1] = 0

            self.moon.model = pyrr.matrix44.create_identity(dtype=np.float32)

            #moon has a third of the size of the earth
            scale = 0.5*pyrr.matrix44.create_identity(dtype=np.float32)
            scale[3][3] = 1

            self.moon.model = pyrr.matrix44.multiply(
            m1=self.moon.model, 
            m2=scale
            )

            #self-rotation
            self.moon.model = pyrr.matrix44.multiply(
                m1=self.moon.model, 
                m2=pyrr.matrix44.create_from_axis_rotation(
                    axis = [0, 1, 0],
                    theta = np.radians(-self.moon.eulers[1]), 
                    dtype = np.float32))
            
            #translation to radius
            self.moon.model = pyrr.matrix44.multiply(
            m1=self.moon.model, 
            m2=pyrr.matrix44.create_from_translation(
                vec=np.array(self.moon.position),dtype=np.float32
            ))

            #rotation around the Earth
            self.moon.model = pyrr.matrix44.multiply(
                m1=self.moon.model, 
                m2=pyrr.matrix44.create_from_axis_rotation(
                    axis = [0, 1, 0],
                    theta = np.radians(-self.moon.eulers[1]), 
                    dtype = np.float32))
            
            #translation to earth
            self.moon.model = pyrr.matrix44.multiply(
            m1=self.moon.model, 
            m2=pyrr.matrix44.create_from_translation(
                vec=np.array(self.earth.position),dtype=np.float32
            ))

            #rotation around the sun following the Earth
            self.moon.model = pyrr.matrix44.multiply(
                m1=self.moon.model, 
                m2=pyrr.matrix44.create_from_axis_rotation(
                    axis = [0, 1, 0],
                    theta = np.radians(self.earth.eulers[1]), 
                    dtype = np.float32))


            self.moon_tex.use()
            self.draw(self.moon)

            # SCENE END

            pg.display.flip()
        
            #timing
            self.clock.tick(60)

        self.quit()

    def draw(self, entity):

        """
            Draws a mesh on the scene.
        """

        glUseProgram(self.shader)

        #dynamic uniforms
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "view"), 1, GL_FALSE, self.view)
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "model"), 1, GL_FALSE, entity.model)

        entity.draw()


    def setLight(self, ambientStrenght, specularStrenght, objectColor):

        """
            Sets light parameters and the color of rendered object. Needs to be called at least once in the app.
        
        """
        
        objectColor = np.array(objectColor, dtype=np.float32)
        glUniform3fv(glGetUniformLocation(self.shader,  "objectColor"), 1, objectColor)

        glUniform1f(glGetUniformLocation(self.shader, "ambientStrengthUniform"), np.float32(ambientStrenght))
        
        glUniform1f(glGetUniformLocation(self.shader, "specularStrengthUniform"), np.float32(specularStrenght))


        

    def transform(self, entity, size):
        """
            Used to size the planets and make them turn around the Sun and themselves.
        """
        
        entity.model = pyrr.matrix44.create_identity(dtype=np.float32)

        #scaling using the size factor
        scale = size*pyrr.matrix44.create_identity(dtype=np.float32)
        scale[3][3] = 1

        entity.model = pyrr.matrix44.multiply(
            m1=entity.model, 
            m2=scale
        )

        #self-rotation
        entity.model = pyrr.matrix44.multiply(
            m1=entity.model, 
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis = [1, 0, 0],
                theta = np.radians(entity.eulers[0]), 
                dtype = np.float32))

        entity.model = pyrr.matrix44.multiply(
            m1=entity.model, 
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis = [0, 1, 0],
                theta = np.radians(entity.eulers[1]*2), 
                dtype = np.float32))

        #translation
        entity.model = pyrr.matrix44.multiply(
            m1=entity.model, 
            m2=pyrr.matrix44.create_from_translation(
                vec=np.array(entity.position),dtype=np.float32
            ))
        
        #rotation around the y-axis
        entity.model = pyrr.matrix44.multiply(
            m1=entity.model, 
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis = [0, 1, 0],
                theta = np.radians(entity.eulers[1]), 
                dtype = np.float32))

    def quit(self):

        """
            Frees the GPU memory.
        """

        for entity in self.entities:
            entity.destroy()

        for texture in self.textures:
            texture.destroy()

        glDeleteProgram(self.shader)

        pg.quit()


if __name__ == "__main__":

    myApp = App()