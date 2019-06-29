import pygame

class wallSprite(pygame.sprite.Sprite):
	def __init__(self,location, direction, *groups):
		super(wallSprite, self).__init__(*groups)
		self.image = pygame.image.load('sprites/wall.png')
		self.defaultImage = self.image.copy()
		self.width = 64
		self.height = 13
		self.hasInteraction = False
		self.direction = direction
		self.hldTime = 0
		self.name = 'wall'
		if direction == 'left' or direction == 'right':
			self.image = pygame.transform.rotate(self.image, 90)
			self.width = 13
			self.height = 64
		if direction == 'left':
			self.currLocation = (location[0] - 77, location[1])
		if direction == 'right':
			self.currLocation = (location[0] + 128, location[1]) 
		if direction == 'up':
			self.currLocation = (location[0], location[1] - 77)
		if direction == 'down':
			self.currLocation = (location[0], location[1] + 128)

		self.location = self.currLocation
		self.rect = pygame.Rect(self.currLocation, (self.width,self.height))


	def update(self, dt, game):
		self.hldTime += dt
		if self.hldTime >= 4000:

			self.remove(self.groups())
			self.kill()

			game.player.wallCounter -= 1

