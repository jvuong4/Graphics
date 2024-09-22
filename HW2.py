#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COSC 4370 Homework #2
"""
import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Planet:
    def __init__(self,r,o,p,c):
        self.radius = r
        self.orb_radius = o
        self.period = p
        self.sphere = gluNewQuadric()
        self.color = c
        #period = 365.26 for earth, earth moves 1 deg each time
        self.speed = 365.26 / p #how fast it should revolve
        
    def draw_orbit(self,a):
        glPushMatrix()
        glLoadIdentity()
        glOrtho(-20, 20, -20, 20, -20, 20)
        #match rotation of the model
        glRotated(a, 1, 0, 0)
        
        glColor(1,1,1)
        glBegin(GL_LINE_LOOP)
        for i in range(36):
            angle = 2.0 * math.pi * i / 36
            x = math.cos(angle) * self.orb_radius
            y = math.sin(angle) * self.orb_radius
            glVertex3fv((x, y, 0))
        glEnd()
        glPopMatrix()
        
    def render(self,t):
        glPushMatrix()
        
        glRotated(self.speed * t, 0, 0, 1)
        glTranslated(self.orb_radius,0,0)
        
        glColor(self.color[0],self.color[1],self.color[2]) # Draw the cube in white
        gluSphere(self.sphere, self.radius, 32, 32)
        
        glPopMatrix()
        
    def get_orb_radius(self):
        return self.orb_radius
    
    def get_speed(self):
        return self.speed
        
class Moon:
    def __init__(self,r,o,p,c,planet):
        self.radius = r
        self.orb_radius = o
        self.period = p
        self.sphere = gluNewQuadric()
        self.color = c
        #period = 365.26 for earth, earth moves 1 deg each time
        self.speed = 365.26 / p #how fast it should revolve
        self.planet_radius = planet.get_orb_radius()
        self.planet_speed = planet.get_speed()
        
    def draw_orbit(self,t,a):
        glPushMatrix()
        glLoadIdentity()
        glOrtho(-20, 20, -20, 20, -20, 20)
        
        #this is a mess...
        #first match the angle that the model is tilted
        glRotated(a, 1, 0, 0)
        #try to find out where the planet is
        glRotated(self.planet_speed * t, 0, 0, 1)
        #move to planet location
        glTranslated(self.planet_radius,0,0)
        #undo the rotation from finding planet
        glRotated(self.planet_speed * -t, 0, 0, 1)
        
        glColor(1,1,1)
        glBegin(GL_LINE_LOOP)
        for i in range(36):
            angle = 2.0 * math.pi * i / 36
            x = math.cos(angle) * self.orb_radius #/ 2
            y = math.sin(angle) * self.orb_radius #/ 2
            glVertex3fv((x, y, 0))
        glEnd()
        glPopMatrix()
        
    def render(self,t):
        glPushMatrix()
        #glLoadIdentity()
        
        glRotated(self.planet_speed * t, 0, 0, 1)
        glTranslated(self.planet_radius,0,0)
        glRotated(self.speed * t, 0, 0, 1)
        glTranslated(self.orb_radius,0,0)
        
        glColor(self.color[0],self.color[1],self.color[2]) # Draw the cube in white
        gluSphere(self.sphere, self.radius, 16, 16)
        
        glPopMatrix()
        

def main():
    pygame.init()
    display = (800,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption('Homework #2')
    glOrtho(-20, 20, -20, 20, -20, 20)
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)
    
    #sun's period is technically 0 but i don't wanna divide by 0 lol
    Sun = Planet(2,0,365.26,(1,0.73,0.31))
    Mercury = Planet(0.38,3.9,87.97,(1,0.56,0.46))
    Venus = Planet(0.95,7.2,224.70,(0.59,0.65,0.45))
    Earth = Planet(1,10,365.26,(0.42,0.63,0.67))
    Mars = Planet(0.53,15,686.98,(0.77,0.33,0.22))
    
    Earth_Moon = Moon(0.27,1.5,27.3,(0.7,0.7,0.73),Earth)
    
    t = -1000 + 1000
    angle = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] == 1 and angle + 1 <= 0:
            glRotated(1, 1, 0, 0)
            angle = angle + 1
        if keys[pygame.K_DOWN] == 1 and angle - 1 >= -90:
            glRotated(-1, 1, 0, 0)
            angle = angle -1
            
        Sun.render(t)
        
        Mercury.render(t)
        Venus.render(t)
        Earth.render(t)
        Mars.render(t)
        Earth_Moon.render(t)
       
        Mercury.draw_orbit(angle)
        Venus.draw_orbit(angle)
        Earth.draw_orbit(angle)
        Mars.draw_orbit(angle)
        
        Earth_Moon.draw_orbit(t, angle)
        
        pygame.display.flip()
        pygame.time.wait(20)
        t = t + 0.4


main()
