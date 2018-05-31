# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 11:45:27 2017

@author: kaykhos
"""

import pygame
import operator
import random
import numpy as np

cwd = 'C:\Users\Administrator\Desktop\Scripts'  # generalize this to 

## Set up screen sizes and colors
pygame.init()
size = width, height = 980, 680
speed = [1.5 for ii in range(2)]
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0
dt = 2
ship_exploded = False

## Input interaction functions
def get_key():
    temp = pygame.key.get_pressed()
    pressed = 'nothing'
    for i in range(len(temp)):
        if temp[i] == 1:
            pressed=pygame.key.name(i)
    return pressed

def get_mouse(): # haha, this looks really inefficient! what was i thinking? 
    button = 'none'
    temp = pygame.mouse.get_pressed()
    if temp[0] == 1:
        button = 1
    elif temp[1] == 1:
        button = 2
    elif temp[2] == 1:
        button = 3
    return button
    
## define spaceship object class
class New_Ship:
    def __init__(self, name, surf, *arg):
        self.name = name
        self.surface = surf
        if not not arg:
            self.rect = arg[0]
        else:
            self.rect = surf.get_rect()
    velocity = np.array([0, 0])
    acceleration = np.array([0, 0])
    position = np.array([width/2, height/2])
    exploded = False
    fuel = 100.0
    def move_to(self, posx, posy):
        self.position = np.array([posx, posy])   
        current = self.rect.center
        pos = tuple(self.position)
        diff = map(operator.sub, pos, current)
        self.rect.move_ip(diff[0], diff[1])
    def print_to_screen(self):
        screen.blit(self.surface, self.rect)
    def center(self):
        return np.array(self.rect.center)



## Calculated properties between objects
def calc_distence(item1,item2):
    p1 = item1.position
    p2 = item2.position
    dist = np.linalg.norm(p1 - p2)
    return dist

def calc_force(item1, item2):
    m = 10
    displacement = item1.position - item2.position
    fx = displacement[0] / calc_distence(item1, item2)
    fy = displacement[1] / calc_distence(item1, item2)
    return -1*fx/m, -1*fy/m

def move_ship(key, obj):
    mag = 0.10
    fuel_cost = 1
    if key == 'left' and ship.fuel > 0:
        ship.acceleration = ship.acceleration + np.array([-mag, 0])
        ship.fuel = ship.fuel - fuel_cost
        rect.move_ip((0, 5*fuel_cost))
    if key == 'right' and ship.fuel > 0:
        ship.acceleration = ship.acceleration + np.array([mag, 0])
        ship.fuel = ship.fuel - fuel_cost
        rect.move_ip((0, 5*fuel_cost))
    if key == 'up' and ship.fuel > 0:
        rect.move_ip((0, 5*fuel_cost))
        ship.acceleration = ship.acceleration + np.array([0, -mag])
        ship.fuel = ship.fuel - fuel_cost
        rect.move_ip((0, 5*fuel_cost))
        print(rect)
    if key == 'down' and ship.fuel > 0:
        ship.acceleration = ship.acceleration + np.array([0, mag])
        ship.fuel = ship.fuel -fuel_cost
        rect.move_ip((0, 5*fuel_cost))
    if key == 'space':
        ship.acceleration = np.array([0, 0])

def check_reset(but, obj):
    if but == 3:
        ship.move_to(width/2, height/2)
        dist = calc_distence(ship, sun)
        while dist < 1.2*rad:
            ship.move_to(rand_spot()[0], rand_spot()[1])    
            dist = calc_distence(ship, sun)
        ship.velocity = np.array([0, 0])
        ship.acceleration = np.array([2*(random.random() - 1), 2*(random.random() - 1)])
        #ship.acceleration = np.array([0, 0])
        ship.exploded = False
        ship.fuel = 100
        rect.move_ip((0,100 - rect.topleft[1]))


def check_win(ship, sun, planet):
    if calc_distence(sun, ship) < 40: #crash into sun
        ship.move_to(width/2, height/2)        
        ship.exploded = True
        ship.velocity = np.array([0, 0])
    if calc_distence(ship, planet) < 25 and np.linalg.norm(ship.velocity) < 6 and ship.exploded == False:
        pos = planet.position
        ship.move_to(pos[0], pos[1])
        ship.velocity = np.array([0, 0])
    if calc_distence(ship, planet) < 25 and np.linalg.norm(ship.velocity) > 6:
        ship.exploded = True        
        pos = planet.position
        ship.move_to(pos[0], pos[1])
        ship.velocity = np.array([0, 0])
        

def rand_spot():
    point = tuple([random.randint(0, width), random.randint(0, height)])
    return point
    


## Define sun, planets, ships and trajectory
sun_surf = pygame.Surface((40, 40))
sun_rect = pygame.draw.circle(sun_surf, red, (20, 20), 20)
sun = New_Ship('sun', sun_surf, sun_rect)
sun.move_to(width/2, height/2)

fuel = pygame.Surface((10, 1000))
rect = pygame.draw.rect(fuel, red, (1, 1, 200, 600))
rect.move_ip((10, 100))


t = np.linspace(0, 2*np.pi, 800);rad = 200
x, y = rad*np.cos(t) + width/2, rad*np.sin(t) + height/2
r = zip(x, y); traj = 0;

earth_surf = pygame.Surface((20, 20))
earth_rect = pygame.draw.circle(earth_surf, green, (10, 10), 10)
earth = New_Ship('earth', earth_surf, earth_rect)
earth.move_to(r[0][0], r[0][1])


ship = New_Ship('ship', pygame.image.load(cwd + '\\space.png'))
ship.move_to(width/2, height/2)
dist = calc_distence(ship, sun)
while dist < 1.2*rad:
    ship.move_to(rand_spot()[0], rand_spot()[1])    
    dist = calc_distence(ship, sun)
ship.velocity = np.array([1, -1])

explode = New_Ship('pow', pygame.image.load(cwd + '\\explode.png'))


## Set up play screen
screen = pygame.display.set_mode(size)




# set up game loop. 
while 1:
    traj+=1;traj = traj%len(t)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
    mouse = get_mouse()
    key = get_key()
    
    move_ship(key, ship)
    check_reset(mouse, ship)    
    
    earth.move_to(r[traj][0], r[traj][1])
    
    new_pos = ship.position + dt*ship.velocity
    ship.move_to(new_pos[0], new_pos[1])
    ship.velocity = ship.velocity + dt* ship.acceleration 
    ship.acceleration = np.array(calc_force(ship, sun)) + 0.4*np.array(calc_force(ship, earth))
    #ship.acceleration = np.array([0, 0])
    check_win(ship, sun, earth)
    print(ship.fuel)
    screen.fill(black)
    sun.print_to_screen()
    earth.print_to_screen()
    if ship.exploded == True:
        pos = ship.position
        explode.move_to(pos[0], pos[1])
        explode.print_to_screen()
        ship.velocity = np.array([0, 0])
    else:
        ship.print_to_screen()
    screen.blit(fuel, rect)
    pygame.display.flip()
    pygame.time.delay(40)








