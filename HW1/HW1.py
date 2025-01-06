#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COSC 4370 Homework #1
This is the starter code for the first homework assignment.
It should run as is and will serve as the starting point for development.
"""
import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


def Cube():
    d = 1.0/math.sqrt(3)  # This is the default but is too large and needs to be changed
    verticies = (
        (d, -d, -d),
        (d, d, -d),
        (-d, d, -d),
        (-d, -d, -d),
        (d, -d, d),
        (d, d, d),
        (-d, -d, d),
        (-d, d, d)
        )

    edges = (
        (0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
        (6,3), (6,4), (6,7), (5,1), (5,4), (5,7)
        )
    glColor(1,1,1) # Draw the cube in white
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def Tetrahedron():
    d = 1.0/math.sqrt(3)  
    verticies = (
        (d, d, d),
        (d, -d, -d),
        (-d, d, -d),
        (-d, -d, d)
        )

    edges = (
        (0,1), (0,2), (0,3),
        (1,2), (1,3), (2,3)
        )
    glColor(1,1,1) # Draw the cube in white
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def Octahedron():
    d = 1 
    verticies = (
        (0, d, 0),
        (0, -d, 0),
        (d, 0, 0),
        (-d, 0, 0),
        (0, 0,d),
        (0, 0,-d)
        )

    edges = (
        (0,2), (0,3), (0,4), (0,5),
        (1,2), (1,3), (1,4), (1,5),
        (2,4), (2,5), (3,4), (3,5)
        )
    glColor(1,1,1) # Draw the cube in white
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def Dodecahedron():
    d = 1.0/math.sqrt(3)
    const = (1.0 + math.sqrt(5.0))/2.0 #golden ratio
    verticies = (
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

    edges = (
        (0,11),(0,13),(0,17),(1,13),(1,9),(1,16),
        (2,9),(2,18),(2,15),(3,15),(3,11),(3,19),
        (4,12),(4,17),(4,10),(5,8),(5,12),(5,16),
        (6,10),(6,14),(6,19),(7,8),(7,14),(7,18),
        (8,9),(10,11),(12,14),(13,15),(16,17),(18,19)
        )
    glColor(1,1,1) # Draw the cube in white
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def Icosahedron():
    #d value calculated using pythag theorem,
    #0^2 + (d*goldenratio)^2 + d^2 = 1
    d = math.sqrt(2.0/(5.0+math.sqrt(5.0)))
    const = (1.0 + math.sqrt(5.0))/2.0 #golden ratio
    verticies = (
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
    edges = (
        (0,1),(0,2),(0,3),(0,4),(0,6),
        (1,2),(1,4),(1,5),(1,9),
        (2,3),(2,5),(2,7),
        (3,6),(3,7),(3,11),
        (4,6),(4,8),(4,9),
        (5,7),(5,9),(5,10),
        (6,8),(6,11),
        (7,10),(7,11),
        (8,9),(8,10),(8,11),
        (9,10),
        (10,11)
        )
    glColor(1,1,1) # Draw the cube in white
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def Axes():
    glBegin(GL_LINES)
    glColor(1,0,0) # Red for the x-axis
    glVertex3fv((0,0,0))
    glVertex3fv((1.5,0,0))
    glColor(0,1,0) # Green for the y-axis
    glVertex3fv((0,0,0))
    glVertex3fv((0,1.5,0))
    glColor(0,0,1) # Blue for the z-axis
    glVertex3fv((0,0,0))
    glVertex3fv((0,0,1.5))
    glEnd()

def Circle():
    glPushMatrix()
    glLoadIdentity()
    glOrtho(-2, 2, -2, 2, -2, 2)
    glColor(1,0,1) # Purple for the limits
    glBegin(GL_LINE_LOOP)
    for i in range(36):
        angle = 2.0 * math.pi * i / 36
        x = math.cos(angle)
        y = math.sin(angle)
        glVertex3fv((x, y, 0))
    glEnd()
    glPopMatrix()

def Draw(state):
    if state == 1:
        Tetrahedron()
    elif state == 2:
        Cube()
    elif state == 3:
        Octahedron()
    elif state == 4:
        Dodecahedron()
    elif state == 5:
        Icosahedron()

def main():
    pygame.init()
    display = (800,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption('Homework #1')
    glOrtho(-2, 2, -2, 2, -2, 2)
    glMatrixMode(GL_MODELVIEW)
    
    state = 1
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glRotatef(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Axes() # Draw the axes
        
        keys = pygame.key.get_pressed()
        states = [1,2,3,4,5] #stores the ASCII values of 1-5
        for check in states:
            if keys[check + 48] == 1: #add 48 to get the number's ascii value
                state = check
                break
        
        Draw(state) #Draw the specified polyhedron
        Circle() # Draw the limit circle
        
        pygame.display.flip()
        pygame.time.wait(10)


main()
