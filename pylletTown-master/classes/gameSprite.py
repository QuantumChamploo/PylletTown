import pygame 

class gameSprite(pygame.sprite.Sprite):
	def __init__(self):
		super(OnBoard, self).__init__()
		print ('probaly some real stuff here')


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





class SpriteLoop(pygame.sprite.Sprite):
    def __init__(self, location, cell, *groups):
        super(SpriteLoop, self).__init__(*groups)
        self.image = pygame.image.load(cell['src'])
        self.defaultImage = self.image.copy()
        self.width = int(cell['width'])
        self.height = int(cell['height'])
        self.rect = pygame.Rect(location, (self.width,self.height))
        self.frames = int(cell['frames'])
        self.frameCount = 0
        self.mspf = int(cell['mspf']) # milliseconds per frame
        self.timeCount = 0
       

    def update(self, dt, game):
        self.timeCount += dt
        if self.timeCount > self.mspf:
            # Advance animation to the appropriate frame
            self.image = self.defaultImage.copy()
            self.image.scroll(-1*self.width*self.frameCount, 0)
            self.timeCount = 0
            
            self.frameCount += 1
            if self.frameCount == self.frames:
                self.frameCount = 0

