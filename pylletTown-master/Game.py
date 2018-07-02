import pygame
from pygame.locals import *
import tmx
import pygameMenu
from pygameMenu.locals import *
import glob
import os
 
from Player import Player
from statebasedSprite import statebasedSprite
from SpriteLoop import SpriteLoop 
from npcSprite import npcSprite
from removableSprite import removableSprite
from enemySprite import enemySprite



black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
COLOR_BLUE = (12, 12, 200)
COLOR_BACKGROUND = [128, 0, 128]
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_MAROON =  (40, 0, 40)
MENU_BACKGROUND_COLOR = (228, 55, 36)


""" 
														Aux method used in processesing images to their text boxes
"""


def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

"""
The game class. Where the main menu is held and where the outer world 
InitArea
Save and Load 
"""


class Game(object):

    def __init__(self, screen):
        self.screen = screen
        self.save = []


    
    def fadeOut(self):
        																	
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
																				
        self.tilemap = tmx.load(mapFile, screen.get_size())
        
        self.players = tmx.SpriteLayer()
        self.objects = tmx.SpriteLayer()
        self.sprites = []
																				        # Initializing other animated sprites
        try:
            for cell in self.tilemap.layers['sprites'].find('src'):
                SpriteLoop((cell.px,cell.py), cell, self.objects)
            for cell in self.tilemap.layers['npcSprites'].find('src'):
                self.sprites.append(npcSprite((cell.px,cell.py), cell,'down', self.objects))
                print ('oh helooooooo2')
            for cell in self.tilemap.layers['statebasedSprites'].find('src'):


                if self.save[cell['saveIndex']] == 'true':
                    self.sprites.append(statebasedSprite((cell.px,cell.py), cell, self.objects))

            for cell in self.tilemap.layers['enemySprites'].find('src'):
                enemySprite((cell.px,cell.py), cell, 'down', self.objects)
                print ('oh helooooooo')






        # In case there is no sprite layer for the current map
        except KeyError:
            print ('key error')
            pass
        else:
            self.tilemap.layers.append(self.objects)
        try:
            hldSprites = self.tilemap.layers['removableSprites'].find('src')
            
            for cell in hldSprites:
               
                self.sprites.append(removableSprite((cell.px,cell.py), cell, self.objects))
              
               

        except KeyError:
           
            pass
        else:
            hld2 = 9
            

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

       


    def initMenu(self):
        """"create generic menu for in game    """
        
        gameDisplay = pygame.display.set_mode((800,600))



        stillOn = True

        clock = pygame.time.Clock()

        def close_fun():
        
            main_menu.disable()
     

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
	            
	            

	        
	        play_function()

	        

            



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
        

        

        gameDisplay = pygame.display.set_mode((800,600))
        
        
        
        
        # this is everything
        self.introMenu()



       
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Pyllet Town")
    os.system('python3 test3.py')
    
    
    Game(screen).main()

    