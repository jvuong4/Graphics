import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math



forced = False

d = 1 / math.sqrt(3)
const = (1.0 + math.sqrt(5.0))/2.0 #golden ratio
vertices_d12 = (
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

edges_d12 = (
        (0,11),(0,13),(0,17),(1,13),(1,9),(1,16),
        (2,9),(2,18),(2,15),(3,15),(3,11),(3,19),
        (4,12),(4,17),(4,10),(5,8),(5,12),(5,16),
        (6,10),(6,14),(6,19),(7,8),(7,14),(7,18),
        (8,9),(10,11),(12,14),(13,15),(16,17),(18,19)
        )

#each of the 12 sides have 3 triangles.
# the first of the 3 are for the number, and the other 2 are just a solid color.
surfaces_d12 = (
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

#each of the 12 sides have 3 triangles.
# the first of the 3 are for the number, and the other 2 are just a solid color.
texture_coords_d12 = (((0, 2.0/3.0), (0.25, 2.0/3.0), (0.125, 1)), ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
                      ((0.25, 2.0/3.0), (0.5, 2.0/3.0), (0.375, 1)), ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
                      ((0.5, 2.0/3.0), (0.75, 2.0/3.0), (0.625, 1)), ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
                      ((0.75, 2.0/3.0), (1, 2.0/3.0), (0.875, 1)), ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
                      
                      ((0, 1.0/3.0), (0.25, 1.0/3.0), (0.125, 2.0/3.0)), ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
                      ((0.25, 1.0/3.0), (0.5, 1.0/3.0), (0.375, 2.0/3.0)), ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
                      ((0.5, 1.0/3.0), (0.75, 1.0/3.0), (0.625, 2.0/3.0)), ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
                      ((0.75, 1.0/3.0), (1, 1.0/3.0), (0.875, 2.0/3.0)), ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
                      
                      ((0, 0), (0.25, 0), (0.125, 1.0/3.0)), ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
                      ((0.25, 0), (0.5, 0), (0.375, 1.0/3.0)), ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
                      ((0.5, 0), (0.75, 0), (0.625, 1.0/3.0)), ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)),
                      ((0.75, 0), (1, 0), (0.875, 1.0/3.0)), ((0, 0), (0.1, 0), (0, 0.1)), ((0, 0), (0.1, 0), (0, 0.1)))

def Dodecahedron(vx,vy,vz,texture):
    glBegin(GL_TRIANGLES)
    
    for surface_index,surface in enumerate(surfaces_d12):
        for vertex_index,vertex in enumerate(surface):
            glTexCoord2fv(texture[surface_index][vertex_index])
            glVertex3fv(vertices_d12[vertex])
    
    glEnd()
    
    glBegin(GL_LINES)
    glColor3f(55.0/255.0,109.0/255.0,122.0/255.0)#,1)
    for edge in edges_d12:
        for vertex in edge:
            glVertex3fv(vertices_d12[vertex])
    glEnd()

def loadTexture():
    textureSurface = pygame.image.load('texture.png')
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
scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)


glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glShadeModel(GL_SMOOTH)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])


glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()

loadTexture()

run = True
angle = 0 # Rotation angle about the vertical axis
tiltangle = 0 # This is so that tilt ISN'T aligned with rotation speed. makes seeing all 12 sides easier
glColor(1,1,1,1)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN: # Capture an escape key press to exit
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = False

    # init model view matrix
    glLoadIdentity()

    # apply view matrix
    glMultMatrixf(viewMatrix)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glColor(1,1,1,1)
    tilt = 10 + 15 * math.cos(tiltangle * math.pi/180) # Tilt as we rotate
    glRotate(tilt, 1, 0, 0) # Tilt a bit to be easier to see
    angle = (angle + 1) % 360
    tiltangle = (tiltangle + 1.7) % 360
    glRotatef(angle, 0, 0, 1) # Rotate around the box's vertical axis
    
    Dodecahedron(0,0,0,texture_coords_d12)

    glColor4f(0.5, 0.5, 0.5, 1)
    glBegin(GL_QUADS)
    glVertex3f(-10, -10, -2)
    glVertex3f(10, -10, -2)
    glVertex3f(10, 10, -2)
    glVertex3f(-10, 10, -2)
    glEnd()

    glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(30)

pygame.quit()