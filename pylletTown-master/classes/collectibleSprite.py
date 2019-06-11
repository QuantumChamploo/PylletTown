import pygame

imageDict = {'magic jar': 'sprites/smokeyTree.png'}
widthDict = {'magic jar' : 64}
heightDict = {'magic jar' : 64}

class collectibleSprite(pygame.sprite.Sprite):
	def __init__(self, location, name, *groups):
		super(collectibleSprite, self).__init__(*groups)
		self.image = pygame.image.load(imageDict[name])
		self.defaultImage = self.image.copy()
		self.width = widthDict[name]
		self.height = heightDict[name]
		self.rect = pygame.Rect(location, (self.width,self.height))
		self.location = location
		self.currLocation = location
		self.beenMoved = False
		self.name = name


	def update(self, dt, game):
		if self.beenMoved == True:
			self.currLocation = (-100, -100)
			self.rect = pygame.Rect(self.currLocation, (self.width,self.height))
			self.beenMoved = False
			self.remove(self.groups())
			self.kill()



