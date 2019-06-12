def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

import pygame
from pygame.locals import *
black = (0,0,0)

def showItemText(itemText, gameDisplay):
	largeText = pygame.font.Font('freesansbold.ttf',25)
	BottomSurf, BottomRect = text_objects(itemText, largeText)
	BottomSurf2, BottomRect2 = text_objects("click b to gooooo back", largeText)

	BottomRect.center = ((200),(370))
	BottomRect2.center = ((200),(400))
	gameDisplay.blit(BottomSurf2, BottomRect2)
	gameDisplay.blit(BottomSurf, BottomRect)


def menuTextUpdate(gameDisplay, menuScroller, miniDisplay):
	arrowImage = pygame.image.load('../images/arrow.png')
	bottomImage = pygame.image.load('../images/sideMenuBottom.png')

	spacing = 60
	topIndex = menuScroller.inventory.index(menuScroller.top)

	largeText = pygame.font.Font('freesansbold.ttf',25)
	TextSurf1, TextRect1 = text_objects(menuScroller.inventory[topIndex], largeText)
	TextSurf2, TextRect2 = text_objects(menuScroller.inventory[topIndex+1], largeText)
	TextSurf3, TextRect3 = text_objects(menuScroller.inventory[topIndex+2], largeText)
	TextSurf4, TextRect4 = text_objects(menuScroller.inventory[topIndex+3], largeText)
	TextSurf5, TextRect5 = text_objects(menuScroller.inventory[topIndex+4], largeText)
	TextSurf6, TextRect6 = text_objects(menuScroller.inventory[topIndex+5], largeText)
	TextRect1.center = ((675),(60 + (0 * spacing)))
	TextRect2.center = ((675),(60 + (1 * spacing)))
	TextRect3.center = ((675),(60 + (2 * spacing)))
	TextRect4.center = ((675),(60 + (3 * spacing)))
	TextRect5.center = ((675),(60 + (4 * spacing)))
	TextRect6.center = ((675),(60 + (5 * spacing)))
	gameDisplay.blit(TextSurf1, TextRect1)
	gameDisplay.blit(TextSurf2, TextRect2)
	gameDisplay.blit(TextSurf3, TextRect3)
	gameDisplay.blit(TextSurf4, TextRect4)
	gameDisplay.blit(TextSurf5, TextRect5)
	gameDisplay.blit(TextSurf6, TextRect6)
	gameDisplay.blit(arrowImage, (580,50 + spacing * menuScroller.counter))

	if miniDisplay == True:
		largeText = pygame.font.Font('freesansbold.ttf',25)
		BottomSurf, BottomRect = text_objects(menuScroller.boxedItem, largeText)
		BottomSurf2, BottomRect2 = text_objects("click b to gooooo back", largeText)

		BottomRect.center = ((200),(370))
		BottomRect2.center = ((200),(400))
		gameDisplay.blit(bottomImage, (10, 330))
		gameDisplay.blit(BottomSurf2, BottomRect2)
		gameDisplay.blit(BottomSurf, BottomRect)




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
