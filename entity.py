#librairies

import glm
import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr
from abc import ABC, abstractmethod
import math

class Entity(ABC):

    def __init__(self, position, eulers):

        #eulers : rotation autour des axes x, y et z

        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

        #model matrix generation

        self.model = pyrr.matrix44.create_identity(dtype=np.float32)

        self.model = pyrr.matrix44.multiply(
            m1=self.model, 
            m2=pyrr.matrix44.create_from_translation(
                vec=np.array(self.position),dtype=np.float32
            ))
        
        self.vertices = []
        self.normals = []
        self.texCoords = []
        self.indices = []
        
        #abstract method
        self.initPoints()

        #conversion
        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.normals = np.array(self.normals, dtype=np.float32)
        self.texCoords = np.array(self.texCoords, dtype=np.float32)
        #INDICES EN INT !!!
        self.indices = np.array(self.indices, dtype=np.uint32)
        
        #create array buffer
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # create vertex buffers
        self.vbo = glGenBuffers(4)

        #position
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[0])
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

        #normals
        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[1])
        glBufferData(GL_ARRAY_BUFFER, self.normals.nbytes, self.normals, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, False, 0, None)

        #texture coordinates
        glEnableVertexAttribArray(2)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo[2])
        glBufferData(GL_ARRAY_BUFFER, self.texCoords.nbytes, self.texCoords, GL_STATIC_DRAW)
        glVertexAttribPointer(2, 2, GL_FLOAT, False, 0, None)

        # create index buffer
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo[3])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        #unbind array buffer
        glBindVertexArray(0)

        

    @abstractmethod
    def initPoints(self):
        pass

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)


    def destroy(self):
        glDeleteVertexArrays(1,(self.vao,))
        glDeleteBuffers(1,(self.vbo,))

        
        
class Square(Entity):

    """
        Used to draw a square.
    """

    def __init__(self, position, eulers):
        
        super().__init__(position, eulers)

    def initPoints(self):
        
        self.vertices = [
            -1, -1, 0,
            1, -1, 0,
            1, 1, 0,
            -1, 1, 0
        ]

        self.normals = [
            0, 0, 1,
            0, 0, 1,
            0, 0, 1,
            0, 0, 1
        ]

        self.texCoords = [
            0, 0,
            1, 0,
            1, 1,
            0, 1
        ]

        self.indices = [
            0, 1, 2,
            0, 2, 3
        ]



class Cube(Entity):

    """
        Used to draw a cube.
    """

    def __init__(self, position, eulers):
        
        super().__init__(position, eulers)

    def initPoints(self):
        
        self.vertices = [
            # Face avant
            1, -1, 1, -1, -1, 1, 1, 1, 1, -1, 1, 1,
            # Face arrière
            1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1,
            # Face gauche
            -1, -1, 1, -1, -1, -1, -1, 1, 1, -1, 1, -1,
            # Face droite
            1, -1, 1, 1, -1, -1, 1, 1, 1, 1, 1, -1,
            # Face supérieure
            -1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, -1,
            # Face inférieure
            -1, -1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1,
        ]

        self.normals = [
            # Face avant
            0, 0, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1,
            # Face arrière
            0, 0, -1,  0, 0, -1,  0, 0, -1,  0, 0, -1,
            # Face gauche
            -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0,
            # Face droite
            1, 0, 0,  1, 0, 0,  1, 0, 0,  1, 0, 0,
            # Face supérieure
            0, 1, 0,  0, 1, 0,  0, 1, 0,  0, 1, 0,
            # Face inférieure
            0, -1, 0,  0, -1, 0,  0, -1, 0,  0, -1, 0
        ]

        self.texCoords = [
            # Face avant
            1, 0, 0, 0, 1, 1, 0, 1,
            # Face arrière
            1, 0, 0, 0, 1, 1, 0, 1,
            # Face gauche
            1, 0, 0, 0, 1, 1, 0, 1,
            # Face droite
            1, 0, 0, 0, 1, 1, 0, 1,
            # Face supérieure
            0, 1, 1, 1, 0, 0, 1, 0,
            # Face inférieure
            0, 1, 1, 1, 0, 0, 1, 0
        ]

        self.indices = [
            # Face avant
            0, 1, 2, 1, 3, 2,
            # Face arrière
            4, 5, 6, 5, 7, 6,
            # Face gauche
            8, 9, 10, 9, 11, 10,
            # Face droite
            12, 13, 14, 13, 15, 14,
            # Face supérieure
            16, 17, 18, 17, 19, 18,
            # Face inférieure
            20, 21, 22, 21, 23, 22
        ]



class Sphere(Entity):

    """
        Used to draw a sphere.
    """

    def __init__(self, position, eulers):
        
        super().__init__(position, eulers)

    def initPoints(self):

        #parameters
        stacks = 30
        slices = 30
        
        for i in range(stacks + 1):
            lat = math.pi * i / stacks
            sinLat = math.sin(lat)
            cosLat = math.cos(lat)

            for j in range(slices + 1):
                lon = 2 * math.pi * j / slices
                sinLon = math.sin(lon)
                cosLon = math.cos(lon)

                x = cosLon * sinLat
                y = cosLat
                z = sinLon * sinLat

                self.vertices.extend([x, y, z])
                self.normals.extend([x, y, z])
                self.texCoords.extend([j / slices, i / stacks])

        for i in range(stacks):
            for j in range(slices):
                first = i * (slices + 1) + j
                second = first + slices + 1

                self.indices.extend([first, second, first + 1])
                self.indices.extend([second, second + 1, first + 1])