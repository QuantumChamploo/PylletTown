import pygame
from classes.cutScene import cutScene
from classes.statebasedSprite import statebasedSprite
from classes.removableSprite import removableSprite
from classes.SpriteLoop import SpriteLoop 
from classes.npcSprite import npcSprite
from classes.spriteMove import spriteMove
from classes.scrollText import scrollText
from classes.projectileSprite import projectileSprite
from classes.wallSprite import wallSprite
from classes.enemySprite import enemySprite
from classes.collectibleSprite import collectibleSprite
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
COLOR_LIMEGREEN = (0, 255, 127)




_sound_library = {}

def play_sound(path):
  pygame.mixer.music.set_volume(0.1)
  global _sound_library
  sound = _sound_library.get(path)
  if sound == None:
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    sound = pygame.mixer.Sound(canonicalized_path)
    _sound_library[path] = sound
  sound.play()


""" 
														These are dictionaries with key values associated with a particular cut scene or text box
"""

cutSceneDictionary = {'walking intro' : cutScene((spriteMove(5,'up'),spriteMove(1,'left')))}
npcSceneCast = {'guided tour': ('smellyboy', 'other'), 'walking intro': ('smellyboy','other')}
npcSceneDictionary = {('guided tour', 'smellyboy') : cutScene((spriteMove(1,'up'),spriteMove(1,'left'))), ('walking intro', 'smellyboy')
																						 : cutScene((spriteMove(1,'up'),spriteMove(1,'left'))) }

textBoxDictionary = {'Prof Glyph': scrollText('Aye, fuck off mate I really want this dumb text stuff to work'),
					'Unlock SuperWaveDashing': scrollText('Congratulations! you are about to get super wavedashing! Press x to obtain it, and s to leave the menu')}


""" 
														Aux method used in processesing images to their text boxes
"""

def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

def text_objectsColor(text, font, color):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()




	
	

""" 
														All of the types of updates a player or sprite might take
"""
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

		lastRect3 = sprite.rect.copy()

		if hldScene.curr.direction == 'up':
			sprite.rect.y -= 4
		if hldScene.curr.direction == 'down':
			sprite.rect.y += 4
		if hldScene.curr.direction == 'left':
			sprite.rect.x -= 4
		if hldScene.curr.direction == 'right':
			sprite.rect.y += 4	
		if len(game.tilemap.layers['triggers'].collide(sprite.rect, 'solid')) > 0:
			sprite.rect = lastRect3
		for hldSprite in game.objects:
			if isinstance(hldSprite, wallSprite):
				hldSprite.rect.colliderect(sprite.rect)
				sprite.rect = lastRect3
			

		sprite.currLocation = (sprite.rect.x, sprite.rect.y)
		hldScene.decrementCurrMove()	
		hldScene.verifyCurrentMove()
			

"""
 								waveDash update: checks in your save file for super wavedashing
 								Later we will add this to the usual wavedashing
"""

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

		for sprite in game.collision:
			if player.rect.colliderect(sprite.rect):
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

"""
						jumpingUpdate: pretty simple
"""

def jumpingUpdate(player):

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


"""
						cutsceneUpdate: A little lengthy. Extra booleans are needed if the cutscene
						ends for the player before the NPCs
"""

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
	for sprite in game.named:
		if sprite.name in npcSceneCast[cutscene]:

			if npcSceneDictionary[(cutscene, sprite.name)].hasNextMove():
				npcBool = True
			else:
				npcBool = False



	if npcBool:
		for sprite in game.named:
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


			# here are some of our booleans. Need to make sure we reset the cutscenes 
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
		
		player.inCutscene = False





