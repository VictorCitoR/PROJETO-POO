import pygame as pg
from pygame.locals import *
from Elementos import *
import time
import random
import math


def update(inp, sc, ct):
    for element in Elemento.ELEMENT_LIST:
        if element.__class__ != Elemento:
            element.update(inp, sc, ct)
    for element in Elemento.ELEMENT_LIST:
        if element.__class__ == Elemento:
            element.update(inp, sc, ct)
            break
    return


def process_input():
    inp_H = inp_V = None
    inp_MOUSE_STATE = inp_MOUSE_POS = (None, None, None)
    pressed = pg.key.get_pressed()
    if pressed[K_w]:
        inp_V = "UP"
    if pressed[K_s]:
        inp_V = "DOWN"
    if pressed[K_a]:
        inp_H = "LEFT"
    if pressed[K_d]:
        inp_H = "RIGHT"
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
        if event.type == MOUSEBUTTONDOWN:
            inp_MOUSE_STATE = event.button
            inp_MOUSE_POS = event.pos
            inp_KB = [inp_H, inp_V]
            inp_MO = [inp_MOUSE_STATE, inp_MOUSE_POS]
            inp = {'keyboard': inp_KB,
                   'mouse': inp_MO}
            return inp

    inp_KB = [inp_H, inp_V]
    inp_MO = [inp_MOUSE_STATE, inp_MOUSE_POS]
    inp = {'keyboard': inp_KB,
           'mouse': inp_MO}
    
    return inp
    

def render(sc, ct):
    screen.fill((0,0,0))
    for element in Elemento.ELEMENT_LIST:
        element.draw(sc, ct)
    return

pg.init()
#screen = pg.display.set_mode(flags=pg.FULLSCREEN)
screen = pg.display.set_mode((1440, 720))
elements_access = Elemento()

previous = time.time()
lag = 0
S_PER_FRAME = 1/30
input_passado = {'keyboard': [None, None], 'mouse': [(None, None, None), (None, None, None)]}

record_time = 2
now = time.time()

while True:
    current = time.time()
    # if current - now < record_time:
    #     previous = current
    #     continue
    elapsed = current - previous
    previous = current
    lag += elapsed

    game_input = process_input()

    while lag >= S_PER_FRAME:
        if input_passado == game_input:
            update(game_input, screen, current)
        else:
            update(input_passado, screen, current)
            input_passado = {'keyboard': [None, None], 'mouse': [(None, None, None), (None, None, None)]}
        lag -= S_PER_FRAME
    else:
        if game_input["keyboard"] != [None, None]:
            input_passado["keyboard"] = game_input["keyboard"]
        if game_input["mouse"] != [(None, None, None), (None, None, None)]:
            input_passado["mouse"] = game_input["mouse"]


    render(screen, current)

    pg.display.update()
        