import pygame

projectileDict = {'fireball': 'sprites/fireball.png'}
widthDict = {'fireball' : 24}
heightDict = {'fireball' : 23}

class projectileSprite(pygame.sprite.Sprite):
	def __init__(self, location, direction, projType, *groups):
		super(projectileSprite, self).__init__(*groups)
		self.image = pygame.image.load(projectileDict[projType])
		self.defaultImage = self.image.copy()
		self.width = widthDict[projType]
		self.height = heightDict[projType]
		self.currLocation = location
		self.location = location
		self.rect = pygame.Rect(location, (self.width,self.height))
		self.hasInteraction = False
		self.direction = direction
		

	def update(self, dt, game):
		if self.rect.x > -30 and self.rect.y > -30:
			if self.direction == 'left':
				self.rect.x -= 16
			if self.direction == 'right':
				self.rect.x += 16
			if self.direction == 'down':
				self.rect.y += 16
			if self.direction == 'up':
				self.rect.y -= 16
		if self.rect.x > 3000 or self.rect.y > 3000:
			self.rect.x = -100
			self.rect.y = -100
			del self

		#self.rect = pygame.Rect(currLocation, (self.width,self.height))
		