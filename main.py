import pygame
import json
import os.path

from random import randint
from player import *
from terrain import *
from breakingterrain import *

class Game():
    def __init__(self, caption):
        pygame.init()
        
        pygame.display.set_caption(caption)

        self.width = None
        self.height = None
        self.maxFPS = None
        self.score = None
        self.scoreSpeed = None
        self.level = 1
        self.clock = pygame.time.Clock()
        self.isPlaying = False

        settings = None
        if (os.path.exists('settings.json')):
            with open('settings.json', 'r') as f:
                settings = json.load(f)

            for key, value in settings.items():
                if key == 'window_width':
                    self.width = value
                elif key == 'window_height':
                    self.height = value
                elif key == 'max_fps':
                    self.maxFPS = value
                elif key == 'start_score':
                    self.score = value
                elif key == 'score_speed':
                    self.scoreSpeed = value
        else:

            settings = {
                'window_width': 350,
                'window_height': 500,
                'max_fps': 30,
                'start_score': 0,
                'score_speed': 1
            }

            self.width = 350
            self.height = 500
            self.maxFPS = 30
            self.score = 0
            self.scoreSpeed = 1

            with open('settings.json', 'w') as f:
                json.dump(settings, f, skipkeys=False, indent=4)

        self.mainWindow = pygame.display.set_mode((self.width, self.height))
        self.bgImage = pygame.image.load('background.png').convert_alpha()

    def menu(self):
        playButtons = [pygame.image.load('buttons/play.png'), pygame.image.load('buttons/play-on.png')]

        while True:
            playButton = playButtons[0]

            rect = playButton.get_rect(center=(self.width // 2, self.height // 2))

            mousePosition = pygame.mouse.get_pos()

            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()

                if i.type == pygame.MOUSEBUTTONDOWN:
                    if i.button == 1 and rect.collidepoint(mousePosition):
                        return True

            if rect.collidepoint(mousePosition):
                playButton = playButtons[1]

            self.mainWindow.blit(self.bgImage, (0,0))
            self.mainWindow.blit(playButton, (rect.x, rect.y))

            pygame.display.update()

            self.clock.tick(self.maxFPS)

    def start(self):
        #Initialize player
        self.player = Player(self.width // 2, self.height // 2, ['sprites/lik-left.png', 'sprites/lik-right.png'])
        self.player.Speed = 6.0
        self.player.FallSpeed = 5.0
        self.player.JumpHeight = 12.0
        self.player.JumpEffect = 20.0

        #Initializing first terrains
        self.terrains = pygame.sprite.Group()
        for i in range(50, 500, 50):
            self.terrains.add(Terrain(randint(1, self.width), i, 'sprites/defaultTerrain.png', 'sounds/jump.wav'))

        #Initializing text font
        self.textFont = pygame.font.SysFont('arial', 20, bold=True)

        #Initializing sounds
        self.soundLose = pygame.mixer.Sound('sounds/pada.wav')

        self.isPlaying = True


    def update(self):
        while (self.player.Y < self.height):
            self.__eventChecking()
            self.__collideChecking()
            self.__autoJumping()
            self.__sideChecking()
            self.__destroyUselessTerrains()
            self.__createNewTerrains()
            self.__changingLevel()
            self.__drawing()
            
            self.clock.tick(self.maxFPS)

    def __eventChecking(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        keys = pygame.key.get_pressed()

        #Keyboard pressing checking
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.moving('left')
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.moving('right')

    def __collideChecking(self):
    #Collide check
        if (not self.player.isJumping):
            for terrain in self.terrains:
                if (terrain.onCollisionEnter(self.player)):
                    self.player.jump(self.terrains)
                    terrain.playSound()

    def __autoJumping(self):
    #Auto-jump
        if self.player.isJumping:
            self.player.jump(self.terrains)
            self.score += self.player.current_dy * self.scoreSpeed
        else:
            self.player.fall()

    def __sideChecking(self):
    #Check side
        if self.player.X < 1:
            self.player.X = self.width
        if self.player.X > self.width:
            self.player.X = 1

        if self.player.Y > self.height and self.isPlaying:
            self.soundLose.play()
            self.isPlaying = False

    def __destroyUselessTerrains(self):
    #Kills useless terrains
        for terrain in self.terrains:
            if terrain.rect.y > self.height:
                terrain.kill()

    def __createNewTerrains(self):
    #Create new terrains
        checked = False
        for terrain in self.terrains:
            if terrain.rect.y < 0 and terrain.rect.y > -200:
                checked = True
        if not checked:
            randPlatform = None
            randY = None
            chance = None
            if (self.level == 1):
                randPlatform = randint(1, 10)
                randY = randint(-70, -40)
                chance = (randPlatform == 1)
            elif (self.level == 2):
                randPlatform = randint(1, 10)
                randY = randint(-100, -60)
                chance = randPlatform >= 1 and randPlatform <= 2
            elif (self.level == 3):
                randPlatform = randint(1, 10)
                randY = randint(-120, -80)
                chance = randPlatform >= 1 and randPlatform <= 3
            elif (self.level == 4):
                randPlatform = randint(1, 10)
                randY = randint(-140, -100)
                chance = randPlatform >= 1 and randPlatform <= 5
            elif (self.level == 5):
                randPlatform = randint(1, 10)
                randY = randint(-160, -120)
                chance = randPlatform >= 1 and randPlatform <= 7
            if chance:
                    self.terrains.add(BreakingTerrain(randint(15, self.width), randY, 'sprites/breakingTerrain.png', 'sounds/bijeli.wav'))
            else:
                    self.terrains.add(Terrain(randint(15, self.width), randY, 'sprites/defaultTerrain.png', 'sounds/jump.wav'))

    def __changingLevel(self):
    #Change level
        if (self.score > 40000):
            self.level = 5
        elif (self.score > 20000):
            self.level = 4
        elif (self.score > 10000):
            self.level = 3
        elif (self.score > 5000):
            self.level = 2

    def __drawing(self):
        #Drawing background
        self.mainWindow.blit(self.bgImage, (0,0))

        #Drawing terrains
        self.terrains.draw(self.mainWindow)

        #Drawing player
        self.mainWindow.blit(self.player.image, self.player.rect)

        #Setting player score
        textScore = self.textFont.render(str(self.score), 0, (0, 180, 0))
        self.mainWindow.blit(textScore, (0, 0))

        #Updating display
        pygame.display.update()

    def end(self):
        self.isPlaying = False
        self.score = 0

def main():
    #Bind game-window caption
    caption = "Doodle Jump"

    game = Game(caption)

    try:
        while True:
            if (game.menu()):
                game.start()
                game.update()
                game.end()
    except Exception as e:
        print(e.args)

if __name__ == '__main__':
    main()