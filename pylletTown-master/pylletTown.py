import pygame
from pygame.locals import *
import tmx
import pygameMenu
from pygameMenu.locals import *
import glob
import os



black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
COLOR_BLUE = (12, 12, 200)
COLOR_BACKGROUND = [128, 0, 128]
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_MAROON =  (40, 0, 40)
MENU_BACKGROUND_COLOR = (228, 55, 36)



def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

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


class scrollText():
	def __init__(self, inputText):
		self.stringList = inputText.split(' ')

		self.counter = 0
		self.length = len(self.stringList)
		self.top = ''
		self.bottom = ''
		self.level = 'top'
		self.wait = 0
		self.nextScreen = False
		self.pause = False
		


	def resetPlace(self):
		self.counter = 0
		self.top = ''
		self.bottom = ''

	def hasnextLetter(self):
		if self.counter  == self.length:
			return False
		else:
			return True

	def nextLetter(self):
		return self.stringList[self.counter]

	def increment(self):
		self.counter += 1

	def updateScroll(self):
		if self.hasnextLetter():
			if self.wait == 0:

				if self.counter == 0:
					self.level = 'top'

				elif self.counter % 6 == 0:
					if self.level == 'top':
						self.level = 'bottom'
					elif self.level == 'bottom':
						self.pause = True
						if self.nextScreen == True:
							print (self.nextScreen)

							self.level = 'top'
							self.top = ''
							self.bottom = ''
							self.nextScreen = False
							self.pause = False
					
				if self.pause == False:
					if self.level == 'top':
						self.top += self.nextLetter() + " "
					if self.level == 'bottom':
						self.bottom += self.nextLetter() + " "

					self.increment()
				
			else:
				self.wait += 1
				if self.wait >= 15:
					self.wait = 0



textBoxDictionary = {'Prof Glyph': scrollText('Aye, fuck off mate I really want this dumb text stuff to work'),
					'Unlock SuperWaveDashing': scrollText('Congratulations! you are about to get super wavedashing! Press x to obtain it, and s to leave the menu')}


def textUpdate(gameDisplay, textScript, game):
	hldScroll = textBoxDictionary[textScript]
	hldScroll.updateScroll()


	largeText = pygame.font.Font('freesansbold.ttf',35)
	TextSurf, TextRect = text_objects(hldScroll.top, largeText)
	TextSurf2, TextRect2 = text_objects(hldScroll.bottom, largeText)
	TextRect.center = ((400),(520))
	TextRect2.center = ((400),(570))
	textBoxImage = pygame.image.load('smallTextBox.png')


	game.tilemap.draw(game.screen)
	gameDisplay.blit(textBoxImage, (25,480))
	gameDisplay.blit(TextSurf, TextRect)
	gameDisplay.blit(TextSurf2, TextRect2)	

	





class spriteMove():
	def __init__(self, paces, direction):
		self.totalMoves = paces*16 + 1
		self.movesLeft = paces*16 + 1
		self.direction = direction

	def resetMoves(self):
		self.movesLeft = self.totalMoves

	def hasMoves(self):
		if self.movesLeft == 0:
			return False
		else:
			return True
	def decrementMoves(self):
		self.movesLeft -= 1


class cutScene():
	def __init__(self, moves):

		self.moves = moves
		
		
		self.first = moves[0]
		self.last = moves[len(moves)-1]
		self.curr = self.first
		self.currPlace = 0


	def hasNextMove(self):
		if self.curr == self.last and not self.curr.hasMoves():
			return False
		else:
			return True


	def verifyCurrentMove(self):
		if not self.curr.hasMoves():
			if self.curr == self.last: 
				print ('something')
				
			else:
				self.curr.resetMoves()
				print (str(self.curr.totalMoves))
				self.currPlace += 1
				self.curr = self.moves[self.currPlace]

	def decrementCurrMove(self):
		self.curr.decrementMoves()

						


