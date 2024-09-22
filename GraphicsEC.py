'''
Use the up, down, left, and right arrows to help rotate the dice
Use the number keys 1-5 to change the displayed dice
'''

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GLU import *
import pywavefront

import math

def draw_label(position, text):
    font = pygame.font.SysFont('Arial', 24)
    text_surface = font.render(text, True, (255, 255, 255), (0, 0, 0))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos3fv(position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

class Polyhedron:
    def __init__(self):
        self.vertices = () #the coordinates of each of the polyhedron's vertices
        self.edges = () #links vertices together to form the polyhedron's edges
        self.texture_coords = () #the texture coordinates that the corresponding tri/quad will use for the polyhedron's texture
        self.surfaces = () #the vertices that form the tris/quads for the polyhedron's texture
        self.normals = [] #the surface normals of the polyhedron's tris/quads, used for lighting
        self.colors = ((1,0,0), (1,0,0), (0,0,1)) #the colors for vertex coloring
    
    def draw(self):
        glBegin(GL_TRIANGLES)
        
        for surface_index,surface in enumerate(self.surfaces):
            glNormal3fv(self.normals[surface_index])
            for vertex_index,vertex in enumerate(surface):
                glColor3fv(self.colors[vertex_index])
                glTexCoord2fv(self.texture_coords[surface_index][vertex_index])
                glVertex3fv(self.vertices[vertex])
        glEnd()
    
    def getNormal(self):
        for face in self.surfaces:
            p1 = self.vertices[face[0]]
            p2 = self.vertices[face[1]]
            p3 = self.vertices[face[2]]
            
            u = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
            v = [p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]]
            
            x = u[1] * v[2] - u[2] * v[1]
            y = u[2] * v[0] - u[0] * v[2]
            z = u[0] * v[1] - u[1] * v[0]
            
            normal = (x,y,z)
            
            self.normals.append(normal)
        
            
class Tetrahedron(Polyhedron):
    def __init__(self):
        super().__init__()
        d = 1.0/math.sqrt(3)
        self.vertices = (
            (d, d, d),
            (d, -d, -d),
            (-d, d, -d),
            (-d, -d, d)
            )
        self.texture_coords = (
            ((0,0.8),(0.2,0.8),(0.1,1)),    
            ((0.2,0.8),(0.4,0.8),(0.3,1)),      
            ((0.4,0.8),(0.6,0.8),(0.5,1)),     
            ((0.6,0.8),(0.8,0.8),(0.7,1))
            )
        self.surfaces = ((1,2,0), (2,1,3), (3,1,0), (2,3,0))
        self.getNormal()

class Cube(Polyhedron):
    def __init__(self):
        super().__init__()
        d = 1.0/math.sqrt(3)
        self.vertices = ((d, -d, -d),
                          (d, d, -d),
                          (-d, d, -d),
                          (-d, -d, -d),
                          (d, -d, d),
                          (d, d, d),
                          (-d, -d, d),
                          (-d, d, d))
        self.texture_coords = (((0,1), (0.2,1), (0.2,0.75), (0,0.75)), #1
                  ((0.2,1), (0.4,1),(0.4,0.75),(0.2,0.75)), #2
                  ((0,0.75),(0.2,0.75),(0.2,0.5),(0,0.5)), #6
                  ((0.8,1), (1,1),(1,0.75),(0.8,0.75)), #5
                  ((0.4,1),(0.6,1),(0.6,0.75),(0.4,0.75)), #3
                  ((0.6,1), (0.8,1), (0.8,0.75), (0.6,0.75)) #4
                  )
        self.surfaces = ((0,1,2,3), (3,2,7,6), (6,7,5,4), (4,5,1,0), (1,5,7,2), (4,0,3,6))
        self.normals = [
            ( 0,  0, -1),  # surface 0
            (-1,  0,  0),  # surface 1
            ( 0,  0,  1),  # surface 2
            ( 1,  0,  0),  # surface 3
            ( 0,  1,  0),  # surface 4
            ( 0, -1,  0)   # surface 5
            ]
        self.colors = ((1,0,0), (0,0,1), (1,0,0), (0,0,1))
        
    def draw(self):
        glBegin(GL_QUADS)
        
        for surface_index,surface in enumerate(self.surfaces):
            glNormal3fv(self.normals[surface_index])
            for vertex_index,vertex in enumerate(surface):
                #index = (surface_index+vertex_index) % 2
                
                glColor3fv(self.colors[vertex_index])
                glTexCoord2fv(self.texture_coords[surface_index][vertex_index])
                glVertex3fv(self.vertices[vertex])
        glEnd()

