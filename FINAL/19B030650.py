import pygame
import random
import time
from tkinter import *
from tkinter import messagebox
pygame.init()
background = pygame.image.load('images/fon.png')

root = Tk()
root.title("Tanki")

C = Canvas(root, bg="blue", height=250, width=300)
filename = PhotoImage(file = "images\\fon.png")
background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
root["bg"] = "gray22"
root.geometry("400x500")

b1 = Button(text="Single Player", width=15, height=3,padx="20",pady="8",font="16")
b2 = Button(text="Multi Player", width=15, height=3,padx="20",pady="8",font="16")
b3 = Button(text="QUIT", width=15, height=3,padx="20",pady="8",font="16")
b1.place(x=115,y=170)
b2.place(x=115,y=270)
b3.place(x=115,y=370) 

def single():
	root.withdraw()
	import pygame
	import time
	import random
	from enum import Enum 
	from pygame import mixer
	from importlib import reload

	pygame.init()
	width = 800
	height = 600
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Single Player Mode")
	font = pygame.font.SysFont('timesnewroman', 30) 
	mixer.music.load('soundtracks/background.mp3')
	mixer.music.set_volume(0.1)
	mixer.music.play(-1)
	explosionSound=pygame.mixer.Sound('soundtracks/classic_hurt.wav')

	class Direction(Enum):
		UP = 1
		DOWN = 2
		LEFT = 3
		RIGHT = 4
	class Tank():
		def __init__(self, x, y, speed, img, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN,d_pull=pygame.K_RETURN):
			self.x = x
			self.y = y
			self.score=3
			self.img = img
			self.speed = speed
			self.width = img.get_width()
			self.orig = img
			self.power = False
			self.time = 0
			self.direction = Direction.RIGHT
			self.KEY = {
				d_right: Direction.RIGHT, 
				d_left: Direction.LEFT, 
				d_up: Direction.UP, 
				d_down: Direction.DOWN}
			self.KEYPULL=d_pull
		def draw(self):
			screen.blit(self.img, (self.x, self.y))
		def change_direction(self,direction):
			self.direction = direction
		def move(self):
			if self.direction == Direction.LEFT:
				self.x -= self.speed
				self.img = pygame.transform.rotate(self.orig, -90)
			if self.direction == Direction.RIGHT:
				self.x += self.speed
				self.img = pygame.transform.rotate(self.orig, 90)
			if self.direction == Direction.UP:
				self.y -= self.speed
				self.img = pygame.transform.rotate(self.orig, 180)
			if self.direction == Direction.DOWN:
				self.y += self.speed
				self.img = pygame.transform.rotate(self.orig, 0)
			if self.x > width:     
				self.x = 0 - self.width 
			if self.x < 0 - self.width:           
				self.x = width
			if self.y > height:
				self.y = 0 - self.width
			if self.y < 0 - self.width:
				self.y = height
	class Bullet:
		def __init__(self,x=0,y=0,color=(0,0,0),direction=Direction.LEFT,speed=12):
			self.x=x
			self.y=y
			self.color=color
			self.speed=speed
			self.direction=direction
			self.status=True
			self.distance=0
			self.radius=5
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
	class Wall:
		def __init__(self,x,y):
			self.x = x
			self.y = y
			self.img = pygame.image.load('images/small_brick.png')
			self.width = self.img.get_width()
			self.height = self.img.get_height()
			self.status = True
			self.time = 0
		def draw(self):
			if self.status:
				screen.blit(self.img, (self.x, self.y))
	class Food:
		def __init__(self,x,y):
			self.x = x
			self.y = y
			self.width = 50
			self.height = 50
			self.time = 0
			self.wait = random.randint(5000,20000)
			self.status = False
			self.img = pygame.image.load('images/gear.png')
		def draw(self):
			screen.blit(self.img, (self.x, self.y))
			
	def score():
		score1 = tanks[1].score
		score2 = tanks[0].score
		res = font.render("Player 1: " + str(score1), True, (0, 0, 0))
		res1 = font.render("Player 2: " + str(score2), True, (0, 0, 0))
		screen.blit(res, (30,30))
		screen.blit(res1, (650,30))

	def give_coordinates(tank):
		if tank.direction == Direction.RIGHT:
			x = tank.x + tank.width + 5
			y = tank.y + int(tank.width / 2)
		if tank.direction == Direction.LEFT:
			x = tank.x - 5
			y = tank.y + int(tank.width / 2)
		if tank.direction == Direction.UP:
			x = tank.x + int(tank.width / 2)
			y = tank.y - 5
		if tank.direction == Direction.DOWN:
			x = tank.x + int(tank.width / 2)
			y = tank.y + tank.width + 5
		if tank.power == True:
			bullet=Bullet(x,y,(0,0,0),tank.direction,24)
		else:
			bullet=Bullet(x,y,(0,0,0),tank.direction,10)
		bullets.append(bullet)

	def collision():
		for bullet in bullets:
			for tank in tanks:
				if (tank.x + tank.width + bullet.radius > bullet.x > tank.x - bullet.radius ) and ((tank.y + tank.width + bullet.radius > bullet.y > tank.y - bullet.radius)) and bullet.status ==True:
					explosionSound.play()
					bullet.color=(0,0,0)
					tank.score -= 1
					bullet.status=False
					tank.x=random.randint(50,width-70)
					tank.y=random.randint(50,height-70)
				if tank.score == 0:
					import menu_updated
					reload(menu_updated)
					game = False
					pygame.quit()
			for wall in walls:
				if (wall.x + wall.width + bullet.radius > bullet.x > wall.x - bullet.radius ) and ((wall.y + wall.width + bullet.radius > bullet.y > wall.y - bullet.radius)) and bullet.status ==True:
					bullet.status=False
					walls.remove(wall)
					new_wall = Wall(random.randint(0,width - 64),random.randint(0,height - 64))
					walls.append(new_wall)
		for wall in walls:
			for tank in tanks:
				if tank.x + tank.width > wall.x > tank.x - wall.width and tank.y + tank.width > wall.y > tank.y - wall.height:
					tank.score -= 1
					explosionSound.play()
					tank.x = random.randint(tank.width,width - tank.width)
					tank.y = random.randint(tank.width,height - tank.width)
					walls.remove(wall)
					new_wall = Wall(random.randint(0,width - 64),random.randint(0,height - 64))
					walls.append(new_wall)
		for food in foods:
			for tank in tanks:
				if tank.x + tank.width > food.x > tank.x - food.width and tank.y + tank.width > food.y > tank.y - food.height:
					foods.remove(food)
					tank.power = True
					new_food = Food(random.randint(0,750),random.randint(0,550))
					foods.append(new_food)

	FPS = 60
	clock = pygame.time.Clock()
	tank1 = Tank(100,100,2,pygame.image.load('images/mytank.png'))
	tank2 = Tank(600,100,2,pygame.image.load('images/enemy.png'),pygame.K_d,pygame.K_a,pygame.K_w,pygame.K_s,pygame.K_SPACE)
	bullet1 = Bullet()
	bullet2 = Bullet()
	tanks = [tank1,tank2]
	bullets = [bullet1,bullet2]
	wall1 = Wall(random.randint(0,750),random.randint(0,500))
	wall2 = Wall(random.randint(0,750),random.randint(0,500))
	wall3 = Wall(random.randint(0,750),random.randint(0,500))
	wall4 = Wall(random.randint(0,750),random.randint(0,500))
	walls = [wall1,wall2,wall3,wall4]
	food1 = Food(random.randint(0,750),random.randint(0,550))
	foods = [food1]
	game = True
	while game:
		mills = clock.tick(FPS)
		screen.fill((229, 255, 204))
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
						give_coordinates(tank)
		collision()
		for tank in tanks:
			if tank.power == True and tank.time < 5000:
				tank.speed = 4
				tank.time += mills
			else:
				tank.speed = 2
				tank.power = False
			tank.draw() 
			tank.move()
		for bullet in bullets:
			bullet.move()
		for wall in walls:
			if wall.time > 10000:
				walls.remove(wall)
				new_wall = Wall(random.randint(0,750),random.randint(0,550))
				walls.append(new_wall)
			else:
				wall.draw()
				wall.time += mills
		for food in foods:
			if food.wait > 0:
				food.wait -= mills
			else:
				if food.time > 5000:
					foods.remove(food)
					new_food = Food(random.randint(0,750),random.randint(0,550))
					foods.append(new_food)
				else:
					food.draw()
					food.time += mills
		pygame.display.flip()
	pygame.quit()