cutSceneDictionary = {'walking intro' : cutScene((spriteMove(5,'up'),spriteMove(1,'left')))}
npcSceneCast = {'guided tour': ('smellyboy', 'other'), 'walking intro': ('smellyboy','other')}
npcSceneDictionary = {('guided tour', 'smellyboy') : cutScene((spriteMove(1,'up'),spriteMove(1,'left'))), ('walking intro', 'smellyboy') : cutScene((spriteMove(1,'up'),spriteMove(1,'left'))) }

def npcUpdate(spriteName, sprite, dt, game, cutscene):
	hldScene = npcSceneDictionary[(cutscene, spriteName)]
	if hldScene.curr.movesLeft == hldScene.curr.totalMoves:
		sprite.orient = hldScene.curr.direction
		sprite.setSprite()
		hldScene.decrementCurrMove()
		sprite.dx = 0
		sprite.step = 'rightFoot'
	else:
		sprite.dx += 4
		if sprite.dx == 32:
			# Self.step keeps track of when to flip the sprite so that
			# the character appears to be taking steps with different feet.
			if (sprite.orient == 'up' or 
				sprite.orient == 'down') and sprite.step == 'leftFoot':
				sprite.image = pygame.transform.flip(sprite.image, True, False)
				sprite.step = 'rightFoot'
			else:
				sprite.image.scroll(-64, 0)
				sprite.step = 'leftFoot'
		# After traversing 64 pixels, the walking animation is done
		if sprite.dx == 64:
			
			sprite.setSprite()    
			sprite.dx = 0

		if hldScene.curr.direction == 'up':
			sprite.rect.y -= 4
		if hldScene.curr.direction == 'down':
			sprite.rect.y += 4
		if hldScene.curr.direction == 'left':
			sprite.rect.x -= 4
		if hldScene.curr.direction == 'right':
			sprite.rect.y += 4	
		sprite.currLocation = (sprite.rect.x, sprite.rect.y)
		hldScene.decrementCurrMove()	
		hldScene.verifyCurrentMove()
			

def wavedashUpdate(player, game):
	lastRect = player.rect.copy()
	if game.save[4] == 'R WE WAVEDASHING':
		maxHld = 128
	else:
		maxHld = 64
	if player.hldx < maxHld:
		
		if player.orient == 'right':
			player.rect.x += 16
			player.hldx += 16
		if player.orient == 'left':
			player.rect.x -= 16
			player.hldx += 16
		if player.orient == 'up':
			player.hldx = 0
			player.waveDashing = False
		if player.orient == 'down':
			player.hldx = 0
			player.waveDashing = False								


		if len(game.tilemap.layers['triggers'].collide(player.rect, 'solid')) > 0:
			player.rect = lastRect

		game.tilemap.set_focus(player.rect.x, player.rect.y)

		if player.hldx == maxHld:
			player.waveDashing = False
			player.hldx = 0
			player.bool = False
			# delete the above and below bool to make super waveDashing!!
	else:

		player.hldx = 0
		player.waveDashing = False
		player.bool = False



def jumpingUpdate(player):
	for event in pygame.event.get():
		if event.type == pygame.KEYUP and event.key == pygame.K_e:
			print ("oh please let wavedaing work")
	if player.hldy < 32:
		player.rect.y -= 4
		player.hldy += 4
	elif 32 <= player.hldy < 64:
		player.rect.y += 4
		player.hldy += 4
	else:
		player.hldy = 0
		player.jumping = False
		player.bool = False		