"""
												The player class. Here is where the interaction between the game and player take place.
												Contains the "master" update function, where all the above will be refenced
"""
class Player(pygame.sprite.Sprite):

	def __init__(self, location, orientation, *groups):
		super(Player, self).__init__(*groups)
		self.image = pygame.image.load('sprites/milosprite01.png')
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
		self.fireHold = 0
		self.wallCounter = 0
		#self.projectiles = []
		self.hearts = 4
		self.invincible = False
		self.invcTime = 0
		self.parry = False
		self.parryTime = 0
		self.wallHld = False
		self.parryHld = False
		self.WOFlevel = 1
		self.transTime = 0
		self.transitionIn = False
		self.transitionOut = False
		self.magicPer = 100


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
		# print (self.transitionIn)
		# if self.transitionIn :
		# 	print ('ahahaha')
		# 	self.transTime += dt
		# 	if self.transTime < 1000:
		# 		game.tilemap.draw(game.screen)
		# 		if game.mapFile == 'WallsOrFireBalls.tmx': 
		# 			gameDisplay = pygame.display.set_mode((800,600))

		# 			largeText = pygame.font.Font('freesansbold.ttf',35)
		# 			TextSurf, TextRect = text_objects('Welcome to level ' + str(self.WOFlevel), largeText)
		
		# 			TextRect.center = ((400),(520))
		# 			gameDisplay.blit(TextSurf, TextRect)
		# 			print ('trying to show this')
		# 	else:
		# 		self.transTime = 0
		# 		self.transitionIn = False

		if game.mapFile == 'WallsOrFireBalls.tmx':
			if len(game.enemies) == 0:
				if self.transitionOut == False:
					self.WOFlevel += 1
					self.transitionOut = True
					game.samePlayer = True
			if self.hearts < 1:
				self.transitionOut = True
				game.samePlayer = True

		
	



		if self.invincible:
			self.invcTime += dt
			if self.invcTime > 800:
				self.invcTime = 0
				self.invincible = False
		if self.parry:
			self.parryTime += dt
			
			if self.parryTime > 800:
				self.parryTime = 0
				self.parry = False




		self.fireHold += 5
		if self.fireHold > 30:
			self.fireHold = 0
		for sprite in game.objects:
			if isinstance(sprite, projectileSprite):
				for hldSprite in game.objects:
					if isinstance(hldSprite, removableSprite):
						# if rectCollision(sprite, hldSprite):
						# 	hldSprite.beenMoved = True
						# if rectCollision(hldSprite, sprite):
						# 	hldSprite.beenMoved = True	

						if hldSprite.rect.colliderect(sprite.rect):
							hldSprite.beenMoved = True
					if isinstance(hldSprite, enemySprite):
						# if rectCollision(sprite, hldSprite):
						# 	hldSprite.beenMoved = True
						# if rectCollision(hldSprite, sprite):
						# 	hldSprite.beenMoved = True	
						if sprite.name == 'fireball':
							
							if hldSprite.rect.colliderect(sprite.rect):
								hldSprite.beenMoved = True
								collectibleSprite(hldSprite.location, 'magic jar', game.objects, game.removable, game.collision)

					if isinstance(hldSprite, wallSprite):
						if hldSprite.rect.colliderect(sprite.rect):
							sprite.beenMoved = True	

				if sprite.name == "enemyFireball":
					if self.waveDashing == True:
						if sprite.rect.colliderect(self.rect):
							sprite.beenMoved = True
					elif self.invincible == False:
						if self.parry == False:
							if sprite.rect.colliderect(self.rect):
								self.hearts -= 1
								self.invincible = True

								
								play_sound('sounds/DK - Super Hit.wav')
								
						if self.parry == True:
							play_sound('sounds/Link - Whoosh.wav')
							self.invincible = True
							projectileSprite((self.rect[0], self.rect[1]), self.orient, 'fireball', game.objects, game.projectiles, game.named)
							self.hearts += 1


		

		key = pygame.key.get_pressed()



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


		if self.inCutscene == True:
			cutsceneUpdate(self, dt, game, self.whichCutscene)
			self.jumping = False
			self.waveDashing = False
			self.bool = False




        # Setting orientation and sprite based on key input: 

		else:
		    for event in pygame.event.get():
		        if event.type == pygame.KEYUP and event.key == pygame.K_c:
		            pass
		            # self.parry = True
		            # print ('oh boy im parrying ')
		        if event.type == pygame.KEYUP and event.key == pygame.K_g:
		            pass
		            # if self.wallCounter < 10:
		            #     wallSprite((self.rect[0], self.rect[1]), self.orient, game.objects, game.collision)
		            #     self.wallCounter += 1
		    if not key[pygame.K_g]:
		        self.wallHld = False
		    if not key[pygame.K_c]:
		    	if self.parryTime == 0:
		    		self.parryHld = False
		    	if self.parryTime > 850:
		    		self.parryHld = False 
		    if key[pygame.K_c]:
		    	
		    	if not self.parryHld:
		    		
		    		self.parry = True
		    		self.parryHld = True		    		
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
		    elif key[pygame.K_f]:
		    	if self.fireHold == 0:
		    		if self.magicPer >= 5:
		    			projectileSprite((self.rect[0], self.rect[1]), self.orient, 'fireball', game.objects, game.projectiles, game.named)
		    			self.magicPer -= 5
		    			play_sound('sounds/Dot.wav')


		    
		    elif key[pygame.K_g]:
		    	if not self.wallHld:
		    	
		        	if self.wallCounter < 10:
		        		wallSprite((self.rect[0], self.rect[1]), self.orient, game.objects, game.collision)
		        		self.wallCounter += 1
		        		self.wallHld = True




		    
		    elif key[pygame.K_a] and not self.walking:

		        #import pdb; pdb.set_trace()
		        
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
		            # if len(game.tilemap.layers['removableSprites'].collide(self.rect, 'test')) > 0:
		            # 	print ('omgomgomg')
		            # 	hldCol = game.tilemap.layers['removableSprites'].collide(self.rect, 'test')
		            # 	print ('omgomgomg')
		            # 	for sprite in hldCol:
		            # 		sprite.beenMoved = True

		            # 	print ('in the nadnafsnd')

		            ## this needs to be looked at
		            for sprite in game.interactable:

		            	if sprite.hasInteraction == True:
		            		if abs(sprite.currLocation[0] - self.rect.x) < 20:
		            			if abs(sprite.currLocation[1] - self.rect.y) < 20:
		            				hld = sprite.pacing
		            				
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
		            				
		            				sprite.pause = False
		            				sprite.pacing = hld






		            if len(game.tilemap.layers['interactions'].collide(self.rect,'event')) > 0:
		           		clock = pygame.time.Clock()
		           		gameDisplay = pygame.display.set_mode((800,600))
		           		entryCell = game.tilemap.layers['interactions'].collide(self.rect,'event')[0]
		           		self.whichCutscene = str(entryCell['event'])
		           			

		           		self.inCutscene = True


		            	


		            if len(game.tilemap.layers['actions'].collide(self.rect, 'game')) > 0:
		            	print('omg i hope this fucking workssssss')
		            	entryCell = game.tilemap.layers['actions'].collide(self.rect, 'game')[0]
		            	print (entryCell['game'])
		            	path = str(entryCell['game'])
		            	if path == "streetpyghter.py":
		            		os.system('cd ../StreetPyghter/src')
		            	os.system('python3 ' + path)





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
		    for sprite in game.collision:

		    	if isinstance(sprite, collectibleSprite):
		    		if self.rect.colliderect(sprite.rect):
		    			sprite.beenMoved = True 
		    			if sprite.name == 'magic jar':
		    				self.magicPer += 5


		    	if isinstance(sprite, removableSprite):
		    		if self.rect.colliderect(sprite.rect):
		    			sprite.beenMoved = True

		    				
		    	if isinstance(sprite, wallSprite):
		    		if self.rect.colliderect(sprite):
		    			self.rect = lastRect
		    	if isinstance(sprite, npcSprite):
		    		if self.rect.colliderect(sprite):
		    			self.rect = lastRect
		    	if isinstance(sprite, statebasedSprite):
		    		if self.rect.colliderect(sprite):
		    			self.rect = lastRect
		    	if isinstance(sprite, enemySprite):
		    		if self.rect.colliderect(sprite):
		    			if self.waveDashing == True:
		    				sprite.beenMoved = True
		    			else:
		    				self.rect = lastRect		    			
		    		
		    if len(game.tilemap.layers['triggers'].collide(self.rect, 
		                                                    'solid')) > 0:
		        self.rect = lastRect
		        
		    if len(game.tilemap.layers['triggers'].collide(self.rect, 
		                                                    'waveDashable')) > 0:
		        self.rect = lastRect

		    if len(game.tilemap.layers['interactions'].collide(self.rect, 
		                                                    'mini')) > 0:
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
