import pygame
from pygame.locals import *
#import tmx
from menuScroller import *
from menuSet import *

pygame.init()

black = (0,0,0)


inventory = ['aaaaaaa','bbbbbbbb','ccccccc','ddddddd','eeeeeee','f','g','h','i','j','k']
actions = ['print', 'menuSwitch', 'print', 'menuSwitch', 'print', 'menuSwitch', 'print', 'menuSwitch', 'print', 'menuSwitch', 'print']
inventory2 = ['z', 'y', 'x', 'w', 't', 'u', 'v']
actions2 = ['menuSwitch','menuSwitch','menuSwitch','menuSwitch','menuSwitch','menuSwitch','menuSwitch']

menu1 = []



hldscrl = menuScroller(inventory, actions, 'first')
hldscrl2 = menuScroller(inventory2, actions2, 'second')
menu1 = [hldscrl, hldscrl2]

hldSet = menuSet(menu1)



clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((800,600)) 

def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

textBoxImage = pygame.image.load('../images/sideMenuBox.png')
arrowImage = pygame.image.load('../images/arrow.png')
bottomImage = pygame.image.load('../images/sideMenuBottom.png')
pygame.transform.rotate(textBoxImage, 90)
largeText = pygame.font.Font('freesansbold.ttf',25)

hldText = "asdfasdf"






displaying = True
miniDisplay = False

while displaying:
	for event in pygame.event.get():
		if event.type == pygame.KEYUP and event.key == pygame.K_z:
			diplaying = False
			pygame.quit()
			quit()
		if event.type == pygame.KEYUP and event.key == pygame.K_UP:
			if miniDisplay == False:
				hldscrl.scrollUP()
		if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
			if miniDisplay == False:
				hldSet.currMenu.scrollDOWN()
		if event.type == pygame.KEYUP and event.key == pygame.K_a:
			if hldSet.currMenu.actions[hldSet.currMenu.counter] == 'print':
				hld3r = 8
				miniDisplay = True
				hldSet.actionText()
			if hldSet.currMenu.actions[hldSet.currMenu.counter] == 'menuSwitch':
				hldSet.actionMenuSwitch(hldSet.currMenu)
			#showItemText("Info about  " + hldscrl.inventory[hldscrl.inventory.index(hldscrl.top) + hldscrl.counter])
			#hldText = "Info about  " + hldscrl.inventory[hldscrl.inventory.index(hldscrl.top) + hldscrl.counter]

		if event.type == pygame.KEYUP and event.key == pygame.K_b:
			if miniDisplay == True:
				miniDisplay = False

			


	gameDisplay.fill((255, 255, 255))
	largeText = pygame.font.Font('freesansbold.ttf',25)
	BottomSurf, BottomRect = text_objects(hldText, largeText)
	BottomSurf2, BottomRect2 = text_objects("click b to go back", largeText)

	BottomRect.center = ((200),(370))
	BottomRect2.center = ((200),(400))
	#if miniDisplay == False:
	gameDisplay.fill((255, 255, 255))
	gameDisplay.blit(textBoxImage, (550,1))


		
	menuTextUpdate(gameDisplay, hldSet.currMenu, miniDisplay)
	if miniDisplay:
		hdhd = 2
		# gameDisplay.blit(BottomSurf2, BottomRect2)
		# gameDisplay.blit(BottomSurf, BottomRect)


	pygame.display.flip()
	clock.tick(15)



