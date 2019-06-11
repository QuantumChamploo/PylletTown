import pygame

class statebasedSprite(pygame.sprite.Sprite):
	"""sprites that are game state dependent. Will read off the save file when intializing the sprites whether
	the sprite should be rendered or not"""

	def __init__(self, location, cell, *groups):

		super(statebasedSprite, self).__init__(*groups)
		self.image = pygame.image.load(cell['src'])
		self.defaultImage = self.image.copy()
		self.width = int(cell['width'])
		self.height = int(cell['height'])
		self.rect = pygame.Rect(location, (self.width,self.height))
		self.location = location
		self.currLocation = location
		self.saveIndex = int(cell['saveIndex'])
		self.hasInteraction = False 
