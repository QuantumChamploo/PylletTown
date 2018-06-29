def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

import pygame
from pygame.locals import *
black = (0,0,0)


class menuSet():

							#something someting
	def __init__(self, menus):
		self.menus = menus 
		self.currMenu = menus[0]
		self.currItem = [self.currMenu.inventory[self.currMenu.counter + self.currMenu.findIndex(self.currMenu.top)],
					 self.currMenu.actions[self.currMenu.counter + self.currMenu.findIndex(self.currMenu.top)]]

		self.currMenu = menus[0]


	def actionText(self):
		
		
		gameDisplay = pygame.display.set_mode((800,600))
		if self.currItem[1] == 'print':
			largeText = pygame.font.Font('freesansbold.ttf',25)
			BottomSurf, BottomRect = text_objects(self.currItem[0], largeText)
			BottomSurf2, BottomRect2 = text_objects("click b to go back and im in the the action", largeText)

			BottomRect.center = ((200),(370))
			BottomRect2.center = ((200),(400))




			gameDisplay.blit(BottomSurf2, BottomRect2)
			gameDisplay.blit(BottomSurf, BottomRect)
			gameDisplay.fill((255,0,0))
			print ('got to actionasdf')

	def actionMenuSwitch(self, menu):
		if menu.name == 'first':
			self.currMenu = self.menus[1]
		if menu.name == 'second':
			self.currMenu = self.menus[0]
