"""
COSC 4370 Extra Credit

"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GLU import *
import pywavefront

# Initialize Pygame and OpenGL
pygame.init()
display = (800, 800)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
#import random

#from LightingExample
clock = pygame.time.Clock()

# Set up the perspective projection
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
    
glMatrixMode(GL_PROJECTION)
    
glOrtho(-25,25,-25,25,-25,25)
glTranslate(0,-5, 0)
glRotatef(-80, 1, 0, 0)

glTranslatef(0, 0, -5)
    
glLight(GL_LIGHT0, GL_POSITION, (10.0, -10.0, 0, 1))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
glMatrixMode(GL_MODELVIEW)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
# Load the .obj file
scene = pywavefront.Wavefront('teapot.obj', collect_faces=True)


verts = scene.vertices
faces = []
NORMALS = []
for mesh in scene.mesh_list:
    for face in mesh.faces:
        faces.append(tuple([v for v in face]))
        #for vertex_i in face:
        #    verts.append(scene.vertices[vertex_i])

#Generate some randome colors so we can see what is going on
# ** This should be removed before submission! **
#COLORS = [(random.random(), random.random(), random.random(), 1) for x in verts]
COLORS = [(0.2,0.5,1) for x in verts]

for face in faces:
    p1 = verts[face[0]]
    p2 = verts[face[1]]
    p3 = verts[face[2]]
    
    u = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
    v = [p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]]
    
    x = u[1] * v[2] - u[2] * v[1]
    y = u[2] * v[0] - u[0] * v[2]
    z = u[0] * v[1] - u[1] * v[0]
    
    normal = (x,y,z)
    
    NORMALS.append(normal)
        

# Function to draw the .obj file
def draw_obj(verts):
    glBegin(GL_TRIANGLES)
    '''
    for color, vert in zip(COLORS, verts):
        glColor(color)
        glVertex3fv(vert)
    glEnd()
    '''
    for i_surface, surface in enumerate(faces):
        glNormal3fv(NORMALS[i_surface])
        for i_vertex, vertex in enumerate(surface):
            index = (i_surface+i_vertex) % 2
            glColor3fv(COLORS[i_vertex])
            glVertex3fv(verts[vertex])
    glEnd()
    '''
    glColor3fv((0,0,0))
    glBegin(GL_LINES)
    for edge in EDGES:
        for vertex in edge:
            glVertex3fv(VERTICES[vertex])
    glEnd()
    '''

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    # Clear the screen and draw the .obj file
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glRotate(2,0,0,1)
    draw_obj(verts)
    pygame.display.flip()
    clock.tick(10)


pygame.quit()