def cutsceneUpdate(player, dt, game, cutscene):
	# the cast and dictionary for the npcs r almost set up to do multiple npcs at a time, but
	# was having issues iterating through dictionary values, so left it simple for now
	try:
		hldScene = cutSceneDictionary[cutscene]
		playerBool = hldScene.hasNextMove()
		skipReset = False
	except KeyError:
		playerBool = False
		skipReset = True

	if len(npcSceneCast[cutscene]) == 0:
		skipNpcReset = True
	else:
		skipNpcReset = False
	for sprite in game.sprites:
		if sprite.name in npcSceneCast[cutscene]:

			if npcSceneDictionary[(cutscene, sprite.name)].hasNextMove():
				npcBool = True
			else:
				npcBool = False



	if npcBool:
		for sprite in game.sprites:
			if sprite.name in npcSceneCast[cutscene]:

				npcUpdate(sprite.name, sprite, dt, game, cutscene)


	if playerBool:
		if hldScene.curr.movesLeft == hldScene.curr.totalMoves:
			player.orient = hldScene.curr.direction
			player.setSprite()
			hldScene.decrementCurrMove()
			player.dx = 0
			player.step = 'rightFoot'


		else:

			player.dx += 4
			if player.dx == 32:
				# Self.step keeps track of when to flip the sprite so that
				# the character appears to be taking steps with different feet.
				if (player.orient == 'up' or 
					player.orient == 'down') and player.step == 'leftFoot':
					player.image = pygame.transform.flip(player.image, True, False)
					player.step = 'rightFoot'
				else:
					player.image.scroll(-64, 0)
					player.step = 'leftFoot'
			# After traversing 64 pixels, the walking animation is done
			if player.dx == 64:
				player.walking = False
				player.setSprite()    
				player.dx = 0

			if hldScene.curr.direction == 'up':
				player.rect.y -= 4
			if hldScene.curr.direction == 'down':
				player.rect.y += 4
			if hldScene.curr.direction == 'left':
				player.rect.x -= 4
			if hldScene.curr.direction == 'right':
				player.rect.y += 4	
			hldScene.decrementCurrMove()	
			hldScene.verifyCurrentMove()
			game.tilemap.set_focus(player.rect.x, player.rect.y)	



	if not (playerBool or npcBool):
		if not skipReset:
			for move in hldScene.moves:
				move.resetMoves()
			hldScene.currPlace = 0
			hldScene.curr = hldScene.first
		if not skipNpcReset:
			for spriteName in npcSceneCast[cutscene]:
				if spriteName != 'other':
					for move in npcSceneDictionary[(cutscene,spriteName)].moves:
						move.resetMoves()
					npcSceneDictionary[(cutscene,spriteName)].currPlace = 0
					npcSceneDictionary[(cutscene,spriteName)].curr = npcSceneDictionary[(cutscene,spriteName)].first
		print ("LEFT THE CUTSCENE")
		player.inCutscene = False

																							"""

																							**********
																							* Player Class
																							**********

																							"""
