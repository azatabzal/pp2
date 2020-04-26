import pygame
import random
import time
from enum import Enum
from pygame import mixer

pygame.init()
width=800
height=600
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont('Arial', 32) 
FPS=60


mixer.music.load('game.mp3')
mixer.music.play(-1)


pygame.display.set_caption("Tanks")


bulletSound=pygame.mixer.Sound('bullet_shot.wav')
explosionSound=pygame.mixer.Sound('explosion.wav')

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Tank:

    def __init__(self, x, y, speed, color, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN,d_pull=pygame.K_RETURN):
        self.x = x
        self.y = y
        self.score=3
        self.speed = speed
        self.color = color
        self.width = 40
        self.direction = Direction.RIGHT

        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                    d_up: Direction.UP, d_down: Direction.DOWN}

        self.KEYPULL=d_pull

    def draw(self):
        tank_center = (self.x + int(self.width / 2), self.y + int(self.width / 2))
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.width),8)
        pygame.draw.circle(screen,self.color,tank_center, int(self.width / 3))


        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen,self.color, tank_center, (self.x + self.width + int(self.width /2), self.y  + int(self.width /2 )),4)

        if self.direction == Direction.LEFT:
            pygame.draw.line(screen,self.color, tank_center, (self.x - int(self.width /2), self.y + int(self.width /2 )),4)

        if self.direction == Direction.UP:
            pygame.draw.line(screen,self.color, tank_center, (self.x + int(self.width /2), self.y - int(self.width /2 )),4)

        if self.direction == Direction.DOWN:
            pygame.draw.line(screen,self.color, tank_center,  (self.x + int(self.width /2), self.y + self.width + int(self.width /2 )),4)


    def change_direction(self,direction):
        self.direction = direction


    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed

        


        if self.x > 800:     
            self.x = 0 - self.width   
        if self.x < 0 - self.width:           
            self.x = 800
        if self.y > 600:
            self.y = 0 - self.width
        if self.y < 0 - self.width:
            self.y = 600

        self.draw()
    
class Pulya:
    def __init__(self,x=0,y=0,color=(0,0,0),direction=Direction.LEFT,speed=12):
        self.x=x
        self.y=y
        self.color=color
        self.speed=speed
        self.direction=direction
        self.status=True
        self.distance=0
        self.radius=10

    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed
        self.distance+=1
        if self.distance>(2*width):
            self.status=False
        self.draw()

    def draw(self):
        if self.status:
            pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)

def give_coordinates(tank):
    if tank.direction == Direction.RIGHT:
        x=tank.x + tank.width + int(tank.width / 2)
        y=tank.y + int(tank.width / 2)

    if tank.direction == Direction.LEFT:
        x=tank.x - int(tank.width / 2)
        y=tank.y + int(tank.width / 2)

    if tank.direction == Direction.UP:
        x=tank.x + int(tank.width / 2)
        y=tank.y - int(tank.width / 2)

    if tank.direction == Direction.DOWN:
        x=tank.x + int(tank.width / 2)
        y=tank.y + tank.width + int(tank.width / 2)

    p=Pulya(x,y,tank.color,tank.direction)
    pulya.append(p)



def collision():

    for p in pulya:
        
        for tank in tanks:
            
            if (tank.x+tank.width+p.radius > p.x > tank.x - p.radius ) and ((tank.y+tank.width + p.radius > p.y > tank.y - p.radius)) and p.status==True:
                explosionSound.play()
                p.color=(0,0,0)
                tank.score -= 1
                
                p.status=False
                
                tank.x=random.randint(50,width-70)
                tank.y=random.randint(50,height-70)

            if tank.score == 0:
               exit()
            
            



def score():
    score1= tanks[1].score
    score2= tanks[0].score
    res = font.render(str(score1), True, (161, 195, 209))
    res1 = font.render(str(score2), True, (230, 67, 152))
    screen.blit(res, (30,30))
    screen.blit(res1, (750,30))




mainloop = True
tank1 = Tank(350,350,4,(230, 67, 152))
tank2 = Tank(100,100,4,(161, 195, 209),pygame.K_d,pygame.K_a,pygame.K_w,pygame.K_s,pygame.K_SPACE)

pulya1=Pulya()
pulya2=Pulya()

tanks = [tank1, tank2]
pulya = [pulya1,pulya2]

FPS = 60

clock = pygame.time.Clock()

clock=pygame.time.Clock()
while mainloop:
    millis=clock.tick(FPS)
    screen.fill((244, 228, 193))
    
    score()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                quit()
            pressed = pygame.key.get_pressed()
            for tank in tanks:
                if event.key in tank.KEY.keys():
                    tank.change_direction(tank.KEY[event.key])

                if event.key in tank.KEY.keys():
                    tank.move()
                
                if pressed[tank.KEYPULL]:
                    bulletSound.play()
                    give_coordinates(tank)
                        

    collision()

    for p in pulya:
        p.move()
    
    for tank in tanks:
        tank.draw() 
    tank1.move()
    tank2.move()
   
    
    pygame.display.flip()

pygame.quit()