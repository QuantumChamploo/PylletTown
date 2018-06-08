import pygame
from pygame.locals import *
import pygameMenu
from pygameMenu.locals import *

COLOR_BLUE = (12, 12, 200)
COLOR_BACKGROUND = [128, 0, 128]
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
MENU_BACKGROUND_COLOR = (228, 55, 36)
COLOR_MAROON =  (40, 0, 40)

pygame.init()
clock = pygame.time.Clock()
inMenu = True

def mainmenu_background():
    """Background color of the main menu, on this function user can plot
        images, play sounds, etc."""
    gameDisplay.fill((40, 0, 40))

def hldfunction():
	print('hereASDFASDF')
	print('adsfasdfasdf')

def leavemenu():
	inMenu = False


gameDisplay = pygame.display.set_mode((800,600))


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
                            onclose=PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow=False,
                            title='RPmG',
                            window_height=600,
                            window_width=800
                            )

secondMenu = pygameMenu.Menu(gameDisplay,
                            bgfun=mainmenu_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.fonts.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=(40,0,40),
                            menu_height=600,
                            menu_width=800,
                            onclose=PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow=False,
                            title='Load Game',
                            window_height=600,
                            window_width=800
                            )
thirdMenu = pygameMenu.Menu(gameDisplay,
                            bgfun=mainmenu_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.fonts.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=(40,0,40),
                            menu_height=600,
                            menu_width=800,
                            onclose=PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow=False,
                            title='New Game',
                            window_height=600,
                            window_width=800
                            )
mainMenu.add_option(thirdMenu.get_title(), thirdMenu)
mainMenu.add_option(secondMenu.get_title(), secondMenu)

secondMenu.add_option('Print stuff',hldfunction)
secondMenu.add_option('Return to Menu', PYGAME_MENU_BACK)
secondMenu.add_option('Close', PYGAME_MENU_CLOSE)
mainMenu.add_option('Exit', PYGAME_MENU_EXIT)

thirdMenu.add_option('Exit', PYGAME_MENU_EXIT)


fileRead = open('saveFile.txt', 'r')
for line in fileRead:
	print (line)
inMenu = True
while inMenu:
	clock.tick(60)

	gameDisplay.fill(COLOR_BACKGROUND)
	mainMenu.enable()

	events = pygame.event.get()

	mainMenu.mainloop(events)
	print ('looping')
	pygame.display.flip()



print ('here')