class Player(pygame.sprite.Sprite):
	def __init__(self, location, orientation, *groups):
		super(Player, self).__init__(*groups)
		self.image = pygame.image.load('sprites/profglyph.png')
		self.imageDefault = self.image.copy()
		self.rect = pygame.Rect(location, (64,64))
		self.orient = orientation 
		self.holdTime = 0
		self.walking = False
		self.dx = 0
		self.step = 'rightFoot'
		self.inCutscene = False
		self.whichCutscene = ''
		self.hldx = 0;
		self.hldy = 0;
		self.jumping = False
		self.waveDashing = False
		self.bool = False


		# Set default orientation
		self.setSprite()
        
	def setSprite(self):
		# Resets the player sprite sheet to its default position 
		# and scrolls it to the necessary position for the current orientation
		self.image = self.imageDefault.copy()
		if self.orient == 'up':
		    self.image.scroll(0, -64)
		elif self.orient == 'down':
		    self.image.scroll(0, 0)
		elif self.orient == 'left':
		    self.image.scroll(0, -128)
		elif self.orient == 'right':
		    self.image.scroll(0, -192)

	def update(self, dt, game):


		key = pygame.key.get_pressed()

		if self.inCutscene == True:
			cutsceneUpdate(self, dt, game, self.whichCutscene)
			self.jumping = False
			self.waveDashing = False
			self.bool = False

		if self.jumping == True and self.bool == True:
			if key[pygame.K_e] and key[pygame.K_r] and 37 > self.hldy > 27:
	
				self.waveDashing = True
				
			jumpingUpdate(self)

		if self.jumping == True and self.waveDashing == False:
			if key[pygame.K_w]:
				if self.hldy > 32:
					self.hldy -= 32
				hld = self.hldy % 8
				self.rect.y += hld
				self.jumping = False
				self.hldy = 0


		if self.waveDashing == True:
			
			wavedashUpdate(self, game)
			





        # Setting orientation and sprite based on key input: 

		else:

		    if key[pygame.K_UP]:
		        if not self.walking:
		            if self.orient != 'up':
		                self.orient = 'up'
		                self.setSprite()
		            self.holdTime += dt
		            
		    elif key[pygame.K_DOWN]:
		        if not self.walking:
		            if self.orient != 'down':
		                self.orient = 'down'
		                self.setSprite()    
		            self.holdTime += dt
		    elif key[pygame.K_LEFT]:
		        if not self.walking:
		            if self.orient != 'left':
		                self.orient = 'left'
		                self.setSprite()
		            self.holdTime += dt
		    elif key[pygame.K_RIGHT]:
		        if not self.walking:
		            if self.orient != 'right':
		                self.orient = 'right'
		                self.setSprite()
		            self.holdTime += dt
		    elif key[pygame.K_e]:
		    	self.jumping = True
		    	self.bool = True
		    elif key[pygame.K_a] and not self.walking:
		        if not self.walking:
		            lastRect2 = self.rect.copy()
		            if self.orient == 'up':
		                self.rect.y -= 8
		            elif self.orient == 'down':
		                self.rect.y += 8
		            elif self.orient == 'left':
		                self.rect.x -= 8
		            elif self.orient == 'right':
		                self.rect.x += 8
		           # self.dx += 8

		            for sprite in game.sprites:
		            	if sprite.hasInteraction == True:
		            		if abs(sprite.currLocation[0] - self.rect.x) < 20:
		            			if abs(sprite.currLocation[1] - self.rect.y) < 20:
		            				hld = sprite.pacing
		            				print (sprite.currLocation)
		            				sprite.pause = True
		            				clock = pygame.time.Clock()
		            				gameDisplay = pygame.display.set_mode((800,600))

		            				displaying = True

		            				while displaying:

		            					for event in pygame.event.get():
		            						if event.type == pygame.QUIT:
		            							pygame.quit()
		            							return
		            						if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
		            							pygame.quit()
		            							return
		            						if event.type == pygame.QUIT:
		            							pygameMenu.quit()
		            							quit()
		            						if event.type == pygame.KEYUP and event.key == pygame.K_s:
		            							hldText = textBoxDictionary['Prof Glyph'].resetPlace()
		            							displaying = False



		            						

		            						textUpdate(gameDisplay, 'Prof Glyph', game)
		            						pygame.display.flip()

		            						clock.tick(15)
		            				print ('over heheheeh')
		            				print (sprite.currLocation)
		            				sprite.pause = False
		            				sprite.pacing = hld

	            		if abs(sprite.currLocation[0] - self.rect.x) < 8:
	            			if abs(sprite.currLocation[1] - self.rect.y) < 8:
	            				self.rect = lastRect2


		            if len(game.tilemap.layers['interactions'].collide(self.rect,'event')) > 0:
		           		clock = pygame.time.Clock()
		           		gameDisplay = pygame.display.set_mode((800,600))
		           		entryCell = game.tilemap.layers['interactions'].collide(self.rect,'event')[0]
		           		self.whichCutscene = str(entryCell['event'])

		           		self.inCutscene = True
		           		print (str(entryCell['event']))
		           		print (self.inCutscene)


		            if len(game.tilemap.layers['actions'].collide(self.rect, 'sign')) > 0:
		                clock = pygame.time.Clock()
		                gameDisplay = pygame.display.set_mode((800,600))  
		                thisImage = pygame.image.load('uujihyugtguyh.png')
		                game.save[3] = 'CHANGED'
		                signCell = game.tilemap.layers['actions'].collide(self.rect, 'sign')[0]
		                

		                displaying = True

		                while displaying:
		        
		        
		    
		                    for event in pygame.event.get():
		                        print(event)
		                        if event.type == pygame.QUIT:
		                             
		                            pygame.quit()
		                            return
		                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
		                            
		                            pygame.quit()
		                    
		                            return 
		                        if event.type == pygame.QUIT:
		                            pygame.quit()
		                            quit()

		                        if event.type == pygame.KEYUP and event.key == pygame.K_z:
		                        	hldText = textBoxDictionary[str(signCell['sign'])].nextScreen = True
		                        	
		                        if event.type == pygame.KEYUP and event.key == pygame.K_s:
		                            hldText = textBoxDictionary[str(signCell['sign'])].resetPlace()
		                            displaying = False
		                        if event.type == pygame.KEYUP and event.key == pygame.K_x:
		                            displaying = False
		                            game.save[4] = 'R WE WAVEDASHING'

		                        


		                    textUpdate(gameDisplay, str(signCell['sign']),game)
		                    pygame.display.flip()
		                    clock.tick(7)  
		                hldText = textBoxDictionary[str(signCell['sign'])].nextScreen = False    
		            self.rect = lastRect2
		           
		    else:

		        self.holdTime = 0
		        self.step = 'rightFoot'
		    # Walking mode enabled if a button is held for 0.1 seconds
		    if self.holdTime >= 100:
		        self.walking = True
		    lastRect = self.rect.copy()
		    # Walking at 8 pixels per frame in the direction the player is facing 
		    if self.walking and self.dx < 64:
		        if self.orient == 'up':
		            self.rect.y -= 8
		        elif self.orient == 'down':
		            self.rect.y += 8
		        elif self.orient == 'left':
		            self.rect.x -= 8
		        elif self.orient == 'right':
		            self.rect.x += 8
		        self.dx += 8
		    # Collision detection:
		    # Reset to the previous rectangle if player collides
		    # with anything in the foreground layer
		    for sprite in game.sprites:
		    	if abs(sprite.currLocation[0] - self.rect.x) < 64:
		    		if abs(sprite.currLocation[1] - self.rect.y) < 64:
		    			self.rect = lastRect
		    if len(game.tilemap.layers['triggers'].collide(self.rect, 
		                                                    'solid')) > 0:
		        self.rect = lastRect
		    if len(game.tilemap.layers['triggers'].collide(self.rect, 
		                                                    'waveDashable')) > 0:
		        self.rect = lastRect


		    # Area entry detection:
		    elif len(game.tilemap.layers['triggers'].collide(self.rect, 
		                                                    'entry')) > 0:
		        entryCell = game.tilemap.layers['triggers'].find('entry')[0]
		        print ("going to area" + str(entryCell['entry']))

		        game.fadeOut()
		        game.initArea(entryCell['entry'])
		        
		        return
		    # Switch to the walking sprite after 32 pixels 
		    if self.dx == 32:
		        # Self.step keeps track of when to flip the sprite so that
		        # the character appears to be taking steps with different feet.
		        if (self.orient == 'up' or 
		            self.orient == 'down') and self.step == 'leftFoot':
		            self.image = pygame.transform.flip(self.image, True, False)
		            self.step = 'rightFoot'
		        else:
		            self.image.scroll(-64, 0)
		            self.step = 'leftFoot'
		    # After traversing 64 pixels, the walking animation is done
		    if self.dx == 64:
		        self.walking = False
		        self.setSprite()    
		        self.dx = 0

		    game.tilemap.set_focus(self.rect.x, self.rect.y)


																							"""

																							**********
																							* SpriteLoop Class
																							**********

																							"""
