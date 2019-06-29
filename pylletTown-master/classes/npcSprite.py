import pygame


def pacingUpdate(sprite, dt, game):
	if sprite.pace == True:
		sprite.timeCount += dt

		if sprite.direction == 'left' and dt < 65:
			if sprite.pause == False:
				sprite.pacing -= dt/25

		if sprite.direction == 'right' and dt < 65:
			if sprite.pause == False:
				sprite.pacing += dt/25

		if sprite.pacing <= -150:
			sprite.direction = 'right'
			sprite.image = pygame.transform.flip(sprite.image, True, False)

		if sprite.pacing >= 150:
			sprite.direction = 'left'
			sprite.image = pygame.transform.flip(sprite.image, True, False)

		sprite.currLocation = (sprite.location[0] + sprite.pacing, sprite.location[1])
		

		sprite.rect = pygame.Rect((sprite.location[0] + sprite.pacing, sprite.location[1]), (sprite.width,sprite.height))

class npcSprite(pygame.sprite.Sprite):
	"""  Trying to make npc class   
		src - the source of the image that contains the sprites
	"""
	
	def __init__(self, location, cell, orientation, *groups):
		super(npcSprite, self).__init__(*groups)
		self.image = pygame.image.load(cell['src'])
		self.defaultImage = self.image.copy()
		self.width = int(cell['width'])
		self.height = int(cell['height'])
		self.rect = pygame.Rect(location, (self.width,self.height))
		self.timeCount = 0
		self.direction = 'left'
		self.location = location
		self.currLocation = location
		self.orient = orientation
		self.dx = 0

		self.setSprite()

		self.pacing = 0
		self.pause = False
		self.name = cell['name']
		
		if cell['hasInteraction'] == 'true':
			self.hasInteraction = True
		if cell['hasInteraction'] == 'false':
			self.hasInteraction = False
		if cell['pace'] == 'true':
			self.pace = True
		if cell['pace'] == 'false':
			self.pace = False
		
			



	def update(self, dt, game):
		pacingUpdate(self, dt, game)

	def setSprite(self):
		# Resets the player sprite sheet to its default position 
		# and scrolls it to the necessary position for the current orientation
		self.image = self.defaultImage.copy()
		if self.orient == 'up':
		    self.image.scroll(0, -64)
		elif self.orient == 'down':
		    self.image.scroll(0, 0)
		elif self.orient == 'left':
		    self.image.scroll(0, -128)
		elif self.orient == 'right':
		    self.image.scroll(0, -192)		