class Octahedron(Polyhedron):
    def __init__(self):
        super().__init__()
        d = 1
        self.vertices = (
            (0, d, 0),
            (0, -d, 0),
            (d, 0, 0),
            (-d, 0, 0),
            (0, 0,d),
            (0, 0,-d)
            )
        self.texture_coords = (
            ((0,0.8),(0.2,0.8),(0.1,1)),    
            ((0.2,0.8),(0.4,0.8),(0.3,1)),      
            ((0.4,0.8),(0.6,0.8),(0.5,1)),     
            ((0.6,0.8),(0.8,0.8),(0.7,1)),  
            ((0.8,0.8),(1,0.8),(0.9,1)),
            ((0,0.55),(0.2,0.55),(0.1,0.75)),   
            ((0.2,0.55),(0.4,0.55),(0.3,0.75)),   
            ((0.4,0.55),(0.6,0.55),(0.5,0.75))
            ) 
        self.surfaces = (
            (1,2,4),
            (2,0,4),
            (0,3,4),
            (3,1,4),
            (5,2,1),
            (5,0,2),
            (5,3,0),
            (5,1,3)
            ) 
        self.getNormal()

class Dodecahedron(Polyhedron):
    def __init__(self):
        super().__init__()
        d = 1.0/math.sqrt(3)
        const = (1.0 + math.sqrt(5.0))/2.0 #golden ratio
        self.vertices = (
                (d, -d, -d),
                (d, d, -d),
                (-d, d, -d),
                (-d, -d, -d),
                (d, -d, d),
                (d, d, d),
                (-d, -d, d),
                (-d, d, d),
                (0, d * const, d / const),
                (0, d * const, -d / const),
                (0, -d * const, d / const),
                (0, -d * const, -d / const),
                (d / const, 0, d * const),
                (d / const, 0, -d * const),
                (-d / const, 0, d * const),
                (-d / const, 0, -d * const),
                (d * const, d / const, 0),
                (d * const, -d / const, 0),
                (-d * const, d / const, 0),
                (-d * const, -d / const, 0)
                )
        self.texture_coords = (
            ((0,0.75),(0.2,0.75),(0.1,1)),       ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
            ((0.2,0.75),(0.4,0.75),(0.3,1)),       ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
            ((0.4,0.75),(0.6,0.75),(0.5,1)),       ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
            ((0.6,0.75),(0.8,0.75),(0.7,1)),       ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
            ((0.8,0.75),(1,0.75),(0.9,1)),       ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
            
            ((0,0.5),(0.2,0.5),(0.1,0.75)),       ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
            ((0.2,0.5),(0.4,0.5),(0.3,0.75)),       ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
            ((0.4,0.5),(0.6,0.5),(0.5,0.75)),       ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
            ((0.6,0.5),(0.8,0.5),(0.7,0.75)),       ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
            ((0.8,0.5),(1,0.5),(0.9,0.75)),       ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
                
            ((0,0.25),(0.2,0.25),(0.1,0.5)),       ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
            ((0.2,0.25),(0.4,0.25),(0.3,0.5)),       ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
            ) 
        self.surfaces = (
                        (6,10,12), (6,14,12), (10,4,12),
                        (17,16,12), (17,4,12), (16,5,12),
                        (8,7,12), (8,5,12), (7,14,12),
                        (3,11,6), (3,19,6), (11,10,6),
                        (18,19,14), (18,7,14), (19,6,14),
                        (11,0,4), (11,10,4), (0,17,4),
                        (13,15,9), (13,1,9), (15,2,9),
                        (13,1,17), (13,0,17), (1,16,17),
                        (1,9,5), (1,16,5), (9,8,5),
                        (2,15,19), (2,18,19), (15,3,19),
                        (9,2,7), (9,8,7), (2,18,7),
                        (15,13,11), (15,3,11), (13,0,11)
                        )
        self.getNormal()
    
    def draw(self):
        glBegin(GL_TRIANGLES)
            
        for surface_index,surface in enumerate(self.surfaces):
            glNormal3fv(self.normals[surface_index // 3])
            for vertex_index,vertex in enumerate(surface):
                glColor3fv(self.colors[vertex_index])
                glTexCoord2fv(self.texture_coords[surface_index][vertex_index])
                glVertex3fv(self.vertices[vertex])
        glEnd()
    
    def getNormal(self):
        i = 0
        for face in self.surfaces:
            if i == 0:
                p1 = self.vertices[face[0]]
                p2 = self.vertices[face[1]]
                p3 = self.vertices[face[2]]
                
                u = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
                v = [p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]]
                
                x = u[1] * v[2] - u[2] * v[1]
                y = u[2] * v[0] - u[0] * v[2]
                z = u[0] * v[1] - u[1] * v[0]
                
                normal = (x,y,z)
                
                self.normals.append(normal)
            i = (i + 1) % 3
                
    

class Icosahedron(Polyhedron):
    def __init__(self):
        super().__init__()
        d = 1.0/math.sqrt(3)
        const = (1.0 + math.sqrt(5.0))/2.0 #golden ratio
        self.vertices = (
            (0,d*const,d),
            (d*const,d,0),
            (0,d*const,-d),
            (-d*const,d,0),
            (d,0,d*const),
            (d,0,-d*const),
            (-d,0,d*const),
            (-d,0,-d*const),
            (0,-d*const,d),
            (d*const,-d,0),
            (0,-d*const,-d),
            (-d*const,-d,0)
            )
        self.texture_coords = (
            ((0,0.8),(0.2,0.8),(0.1,1)),    
            ((0.2,0.8),(0.4,0.8),(0.3,1)),      
            ((0.4,0.8),(0.6,0.8),(0.5,1)),     
            ((0.6,0.8),(0.8,0.8),(0.7,1)),    
            ((0.8,0.8),(1,0.8),(0.9,1)),

            ((0,0.55),(0.2,0.55),(0.1,0.75)),   
            ((0.2,0.55),(0.4,0.55),(0.3,0.75)),   
            ((0.4,0.55),(0.6,0.55),(0.5,0.75)),    
            ((0.6,0.55),(0.8,0.55),(0.7,0.75)),    
            ((0.8,0.55),(1,0.55),(0.9,0.75)),     
    
            ((0,0.3),(0.2,0.3),(0.1,0.5)),     
            ((0.2,0.3),(0.4,0.3),(0.3,0.5)),    
            ((0.4,0.3),(0.6,0.3),(0.5,0.5)),    
            ((0.6,0.3),(0.8,0.3),(0.7,0.5)),   
            ((0.8,0.3),(1,0.3),(0.9,0.5)),     
    
            ((0,0.05),(0.2,0.05),(0.1,0.25)),    
            ((0.2,0.05),(0.4,0.05),(0.3,0.25)),   
            ((0.4,0.05),(0.6,0.05),(0.5,0.25)),  
            ((0.6,0.05),(0.8,0.05),(0.7,0.25)),
            ((0.8,0.05),(1,0.05),(0.9,0.25))
            
            ) 
        self.surfaces = (
            (1,0,4),
            (0,6,4),
            (4,6,8),
            (6,11,8),
            (11,6,3),
            (0,3,6),
            (0,2,3),
            (1,2,0),
            (4,9,1),
            (8,9,4),
            (11,10,8),
            (3,7,11),
            (2,7,3),
            (10,9,8),
            (7,10,11),
            (2,1,5),
            (1,9,5),
            (9,10,5),
            (10,7,5),
            (7,2,5)
            ) 
        self.getNormal()


def loadTexture():
    textureSurface = pygame.image.load('ECTexture.png')
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texid


pygame.init()
display = (800, 800)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)


glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

glMatrixMode(GL_MODELVIEW)
glTranslatef(0, 0, -5)

glLight(GL_LIGHT0, GL_POSITION,  (0, -5.0, 0.5, 1)) # point light from the below
glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

glEnable(GL_DEPTH_TEST) 

glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )

loadTexture()

run = True
angle = 0 # Rotation angle about the vertical axis
tiltangle = 0
glColor(1,1,1,1)

d4 = Tetrahedron()
d6 = Cube()
d8 = Octahedron()
d12 = Dodecahedron()
d20 = Icosahedron()

state = 1
states = [1,2,3,4,5] #stores the ASCII values of 1-5

def Draw(state):
    if state == 1:
        d4.draw()
    elif state == 2:
        d6.draw()
    elif state == 3:
        d8.draw()
    elif state == 4:
        d12.draw()
    elif state == 5:
        d20.draw()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN: # Capture an escape key press to exit
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = False

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glRotatef(2, 0.1, 0.1, 10) # Rotate around the box's vertical axis
    
    keys = pygame.key.get_pressed()
    for check in states:
        if keys[check + 48] == 1: #add 48 to get the number's ascii value
            state = check
            break
    if keys[pygame.K_UP] == 1:
        glRotated(-10, 1, 0, 0)
    if keys[pygame.K_DOWN] == 1:
        glRotated(10, 1, 0, 0)
    if keys[pygame.
            K_LEFT] == 1:
        glRotated(-10, 0, 1, 0)
    if keys[pygame.K_RIGHT] == 1:
        glRotated(10, 0, 1, 0)
    
    Draw(state)

    pygame.display.flip()
    pygame.time.wait(30)

pygame.quit()