class SpriteLoop(pygame.sprite.Sprite):
																					    """A simple looped animated sprite.
																					    
																					    SpriteLoops require certain properties to be defined in the relevant
																					    tmx tile:
																					    
																					    src - the source of the image that contains the sprites
																					    width, height - the width and height of each section of the sprite that
																					        will be displayed on-screen during animation
																					    mspf - milliseconds per frame, or how many milliseconds must pass to 
																					        advance onto the next frame in the sprite's animation 
																					    frames - the number individual frames that compose the animation
																					    """
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

																							"""

																							**********
																							* npcSprite Class
																							**********

																							"""
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

																							"""

																							**********
																							GAME CLASS
																							**********

																							"""
class Game(object):

    def __init__(self, screen):
        self.screen = screen
        self.save = []

    def play_function():
        mainMenu.disable()
        mainMenu.reset(1)
        clock = pygame.time.Clock()

        playLoop = True
        while playLoop:
            dt = clock.tick(30)
            print ('dt = ' + dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            thisImage = pygame.image.load('MGlogo.jpg')

            self.tilemap.update(dt, self)
            screen.fill((0,0,0))

            self.tilemap.draw(self.screen)
            
            gameDisplay.blit(thisImage, (690, 500))
            pygame.display.flip()

    
    def fadeOut(self):
        																	"""Animate the screen fading to black for entering a new area"""
        clock = pygame.time.Clock()
        blackRect = pygame.Surface(self.screen.get_size())
        blackRect.set_alpha(100)
        blackRect.fill((0,0,0))
        																		# Continuously draw a transparent black rectangle over the screen
        																		# to create a fadeout effect
        for i in range(0,5):
            clock.tick(15)
            self.screen.blit(blackRect, (0,0))  
            pygame.display.flip()
        clock.tick(15)
        screen.fill((255,255,255,50))
        pygame.display.flip()
        																		# *** *** ***
    def initArea(self, mapFile):												# initArea
																				# *** *** ***
																				"""Load maps and initialize sprite layers for each new area"""
        self.tilemap = tmx.load(mapFile, screen.get_size())
        print (type(self.tilemap.layers))
        self.players = tmx.SpriteLayer()
        self.objects = tmx.SpriteLayer()
        self.sprites = []
																				        # Initializing other animated sprites
        try:
            for cell in self.tilemap.layers['sprites'].find('src'):
                SpriteLoop((cell.px,cell.py), cell, self.objects)
            for cell in self.tilemap.layers['npcSprites'].find('src'):
            	self.sprites.append(npcSprite((cell.px,cell.py), cell,'down', self.objects))
            	print ('in the npcSprites')


        # In case there is no sprite layer for the current map
        except KeyError:
            pass
        else:
            self.tilemap.layers.append(self.objects)
        # Initializing player sprite
        startCell = self.tilemap.layers['triggers'].find('playerStart')[0]
        self.player = Player((startCell.px, startCell.py), 
                             startCell['playerStart'], self.players)
        self.tilemap.layers.append(self.players)
        self.tilemap.set_focus(self.player.rect.x, self.player.rect.y) 


    def saveGame(self):
        hldString = ""
        for i in range(len(self.save)-1):
            hldString += self.save[i] + ","
        hldString += self.save[len(self.save)-1]

        path = os.getcwd() + '/SaveFiles/' + self.save[0]

        fileRead = open(path, 'w')

        fileRead.write(hldString)

        print (hldString)


    def initMenu(self):
        """"create generic menu for in game    """
        
        gameDisplay = pygame.Surface((400,600))



        stillOn = True

        clock = pygame.time.Clock()

        def close_fun():
            print (main_menu.is_disabled())
            main_menu.disable()
            print (main_menu.is_disabled())

        def mainmenu_background():
            """Background color of the main menu, on this function user can plot
                images, play sounds, etc."""
            gameDisplay.fill((40, 0, 40))
            




        main_menu = pygameMenu.Menu(gameDisplay,
                                    bgfun=mainmenu_background,
                                    color_selected=COLOR_WHITE,
                                    font=pygameMenu.fonts.FONT_BEBAS,
                                    font_color=COLOR_BLACK,
                                    font_size=30,
                                    menu_alpha=100,
                                    menu_color=(40,0,40),
                                    menu_height=600,
                                    menu_width=800,
                                    onclose=mainmenu_background,
                                    option_shadow=False,
                                    title='RPmG',
                                    window_height=600,
                                    window_width=800
                                    )
        print ('inside the game init menu')

        main_menu.add_option('Save the Game', self.saveGame)
        main_menu.add_option('Close: Pressasdfg esc', PYGAME_MENU_CLOSE)

        looping = True
        while looping:

            # Tick
            clock.tick(60)

            # Application events
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    exit()

            # Main menu
            main_menu.mainloop(events)
            looping = False


            # Flip surface
            pygame.display.flip()



    def introMenu(self):

        gameDisplay = pygame.display.set_mode((800,600))

        clock = pygame.time.Clock()

        def play_function():
            mainMenu.disable()
            mainMenu.reset(1)
            clock = pygame.time.Clock()
            

            

            
            if len(self.save) != 0:
                self.initArea(self.save[1])

            playLoop = True
            while playLoop:
                dt = clock.tick(30)


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        self.initMenu()
                thisImage = pygame.image.load('MGlogo.jpg')

                self.tilemap.update(dt, self)
                screen.fill((0,0,0))

                self.tilemap.draw(self.screen)
                

                
                gameDisplay.blit(thisImage, (690, 500))
                pygame.display.flip()
            

        def mainmenu_background():
            """Background color of the main menu, on this function user can plot
                images, play sounds, etc."""
            gameDisplay.fill((40, 0, 40))

        def hldfunction(filename):
        	if(filename == 'NewBlankGame'):
        		self.save = ['newGameSave.txt','test3.tmx','other','notChanged','in','here']
        	else:

	            path = os.getcwd() + '/SaveFiles/' + filename 
	            fileRead = open(path, 'r')
	            hldString = ""

	            for line in fileRead:
	                hldString += line
	            
	            self.save = hldString.split(',')
	            
	            print ('oh over here')
	            print (self.save)

	        print ('here')
	        play_function()

	        print ('heregain')

            



        newgameMenu = pygameMenu.Menu(gameDisplay,
                                    bgfun=mainmenu_background,
                                    color_selected=COLOR_WHITE,
                                    font=pygameMenu.fonts.FONT_BEBAS,
                                    font_color=COLOR_BLACK,
                                    font_size=30,
                                    menu_alpha=100,
                                    menu_color=(40,0,40),
                                    menu_height=600,
                                    menu_width=800,
                                    onclose=mainmenu_background,
                                    option_shadow=False,
                                    title='New Game',
                                    window_height=600,
                                    window_width=800
                                    )
                                
       # newgameMenu.add_option('Start a New Game',play_function)

        mainMenu = pygameMenu.Menu(gameDisplay,
                                    bgfun=mainmenu_background,
                                    color_selected=COLOR_WHITE,
                                    font=pygameMenu.fonts.FONT_BEBAS,
                                    font_color=COLOR_BLACK,
                                    font_size=30,
                                    menu_alpha=100,
                                    menu_color=(40,0,40),
                                    menu_height=600,
                                    menu_width=800,
                                    onclose=mainmenu_background,
                                    option_shadow=False,
                                    title='RPmG',
                                    window_height=600,
                                    window_width=800
                                    )


        loadgameMenu = pygameMenu.Menu(gameDisplay,
                                    bgfun=mainmenu_background,
                                    color_selected=COLOR_WHITE,
                                    font=pygameMenu.fonts.FONT_BEBAS,
                                    font_color=COLOR_BLACK,
                                    font_size=30,
                                    menu_alpha=100,
                                    menu_color=(40,0,40),
                                    menu_height=600,
                                    menu_width=800,
                                    onclose=mainmenu_background,
                                    option_shadow=False,
                                    title='Load Game',
                                    window_height=600,
                                    window_width=800
                                    )
       

        

        mainMenu.add_option(newgameMenu.get_title(), newgameMenu)
        mainMenu.add_option(loadgameMenu.get_title(), loadgameMenu)
        newgameMenu.add_option('Return to Menu', PYGAME_MENU_BACK)
        newgameMenu.add_option('New Game', hldfunction, 'NewBlankGame')
        loadgameMenu.add_option('Return to Menu', PYGAME_MENU_BACK)
        
        # loadgameMenu.add_option('Load Game',hldfunction)
        mainMenu.add_option('Exit', PYGAME_MENU_EXIT)

        path = os.getcwd() + '/SaveFiles'
        for filename in os.listdir(path):
            loadgameMenu.add_option(filename, hldfunction, filename)
        
        looping = True

        while looping:
            clock.tick(60)

            gameDisplay.fill(COLOR_BACKGROUND)
            mainMenu.enable()

            events = pygame.event.get()

            mainMenu.mainloop(events)
            looping = False

            pygame.display.flip()




    

    def main(self):
        clock = pygame.time.Clock()
        self.initArea('test3.tmx')
        print (self.save)

        

        gameDisplay = pygame.display.set_mode((800,600))
        
        

        def mainmenu_background():
            """Background color of the main menu, on this function user can plot
                images, play sounds, etc."""
            gameDisplay.fill((40, 0, 40))

        mainMenu = pygameMenu.Menu(gameDisplay,
                       bgfun=mainmenu_background,
                       enabled=True,
                       font=pygameMenu.fonts.FONT_NEVIS,
                       menu_alpha=90,
                       onclose=PYGAME_MENU_CLOSE,
                       title='Start Game',
                       title_offsety=5,
                       window_height=600,
                       window_width=800
                       )
        newgameMenu = pygameMenu.Menu(gameDisplay,
                       bgfun=mainmenu_background,
                       enabled=True,
                       font=pygameMenu.fonts.FONT_NEVIS,
                       menu_alpha=90,
                       onclose=PYGAME_MENU_CLOSE,
                       title='New Game',
                       title_offsety=5,
                       window_height=600,
                       window_width=800
                       )
        newgameMenu.add_option('Return to Menu', PYGAME_MENU_BACK)
       
        loadgameMenu = pygameMenu.TextMenu(gameDisplay,
                       bgfun=mainmenu_background,
                       enabled=True,
                       font=pygameMenu.fonts.FONT_NEVIS,
                       menu_alpha=90,
                       onclose=PYGAME_MENU_CLOSE,
                       title='Load Game',
                       title_offsety=5,
                       window_height=600,
                       window_width=800
                       )
        

        menu = pygameMenu.TextMenu(gameDisplay,
                       bgfun=mainmenu_background,
                       enabled=True,
                       font=pygameMenu.fonts.FONT_NEVIS,
                       menu_alpha=90,
                       onclose=PYGAME_MENU_CLOSE,
                       title='RPmG',
                       title_offsety=5,
                       window_height=600,
                       window_width=800
                       )
        menu.add_option(mainMenu.get_title(), mainMenu)
        
        mainMenu.add_option(newgameMenu.get_title(), newgameMenu)
        mainMenu.add_option(loadgameMenu.get_title(), loadgameMenu)

        loadgameMenu.add_option('Return to Menu', PYGAME_MENU_BACK)
        loadgameMenu.add_option('Close', PYGAME_MENU_CLOSE)
        mainMenu.add_option('Exit', PYGAME_MENU_EXIT)
        newgameMenu.add_option('Start a New Game', PYGAME_MENU_EXIT)
        
        
        
        # this is everything
        self.introMenu()



       
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Pyllet Town")
    print ("hello")
    
    Game(screen).main()

    