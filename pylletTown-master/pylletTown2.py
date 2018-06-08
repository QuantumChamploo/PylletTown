import pygame
from pygame.locals import *
import tmx
import pygameMenu
from pygameMenu.locals import *


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
                        gameDisplay.fill(red)    
                        gameDisplay.blit(thisImage, (100, 0))
                        largeText = pygame.font.Font('freesansbold.ttf',35)
                        TextSurf, TextRect = text_objects("Click 's' to leave 'menu'", largeText)
                        TextRect.center = ((300),(200))
                        gameDisplay.blit(TextSurf, TextRect)
                
               
                        pygame.display.update()
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


    def introMenu(self):

        gameDisplay = pygame.display.set_mode((800,600))

        clock = pygame.time.Clock()

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

        def mainmenu_background():
            """Background color of the main menu, on this function user can plot
                images, play sounds, etc."""
            gameDisplay.fill((40, 0, 40))

        def hldfunction():
            print('hereASDFASDF')
            print('adsfasdfasdf')


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
                                    onclose=PYGAME_MENU_DISABLE_CLOSE,
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
                                    onclose=PYGAME_MENU_DISABLE_CLOSE,
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
                                    onclose=PYGAME_MENU_DISABLE_CLOSE,
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
        loadgameMenu.add_option('Close', PYGAME_MENU_CLOSE)
        loadgameMenu.add_option('Print stuff',hldfunction)
        mainMenu.add_option('Exit', PYGAME_MENU_EXIT)
        

        while True:
            clock.tick(60)

            gameDisplay.fill(COLOR_BACKGROUND)
            mainMenu.enable()

            events = pygame.event.get()

            mainMenu.mainloop(events)
            print ("looping")

            pygame.display.flip()






    def initSign(self, signFile):
        """Loads sign up"""
        clock = pygame.time.Clock()
        gameDisplay = pygame.display.set_mode((800,600))  
        thisImage = pygame.image.load('uujihyugtguyh.png')
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
            gameDisplay.fill(red)    
            gameDisplay.blit(thisImage, (100, 0))
            largeText = pygame.font.Font('freesansbold.ttf',35)
            TextSurf, TextRect = text_objects("Click 's' to leave 'menu'", largeText)
            TextRect.center = ((300),(200))
            gameDisplay.blit(TextSurf, TextRect)
    
   
            pygame.display.update()
            clock.tick(15)  
            print ("HERE")



    

    def main(self):
        clock = pygame.time.Clock()
        self.initArea('test3.tmx')
        print (self.save)

        keepPlaying = True

        intro = False

        gameDisplay = pygame.display.set_mode((800,600))
        
        while intro:
            
            
        
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    keepPlaying = False
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    keepPlaying = False
                    pygame.quit()
                    
                    return 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP and event.key == pygame.K_a:
                    intro = False    
            gameDisplay.fill(red)
            
            largeText = pygame.font.Font('freesansbold.ttf',35)
            TextSurf, TextRect = text_objects("Click 'a' to leave 'menu'", largeText)
            TextRect.center = ((300),(200))
            gameDisplay.blit(TextSurf, TextRect)

            pygame.display.update()
            clock.tick(15)
            # print("i am in the introOOOOO")
                      
            # intro = False

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
        
        
        

        startMenu = False
        self.introMenu()
        while startMenu:
            clock.tick(60)
            gameDisplay.fill(COLOR_BACKGROUND)


            events = pygame.event.get()
            menu.enable()
            for event in pygame.event.get():
                print(event)
                if event.type == QUIT:
                    
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    
                    pygame.quit()
                    
                    return 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP and event.key == pygame.K_a:
                    startMenu = False


            menu.mainloop(events)

             # Flip surface
            pygame.display.flip()





        while keepPlaying:
            
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


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Pyllet Town")
    print ("hello")
    
    Game(screen).main()

    