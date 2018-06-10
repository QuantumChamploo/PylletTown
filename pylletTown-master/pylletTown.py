import pygame
from pygame.locals import *
import tmx
import pygameMenu
from pygameMenu.locals import *
import glob
import os


aCounter = 0
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
COLOR_BLUE = (12, 12, 200)
COLOR_BACKGROUND = [128, 0, 128]
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_MAROON =  (40, 0, 40)
MENU_BACKGROUND_COLOR = (228, 55, 36)


menuSets = [









]




def initMenu():
        """"create generic menu for in game    """
        gameDisplay = pygame.display.set_mode((800,600))

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
                                    onclose=PYGAME_MENU_CLOSE,
                                    option_shadow=False,
                                    title='RPmG',
                                    window_height=600,
                                    window_width=800
                                    )

        # main_menu.add_option('Save', saveGame)
                                    
        main_menu.add_option('Close: press esc to leave', PYGAME_MENU_CLOSE)

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


def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()
        

class Player(pygame.sprite.Sprite):
    def __init__(self, location, orientation, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('sprites/player.png')
        self.imageDefault = self.image.copy()
        self.rect = pygame.Rect(location, (64,64))
        self.orient = orientation 
        self.holdTime = 0
        self.walking = False
        self.dx = 0
        self.step = 'rightFoot'
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
        aCounter = 0

        key = pygame.key.get_pressed()
        # Setting orientation and sprite based on key input: 
        if key[pygame.K_UP]:
            if not self.walking:
                if self.orient != 'up':
                    self.orient = 'up'
                    self.setSprite()
                self.holdTime += dt
                if(aCounter < 5):
                    aCounter += 1
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

                if len(game.tilemap.layers['actions'].collide(self.rect, 
                                                                'sign')) > 0:
                    clock = pygame.time.Clock()
                    gameDisplay = pygame.display.set_mode((800,600))  
                    thisImage = pygame.image.load('uujihyugtguyh.png')
                    game.save[3] = 'CHANGED'
                    #game.initMenu()

                    

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
                            if event.type == pygame.KEYUP and event.key == pygame.K_s:
                                displaying = False
                        #gameDisplay.fill(red)    
                        # gameDisplay.blit(thisImage, (100, 0))
                        
                        #gameDisplay.blit(currState, (0,0))
                        largeText = pygame.font.Font('freesansbold.ttf',35)
                        TextSurf, TextRect = text_objects('press s to leave interaction', largeText)
                        TextRect.center = ((300),(510))
                        textBoxImage = pygame.image.load('smallTextBox.png')
                        
                        game.tilemap.draw(game.screen)
                        gameDisplay.blit(textBoxImage, (25,480))
                        gameDisplay.blit(TextSurf, TextRect)

                        
                        
               
                        pygame.display.flip()
                        clock.tick(15)  
                        


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
        if len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'solid')) > 0:
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
        
    def initArea(self, mapFile):
        """Load maps and initialize sprite layers for each new area"""
        self.tilemap = tmx.load(mapFile, screen.get_size())
        print (type(self.tilemap.layers))
        self.players = tmx.SpriteLayer()
        self.objects = tmx.SpriteLayer()
        # Initializing other animated sprites
        try:
            for cell in self.tilemap.layers['sprites'].find('src'):
                SpriteLoop((cell.px,cell.py), cell, self.objects)
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


    def initStartmenu(self):
        print ("start menu")

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
        gameDisplay = pygame.display.set_mode((800,600))

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

            # self.initMenu()

            
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
            print ('hello world')

        def mainmenu_background():
            """Background color of the main menu, on this function user can plot
                images, play sounds, etc."""
            gameDisplay.fill((40, 0, 40))

        def hldfunction(filename):
            path = os.getcwd() + '/SaveFiles/' + filename 
            fileRead = open(path, 'r')
            hldString = ""

            for line in fileRead:
                hldString += line
            
            self.save = hldString.split(',')
            
            print ('oh over here')
            print (self.save)

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
        newgameMenu.add_option('New Game', play_function)
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

    