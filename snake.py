import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
import sys


width = 600

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

pygame.init()

win = pygame.display.set_mode((width, width))


pygame.display.set_caption('Slitherin.io')

game_icon = pygame.image.load('icon.png')
pygame.display.set_icon(game_icon)

apple = pygame.image.load('apple1.jpg')



smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

clock = pygame.time.Clock()

class apple_snack(object):
    rows = 20
    w = width
    def __init__(self, start, dir_x = 1, dir_y = 0):
        self.pos = start
        self.dir_x = 1
        self.dir_y = 0
        
    def move(self, dir_x, dir_y):
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.pos = (self.pos[0] + self.dir_x, self.pos[1] + self.dir_y)

    def draw(self, surface):
        sq = self.w // self.rows

        i = self.pos[0]
        j = self.pos[1]
        surface.blit(apple, (i*sq + 1, j*sq + 1))

class cube(object):
    rows = 20
    w = width
    def __init__(self, start, dir_x = 1, dir_y = 0, color = (0, 255, 0)):
        self.pos = start
        self.dir_x = 1
        self.dir_y = 0
        self.color = color
        
    def move(self, dir_x, dir_y):
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.pos = (self.pos[0] + self.dir_x, self.pos[1] + self.dir_y)

    def draw(self, surface, eyes = False):
        sq = self.w // self.rows

        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * sq + 1, j * sq + 1, sq - 1, sq - 1))

        if eyes:
            radius = 3
            center = sq // 2
            eye1 = (i*sq + center - radius, j*sq + 8)
            eye2 = (i*sq + sq - radius*2, j*sq + 8)
            pygame.draw.circle(surface, (255, 0, 0), eye1 ,radius, 0)
            pygame.draw.circle(surface, (255, 0, 0), eye2 ,radius, 0)



class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dir_x = 0
        self.dir_y = 1


    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        try :
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dir_x = -1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

                elif keys[pygame.K_RIGHT]:
                    self.dir_x = 1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                
                elif keys[pygame.K_UP]:
                    self.dir_x = 0
                    self.dir_y = -1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

                elif keys[pygame.K_DOWN]:
                    self.dir_x = 0
                    self.dir_y = 1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
        except:
            pass
            

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p) 
            else:
                if c.dir_x == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])   
                elif c.dir_x == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])
                elif c.dir_y == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dir_y == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else:
                    c.move(c.dir_x, c.dir_y)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        


    def addCube(self):
        tail = self.body[-1]
        xdir = tail.dir_x
        ydir = tail.dir_y

        if xdir == -1 and ydir == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif xdir == 1 and ydir == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif xdir == 0 and ydir == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))
        elif xdir == 0 and ydir == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))

        self.body[-1].dir_x = xdir
        self.body[-1].dir_y = ydir

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        
        # pygame.draw.line(surface, (255, 255, 255), (x,0), (x,w))
        # pygame.draw.line(surface, (255, 255, 255), (0,y), (w,y))

def redrawWindow(surface):
    try:
        global side, rows, Snake, Snack
        surface.fill((255,255,255))
        Snake.draw(surface)
        Snack.draw(surface)
        # drawGrid(side, rows, surface)
        pygame.display.update()
    except:
        pass

def Score(score):
    game_over = True
    
    while game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    game_over = False
                    Snake.reset((10, 10))
                    
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
   
        win.fill(white)
        msg = largefont.render('Game Over', 1, green)
        win.blit(msg, (width/2 - msg.get_width()/2, width/2 - msg.get_height() - 10))
        text = medfont.render("Score: "+ str(score), True, red)
        win.blit(text, (width/2 - msg.get_width()/4, width/2 ))

        msg = smallfont.render('Press C to Continue or Q to Exit', 1, black)
        win.blit(msg, (width/2 - msg.get_width()/2, width/2 + msg.get_height() + 30))
        pygame.display.update()
        clock.tick(10)



def game_intro():

    intro = True
    global Snake
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
   
        win.fill(white)
        msg = largefont.render('Slitherin.io', 1, green)
        win.blit(msg, (width/2 - msg.get_width()/2, width/2 - msg.get_height()))
        msg = smallfont.render('Press C to Continue or Q to Exit', 1, black)
        win.blit(msg, (width/2 - msg.get_width()/2, width/2 + msg.get_height()))
        pygame.display.update()
        clock.tick(10)



def randomSnack(rows, item):
    
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z : z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    
    return (x,y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    messagebox.showinfo(subject, content)


def main():
    global side, rows, Snake, Snack
    side = width
    rows = 20

    win = pygame.display.set_mode((side, side))

    Snake = snake((0,255,0), (10, 10))
    Snack = apple_snack(randomSnack(rows, Snake))
    
    
    run = True
    state = True # Running
    paused = False

    while run:
        pygame.time.delay(50)
        clock.tick(10)
        
        try:

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_p]:
                    state = False

            if state == False:
                paused = True
                while paused:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_c:
                                state = True
                                paused = False
                            if event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()

                    clock.tick(10)
                    
                
            if state == True:
                
                Snake.move()
                if Snake.body[0].pos == Snack.pos:
                    Snake.addCube()
                    Snack = apple_snack(randomSnack(rows, Snake))
                for x in range(len(Snake.body)):
                    if Snake.body[x].pos in list(map(lambda z: z.pos , Snake.body[x+1 : ])):
                        Score(len(Snake.body) - 1)
                        
                        #print('Score  :', len(Snake.body))
                        #message_box('You Lost !!', 'Play Again')
                        #Snake.reset((10,10))
                        break
                redrawWindow(win)

        except:
            pass


game_intro()
main()           


