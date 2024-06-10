import pygame, random

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crow farm")
clock = pygame.time.Clock()

class Jugador(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.shield = 100

	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		self.rect.x += self.speed_x
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		disparo = Disparo(self.rect.centerx, self.rect.top)
		all_sprites.add(disparo)
		disparos.add(disparo)

class Cuervo(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(cuervo_images)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width) 
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 8)
		self.speedx = random.randrange(-5, 5)

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 22 :
			self.rect.x = random.randrange(WIDTH - self.rect.width)

			#Change this variable
			self.rect.y = random.randrange(-150, -100)
			self.speedy = random.randrange(1, 8)

class Disparo(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("assets/laser1.png")
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y 
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 # how long to wait for the next frame VELOCITY OF THE EXPLOSION

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill() # if we get to the end of the animation we don't keep going.
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

def draw_text(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, (255, 255, 255))
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, WHITE, fill)
	pygame.draw.rect(surface, BLACK, border, 2)

def show_go_screen():
	screen.blit(background, [0, 0])
	draw_text(screen, "CROW FARM", 65, WIDTH // 2, HEIGHT / 4,)
	draw_text(screen, "(INSTRUCCIONES)", 27, WIDTH // 2, HEIGHT // 2)
	draw_text(screen, "PRESIONAR ESPACIO PARA INICIAR", 17, WIDTH // 2, HEIGHT * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False

cuervo_images = []
cuervo_list = ["assets/cuervo.png", "assets/cuervo2.png", "assets/cuervo3.png", "assets/cuervo4.png",
				"assets/cuervo5.png", "assets/cuervo6.png"]

for img in cuervo_list:
	cuervo_images.append(pygame.image.load(img).convert())

## --------------- CARGAR IMAGENES EXPLOSIÓN -------------------------- ##
explosion_anim = []
for i in range(9):
	file = "assets/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70, 70))
	explosion_anim.append(img_scale)


# Cargar fondo.
background = pygame.image.load("assets/background2.png").convert()

# Game Loop
game_over = True
running = True
while running:
	if game_over:
		show_go_screen()
		game_over = False
		all_sprites = pygame.sprite.Group()
		cuervo_list = pygame.sprite.Group()
		disparos = pygame.sprite.Group()

		jugador = Jugador()
		all_sprites.add(jugador)

		for i in range(8):
			cuervo = Cuervo()
			all_sprites.add(cuervo)
			cuervo_list.add(cuervo)
 
		#Marcador 
		score = 0
	# Keep loop running at the right speed
	clock.tick(60)
	# Process input (events)
	for event in pygame.event.get():
		# check for closing window
		if event.type == pygame.QUIT:
			running = False
		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				jugador.shoot()
		

	# Update
	all_sprites.update()

	# Colisiones cuervos - disparos
	hits = pygame.sprite.groupcollide(cuervo_list, disparos, True, True)
	for hit in hits:
		score += 1
		#explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)

		cuervo = Cuervo()
		all_sprites.add(cuervo)
		cuervo_list.add(cuervo)
 		
	# Colisiones jugador - cuervos

	################## CHANGES HERE ################################
	hits = pygame.sprite.spritecollide(jugador, cuervo_list, True) # Change here
	for hit in hits:
		jugador.shield -= 25
		cuervo = Cuervo()
		all_sprites.add(cuervo)
		cuervo_list.add(cuervo)
		if jugador.shield <= 0:
			#running = False

			game_over = True

	#Draw / Render
	screen.blit(background, [0, 0])
	all_sprites.draw(screen)

	# Marcador
	draw_text(screen, str(score), 25, WIDTH // 2, 10)

	# ESCUDO.
	draw_shield_bar(screen, 5, 5, jugador.shield)

	pygame.display.flip()

pygame.quit()
 