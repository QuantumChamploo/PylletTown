import pygame 

class removableSprite(pygame.sprite.Sprite):
	def __init__(self, location, cell, *groups):
		super(removableSprite, self).__init__(*groups)
		self.image = pygame.image.load(cell['src'])
		self.defaultImage = self.image.copy()
		self.width = int(cell['width'])
		self.height = int(cell['height'])
		self.rect = pygame.Rect(location, (self.width,self.height))
		self.currLocation = location
		self.hasInteraction = False
		self.beenMoved = False	
		self.location = location


	def update(self, dt, game):
		if self.beenMoved == True:
			
			self.currLocation = (-100, -100)
			self.rect = pygame.Rect(self.currLocation, (self.width,self.height))
			self.beenMoved = False
			self.remove(self.groups())
			self.kill()
			