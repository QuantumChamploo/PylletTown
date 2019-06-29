import pygame
from pygame.locals import *
import tmx
import pygameMenu
from pygameMenu.locals import *
import glob
import os
 
from Player import Player
from classes.statebasedSprite import statebasedSprite
from classes.SpriteLoop import SpriteLoop 
from classes.npcSprite import npcSprite
from classes.removableSprite import removableSprite
from classes.enemySprite import enemySprite



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
COLOR_LIGHTCORAL  =  (240, 128, 128)


_sound_library = {}

def play_sound(path):
  global _sound_library
  sound = _sound_library.get(path)
  if sound == None:
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    sound = pygame.mixer.Sound(canonicalized_path)
    _sound_library[path] = sound
  sound.play()


""" 
														Aux method used in processesing images to their text boxes
"""


def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()



def text_objectsColor(text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()


"""
The game class. Where the main menu is held and where the outer world 
InitArea
Save and Load 
"""


class Game(object):

    def __init__(self, screen):
        # the screen is a pygame display surface
        self.screen = screen
        # the save field will be filled with the CSV entries from our save files
        self.save = []
        self.samePlayer = False


    
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
        self.mapFile = mapFile
        
        # These fields are sprite class abstract groups. We will use the tmx API to do remove/kill and parse through the games
        # sprite instantiations 

        # Players is for just player class 
        self.players = tmx.SpriteLayer()

        # Objects is all things that will be updated
        self.objects = tmx.SpriteLayer()

        # Sub groups used to make code simpler and easier to read
        self.projectiles = tmx.SpriteLayer()
        self.collision = tmx.SpriteLayer()
        self.interactable = tmx.SpriteLayer()
        self.named = tmx.SpriteLayer()
        self.removable = tmx.SpriteLayer()
        self.enemies = tmx.SpriteLayer()
        #self.sprites = []


        startCell = self.tilemap.layers['triggers'].find('playerStart')[0]
        if self.samePlayer == False:

            self.player = Player((startCell.px, startCell.py), 
                                 startCell['playerStart'], self.players) 
        else:
            hld1 = self.player.hearts
            hld2 = self.player.WOFlevel
            hld3 = self.player.magicPer            
            self.player = Player((startCell.px, startCell.py), 
                                 startCell['playerStart'], self.players) 
            self.player.hearts = hld1
            self.player.WOFlevel = hld2  
            self.player.magicPer = hld3         

            # self.player.rect = pygame.Rect((startCell.px, startCell.py), (64,64)) 
            # self.player.orient =  startCell['playerStart']
            # self.players.set_view(self.screen)  
            # self.players.draw(self.screen)
            # self.player.setSprite()                         
																				        # Initializing other animated sprites
        try:
            for cell in self.tilemap.layers['sprites'].find('src'):
                SpriteLoop((cell.px,cell.py), cell, self.objects)
            for cell in self.tilemap.layers['npcSprites'].find('src'):
                npcSprite((cell.px,cell.py), cell,'down', self.objects, self.collision, self.interactable, self.named)

            for cell in self.tilemap.layers['statebasedSprites'].find('src'):


                if self.save[cell['saveIndex']] == 'true':
                   statebasedSprite((cell.px,cell.py), cell, self.objects, self.collision, self.interactable)

            hld = 0

            print (mapFile)

            if mapFile == 'WallsOrFireBalls.tmx':
                self.player.transitionIn = True
                print (self.player.transitionIn)

                
                for cell in self.tilemap.layers['enemySprites'].find('src'):
                    print (str(self.player.WOFlevel) + "this is the level i should be at")
                    if hld < self.player.WOFlevel + 3:
                        enemySprite((cell.px,cell.py), cell, 'down', self.objects, self.collision, self.removable, self.named, self.enemies)
                        hld += 1


            else:
                for cell in self.tilemap.layers['enemySprites'].find('src'):
                    enemySprite((cell.px,cell.py), cell, 'down', self.objects, self.collision, self.removable, self.named)

            hldSprites = self.tilemap.layers['removableSprites'].find('src')
            
            for cell in hldSprites:
               
                removableSprite((cell.px,cell.py), cell, self.objects, self.collision, self.removable)                
   






        # In case there is no sprite layer for the current map
        except KeyError:
            print ('key error')
            pass
        else:
            self.tilemap.layers.append(self.objects)
        
            

        # Initializing player sprite


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

            pygame.mixer.music.load('sounds/Temporal-Parity.wav')
            #pygame.mixer.music.play(-1)     
            #play_sound('sounds/Temporal-Parity.mp3')       
                        

            

            
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
                thisImage = pygame.image.load('images/MGlogo.jpg')
                fullHeart = pygame.image.load('images/fullheart.png')
                emptyHeart = pygame.image.load('images/emptyheart.png')

                self.tilemap.update(dt, self)
                screen.fill((0,0,0))

                self.tilemap.draw(self.screen)

                pygame.draw.rect(gameDisplay, COLOR_WHITE, (105, 25, 230, 60))

                pygame.draw.rect(gameDisplay, COLOR_LIMEGREEN, (120,30,self.player.magicPer * 2,50))
                
                if self.player.hearts >= 1:
                    gameDisplay.blit(fullHeart, (30, 30))
                else: 
                    gameDisplay.blit(emptyHeart, (30, 30))                    
                if self.player.hearts >= 2:
                    gameDisplay.blit(fullHeart, (30, 60))
                else: 
                    gameDisplay.blit(emptyHeart, (30, 60))
                if self.player.hearts >= 3:
                    gameDisplay.blit(fullHeart, (30, 90)) 
                else: 
                    gameDisplay.blit(emptyHeart, (30, 90))                    
                if self.player.hearts >= 4:
                    gameDisplay.blit(fullHeart, (30, 120))
                else: 
                    gameDisplay.blit(emptyHeart, (30, 120))                                                                               
                gameDisplay.blit(thisImage, (690, 500))

                if self.mapFile == 'WallsOrFireBalls.tmx':
                    if self.player.transitionIn :

                        self.player.transTime += dt
                        if self.player.transTime < 1000:
                            #self.tilemap.draw(self.screen)
                            if self.mapFile == 'WallsOrFireBalls.tmx': 

                                largeText = pygame.font.Font('fonts/Exo2-MediumCondensed.ttf',65)
                                TextSurf, TextRect = text_objectsColor('Level ' + str(self.player.WOFlevel), largeText, COLOR_LIGHTCORAL)
        
                                TextRect.center = ((400),(100))
                                gameDisplay.blit(TextSurf, TextRect)

                        else:
                            self.player.transTime = 0
                            self.player.transitionIn = False

                    if self.player.transitionOut:
                        
                        if self.player.hearts > 0:
                            self.player.transTime += dt
                            if self.player.transTime < 1000:
                                #self.tilemap.draw(self.screen)
                                if self.mapFile == 'WallsOrFireBalls.tmx': 

                                    largeText = pygame.font.Font('fonts/Exo2-MediumCondensed.ttf',65,)
                                    TextSurf, TextRect = text_objectsColor('Going to level ' + str(self.player.WOFlevel), largeText, COLOR_LIGHTCORAL)
            
                                    TextRect.center = ((400),(100))
                                    gameDisplay.blit(TextSurf, TextRect)
                                    
                            else:
                                self.player.transTime = 0
                                self.player.transitionOut = False
                                self.initArea('WallsOrFireBalls.tmx')
                        else:
                            self.player.transTime += dt
                            if self.player.transTime < 1000:
                                #self.tilemap.draw(self.screen)
                                if self.mapFile == 'WallsOrFireBalls.tmx': 

                                    largeText = pygame.font.Font('fonts/Exo2-MediumCondensed.ttf',65)
                                    TextSurf, TextRect = text_objectsColor('OH GOD YOUR DYING', largeText, red)
            
                                    TextRect.center = ((400),(100))
                                    gameDisplay.blit(TextSurf, TextRect)
                                    
                            else:
                                self.player.transTime = 0
                                self.player.transitionOut = False
                                self.initArea('babyHell.tmx')
                                self.samePlayer = False



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
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.1)

    
    
    Game(screen).main()

    