def multi():
	root.withdraw()
	import pika
	import uuid
	import json
	import pygame
	from threading import Thread

	ip = '34.254.177.17'
	RabbitPort = '5672'
	vhost = 'dar-tanks'
	credents = pika.PlainCredentials(username = 'dar-tanks', password ='5orPLExUYnyVYZg48caMpX')

	pygame.init()
	screen = pygame.display.set_mode((1300,800))

	class TankRPC:
	    def __init__(self):
	        self.connection = pika.BlockingConnection(
	            pika.ConnectionParameters(
	                host = ip,
	                port = RabbitPort,
	                virtual_host = vhost,
	                credentials = credents
	            )
	        )
	        self.channel = self.connection.channel()

	        result = self.channel.queue_declare(queue = '', auto_delete = True, exclusive = True)
	        self.queue_callback = result.method.queue

	        self.channel.queue_bind(exchange = 'X:routing.topic',
	                                queue = self.queue_callback)

	        self.channel.basic_consume(
	            queue = self.queue_callback,
	            on_message_callback = self.callback,
	            auto_ack = True
	        )

	        self.response = None
	        self.corr_id = None
	        self.token = None
	        self.tankid = None
	        self.roomid = None
	        
	    
	    def callback(self, ch, method, properties, body):
	        if self.corr_id == properties.correlation_id:
	            self.response = json.loads(body)
	            print(self.response)

	    def call(self, rout_key, message = {}):
	        self.response = None
	        self.corr_id = str(uuid.uuid4())
	        self.channel.basic_publish(
	            exchange = 'X:routing.topic',
	            routing_key = rout_key,
	            properties = pika.BasicProperties(
	                reply_to = self.queue_callback,
	                correlation_id = self.corr_id,
	            ),
	            body=json.dumps(message)
	        ) 
	        while self.response is None:
	            self.connection.process_data_events()

	    def server_check(self):
	        self.call('tank.request.healthcheck')
	        if self.response['status'] == '200':
	            return True
	        return False


	    def register(self, room_id):
	        message = {
	            'roomId': room_id
	        }
	        self.call('tank.request.register', message)
	        if 'token' in self.response:
	            self.token = self.response['token']
	            self.tankid = self.response['tankId']
	            
	            return True
	        return False
	    
	    def povorot(self, token, direction):
	        message = {
	            'token': token,
	            'direction': direction
	        }
	        self.call('tank.request.turn', message)

	    def vistrel(self, token):
	        message = {
	            'token': token
	        }
	        self.call('tank.request.fire', message)

	class ConsumeDataTanks(Thread):
	    def __init__(self, room_id):
	        super().__init__()
	        self.connection = pika.BlockingConnection(
	            pika.ConnectionParameters(
	                host = ip,
	                port = RabbitPort,
	                virtual_host = vhost,
	                credentials = credents
	            )
	        )
	        self.channel = self.connection.channel()

	        result = self.channel.queue_declare(queue = '', auto_delete = True, exclusive = True)
	        self.queue_callback = result.method.queue
	        

	        self.channel.queue_bind(exchange = 'X:routing.topic', queue = self.queue_callback, routing_key = 'event.state.' + room_id)

	        self.channel.basic_consume(
	            queue = self.queue_callback,
	            on_message_callback = self.callback,
	            auto_ack = True
	        )
	        self.response = None
	    
	    def callback(self, ch, method, properties, body):
	        self.response = json.loads(body)
	        print(self.response)

	    def run(self):
	        self.channel.start_consuming()

	UP = 'UP'
	DOWN = 'DOWN'
	RIGHT = 'RIGHT'
	LEFT = 'LEFT'

	TURN_KEYS = {
	    pygame.K_w: UP,
	    pygame.K_a: LEFT,
	    pygame.K_s: DOWN,
	    pygame.K_d: RIGHT
	}




	def game_online():
	    def blit_text(txt, x, y, FontSize, color):
	        font = pygame.font.Font('freesansbold.ttf', FontSize)
	        text = font.render(txt, 1, color)
	        place = text.get_rect(center=(x, y))
	        screen.blit(text, place)

	    def draw_tanks(x, y, width, height, direction, color_tank):
	        tank_center = (x + width // 2, y + height // 2)        

	        pygame.draw.rect(screen, color_tank, (x, y, width, height), 6)
	        pygame.draw.circle(screen, color_tank, tank_center, width // 2,4)
	        if direction == 'RIGHT':
	            pygame.draw.line(screen, color_tank, 
	                             (tank_center[0] + width // 2, tank_center[1]), (x + width + width // 2, y + height // 2), 4)
	        if direction == 'LEFT':
	            pygame.draw.line(screen, color_tank, 
	                             (tank_center[0] - width // 2, tank_center[1]), (x - width // 2, y + height // 2), 4)
	        if direction == 'UP':
	            pygame.draw.line(screen, color_tank, 
	                             (tank_center[0], tank_center[1] - width // 2), (x + width // 2, y - height // 2), 4)
	        if direction == 'DOWN':
	            pygame.draw.line(screen, color_tank, 
	                             (tank_center[0], tank_center[1] + width // 2), (x + width // 2, y + height + height // 2), 4)
	    
	    def draw_bullets(x, y, width, height, color_bullet):
	        pygame.draw.rect(
	            screen, color_bullet,
	            (x, y, width, height)
	        )

	  

	    is_game = True
	    while is_game:
	        screen.fill((0,0,0))
	        for event in pygame.event.get():
	            if event.type == pygame.QUIT:
	                is_game = False
	            
	            if event.type == pygame.KEYDOWN:
	                if event.key == pygame.K_ESCAPE:
	                    is_game = False
	                
	                if event.key in TURN_KEYS:
	                    client.povorot(client.token, TURN_KEYS[event.key])
	                
	                if event.key == pygame.K_SPACE:
	                    client.vistrel(client.token)


	        tanks = event_collect.response['gameField']['tanks']
	        rem_time = event_collect.response['remainingTime']
	        bullets = event_collect.response['gameField']['bullets']

	        try:
	            for tank in tanks:
	                if client.tankid == tank['id']:
	                    draw_tanks(tank['x'], tank['y'], tank['width'],tank['height'], tank['direction'], (35,187,17))
	                else:
	                    draw_tanks(tank['x'], tank['y'], tank['width'],tank['height'], tank['direction'], (255,170,35))
	        except:
	            pass
	        pygame.draw.rect(screen, (4,104,115), (1000, 0, 300, 800))
	        
	        blit_text("Remaining Time: {}".format(rem_time), 1150, 730, 24, (255,255,255))
	        g = len(tanks) - 1
	        f = g
	        t = 0
	        try:
	            blit_text("My Tank          Health           Score", 1150, 30, 14, (255,255,255))
	            blit_text("Enemy Tanks       Health           Score", 1150, 80, 14, (255,255,255))
	            for tank in tanks:
	                if client.tankid == tank['id']:                
	                    blit_text(tank['id'] + "           " + str(tank['health']) + "               " + str(tank['score']), 1140,50,17, (35,187,17))
	                else:
	                    blit_text(tank['id'] + "             " + str(tank['health']) + "                 " + str(tank['score']), 1150,100 + (20 * t),17, (255,170,35))
	                    t += 1
	                    if f == 0:
	                        t = 0
	                        f = g
	                    f -= 1
	        except:
	            pass
	        
	        try:
	            for bullet in bullets:
	                if client.tankid == bullet['owner']:
	                    draw_bullets(bullet['x'], bullet['y'], bullet['width'], bullet['height'], (35,187,17))
	                else:
	                    draw_bullets(bullet['x'], bullet['y'], bullet['width'], bullet['height'], (255,170,35))
	        except:
	            pass
	        pygame.display.flip()
	                


	client = TankRPC()

	client.server_check()
	client.register('room-1')

	event_collect = ConsumeDataTanks('room-1')

	event_collect.start()

	game_online()

def quit():
	root.destroy()

b1.config(command=single)
b2.config(command=multi)
b3.config(command=quit)

C.pack()
 
root.mainloop()