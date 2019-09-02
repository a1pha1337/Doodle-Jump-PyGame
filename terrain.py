import pygame

class Terrain(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite, sound):
        self.x = x
        self.y = y

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(sprite)
        self.sound = pygame.mixer.Sound(sound)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, *args):
        dy = args[0]
        self.y += dy
        self.__setRect(self.x, self.y)

    def playSound(self):
        self.sound.play()

    def onCollisionEnter(self, obj):
        if pygame.sprite.collide_rect(self, obj):
            if obj.Y + obj.Rect.height < self.rect.y + 40:
                return True
            else:
                return False
        else:
            return False

    def __setRect(self, x, y):
        self.rect = self.image.get_rect(center=(x, y))