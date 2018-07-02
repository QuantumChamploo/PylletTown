import pygame
from cutScene import cutScene
from spriteMove import spriteMove
from wallSprite import wallSprite
from projectileSprite import projectileSprite
import random


def enemySpriteUpdate(sprite, dt, game):
	if sprite.moving == False:
		sprite.timeCount += dt
		if sprite.timeCount >= 100:
			game.player.projectiles.append(projectileSprite((sprite.rect[0], sprite.rect[1]), sprite.orient, 'enemyFireball', game.objects))
			if sprite.style == 'random':
				sprite.timeCount = 0
				hld = random.randint(1,101)
				if hld % 4 == 0:
					hld2 = random.randint(1,101)
					if hld2 % 4 == 0:
						sprite.cutscene = cutScene([spriteMove(1,'left')])
					if hld2 % 4 == 1:
						sprite.cutscene = cutScene([spriteMove(1,'right')])
					
					if hld2 % 4 == 2:
						sprite.cutscene = cutScene([spriteMove(1,'up')])
					if hld2 % 4 == 3:
						sprite.cutscene = cutScene([spriteMove(1,'down')])
					sprite.moving = True
					
	


	if sprite.moving == True:
		if sprite.cutscene.curr.movesLeft == sprite.cutscene.curr.totalMoves:
			sprite.orient = sprite.cutscene.curr.direction
			sprite.setSprite()
			sprite.cutscene.decrementCurrMove()
			sprite.dx = 0
			sprite.step = 'rightFoot'
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

		if sprite.cutscene.curr.direction == 'up':
			sprite.rect.y -= 4
		
		if sprite.cutscene.curr.direction == 'down':
			
			sprite.rect.y += 4
		if sprite.cutscene.curr.direction == 'left':
			sprite.rect.x -= 4
			
		if sprite.cutscene.curr.direction == 'right':
			sprite.rect.x += 4	
			
		if len(game.tilemap.layers['triggers'].collide(sprite.rect, 'solid')) > 0:
			sprite.rect = lastRect3
		for hldSprite in game.sprites:
			if isinstance(hldSprite, wallSprite):
				hldSprite.rect.colliderect(sprite.rect)
				sprite.rect = lastRect3
			if isinstance(hldSprite, enemySprite):
				hldSprite.rect.colliderect(sprite.rect)
				sprite.rect = lastRect3

		sprite.currLocation = (sprite.rect.x, sprite.rect.y)
		sprite.cutscene.decrementCurrMove()	
		sprite.cutscene.verifyCurrentMove()
		if sprite.cutscene.hasNextMove() == False:
			sprite.moving = False

	if sprite.beenMoved == True:
		print ('over hererere')
			
		sprite.currLocation = (-100, -100)
		sprite.rect = pygame.Rect(sprite.currLocation, (sprite.width,sprite.height))
		sprite.beenMoved = False

						




class enemySprite(pygame.sprite.Sprite):

	def __init__(self, location, cell, orientation, *groups):
		super(enemySprite, self).__init__(*groups)
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
		self.style = str(cell['style'])
		self.name = str(cell['name'])
		self.moving = False
		self.dx = 0
		self.beenMoved = False



		self.setSprite()

		self.hasInteraction = False

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



	def update(self, dt, game):
		enemySpriteUpdate(self, dt, game)
		hld = 2


