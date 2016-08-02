#!/usr/bin/python2

#
# TETRIS!
#

import pygame
import math
import random
import select
import sys
import time
import tty, termios

# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0, 0, 255)
X, Y = 20, 30
W = 20
SHAPE = [
[[
' xx',
'xx '
],
[
'x ',
'xx',
' x'
]],
[[
'xxxx'
],
[

'x',
'x',
'x',
'x',
]],
[[
'xx',
'xx'
]],
[[
'xxx',
' x '
],
[
' x',
'xx',
' x'
],
[
' x ',
'xxx',
],
[
'x ',
'xx',
'x '
]],
[[
'xx',
' x',
' x'
],
[
'  x',
'xxx',
],
[
'x ',
'x ',
'xx'
],
[
'xxx',
'x  '
]]
]

def drawgrid():
    for y in range(Y):
        pygame.draw.line(scr, WHITE, (0, y * W), (X * W, y * W), 1)
    for x in range(X):
        pygame.draw.line(scr, WHITE, (x * W, 0), (x * W, y * W), 1)
    pygame.display.update()
    
def draw(mode):
    global frame
    if mode == 'erase':
        c1 = c2 = BLACK
    else:
        c1 = RED
        c2 = GREEN
    for (x, y) in pos:
        pygame.draw.rect(scr, c1, (x * W, y * W, W, W), 0)
    for (x, y) in bot:
        pygame.draw.rect(scr, c1, (x * W, y * W, W, W), 0)
    drawgrid()
    pygame.display.update()
    if mode != 'erase':
        pygame.image.save(scr, 'image-{}.png'.format(frame))
        frame += 1

def atbottom():
    for (x, y) in pos:
        if y >= Y:
            return True
    return False

def legal(dx, dy):
    for (x, y) in pos:     
        if (x + dx, y + dy) in bot:
            return False
        if x + dx < 0 or y + dy < 0:
            return False
        if x + dx >= X or y + dy >= Y - 1:
            return False
    return True

def move(dx, dy):
    global pos, bot, n2, t, delay, score, down
    #if dy == 0:
    #    dy = 0
    if dy == 1 and (atbottom() or not legal(dx, dy)):
        t = random.choice(range(len(SHAPE)))
        #t = 1
        n2 = 0
        down = 0
        bot += pos
        init(t, n2)        
    elif legal(dx, dy):  
        pos2 = []
        draw('erase')
        for (x, y) in pos:
            pos2 += [(x + dx, y + dy)]
        pos = pos2
        draw('create')
    
    # check bottom
    cnt = 0
    for (x, y) in bot:
        if y == Y - 2:
            cnt += 1
    if cnt >= X:
        score += 1
        print 'Score: {}'.format(score)
        #wr_score()
        draw('erase')
        bot = [(x, y) for (x, y) in bot if y != Y - 2]  
        bot = [(x, y + 1) for (x, y) in bot]
        #bot = bot2
        draw('create')
    
def wr_score():
    global scr
    font = pygame.font.SysFont('Arial', 35)
    for msg in [
    '                ',
    'Score: {}'.format(score)
    ]:
        scr.blit(font.render(msg, True, (255,255,255)), (0, Y * (W - 0)))

def init(t, n2):
    global pos, delay, bot, scr
    #t = random.choice(range(len(SHAPE)))
    #wr_score()
    delay = 25   
    draw('erase')
    pos = []
    for y3, y2 in enumerate(SHAPE[t][n2]):
        for x3, x2 in enumerate(y2):
            if x2 == 'x':
                pos += [(X / 2 + x3, y3)]
    draw('create')

def getkey(delay):
    i,o,e = select.select([sys.stdin],[],[],delay)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.read()
            return input            

pygame.init()
size = (X * W, (Y + 0) * W)
scr = pygame.display.set_mode(size)
frame = 0
pygame.display.set_caption("Tetris")

# -------- Main Program Loop -----------
COLOR = RED
scr.fill(WHITE)
run = True
x = 0
y = 2
down = 0
score = 0
bot = []
pos = []
pygame.key.set_repeat(100, 50)
scr.fill(BLACK)
t = random.choice(range(len(SHAPE)))
#t = 1
n2 = 0
init(t, n2)
while run == True:
    #move(0, down)
    t0 = int(100 * time.time())
    while int(100 * time.time()) - t0 < delay:
        time.sleep(0.02)
        for e in pygame.event.get(): # User did something
            if e.type == pygame.QUIT: # If user clicked close
                run = False     
            if e.type == pygame.KEYDOWN:    
                ch = pygame.key.get_pressed()
                if ch[pygame.K_z]:
                    n2 = (n2 + 1) % len(SHAPE[t])
                    init(t, n2)
                if ch[pygame.K_x]:
                    tmp = len(SHAPE[t])    
                    n2 = (n2 - 1 + tmp) % tmp
                    init(t, n2)
                if ch[pygame.K_LEFT]:
                    move(-1, 0)
                if ch[pygame.K_RIGHT]:
                    move(1, 0)
                if ch[pygame.K_UP]:
                    move(0, -1)
                if ch[pygame.K_DOWN]:
                    move(0, 1)
                if ch[pygame.K_SPACE]:
                    draw('erase')
                    down = 1
                    delay = 1
                if ch[pygame.K_ESCAPE]:
                    down = 1 - down 
    #n2 = (n2 + 1) % 4
pygame.quit()

#
# convert -delay 20 image-%d.png[0-109] tetris.gif
#

