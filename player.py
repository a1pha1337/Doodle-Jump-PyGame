import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites):
        pygame.sprite.Sprite.__init__(self)

        self.LEFT_DIR = 0
        self.RIGHT_DIR = 1

        self.__x = x
        self.__y = y

        self.current_dy = 0

        self.images = []
        self.image = None

        self.isJumping = False

        for sprite in sprites:
            self.images.append(pygame.image.load(sprite).convert_alpha())

        self.setDirection('left')
        self.__setRect()

    def setDirection(self, direction: str):
        if direction == 'left':
            self.currentDirection = 'left'
            self.image = self.images[self.LEFT_DIR]
        elif direction == 'right':
            self.currentDirection = 'right'
            self.image = self.images[self.RIGHT_DIR]

    def moving(self, direction: str):
        if direction == 'left':
            self.__x -= 2 * self.__speed
            self.setDirection('left')
        elif direction == 'right':
            self.__x += 2 * self.__speed
            self.setDirection('right')
        self.__setRect()

    def fall(self):
        self.isJumping = False
        self.__y += 2 * self.__fallSpeed
        self.__setRect()

    def jump(self, terrains):
        if (self.jumpEffect != 0):
            if (self.__y < 250):
                self.isJumping = True
                self.jumpEffect -= 1

                dy = self.jumpEffect ** 2 / self.__jumpHeight
                terrains.update(dy)
                self.current_dy = int(dy)
            else:
                self.isJumping = True
                self.jumpEffect -= 1
                self.__y -= self.jumpEffect ** 2 / self.__jumpHeight
        else:
            self.isJumping = False
            self.jumpEffect = self.__JUMP_EFFECT

        self.__setRect()

    def __setRect(self):
        self.rect = self.image.get_rect(center=(self.__x, self.__y)).inflate(-20, 0)

    @property
    def Speed(self):
        return self.__speed

    @Speed.setter
    def Speed(self, value):
        self.__speed = value

    @property
    def FallSpeed(self):
        return self.__fallSpeed

    @FallSpeed.setter
    def FallSpeed(self, value):
        self.__fallSpeed = value

    @property
    def JumpHeight(self):
        return self.__jumpHeight

    @JumpHeight.setter
    def JumpHeight(self, value):
        self.__jumpHeight = value

    @property
    def JumpEffect(self):
        return self.__JUMP_EFFECT

    @JumpEffect.setter
    def JumpEffect(self, value):
        self.jumpEffect = value
        self.__JUMP_EFFECT = value

    @property
    def X(self):
        return self.__x

    @X.setter
    def X(self, value):
        self.__x = value

    @property
    def Y(self):
        return self.__y

    @Y.setter
    def Y(self, value):
        self.__y = value

    @property
    def Rect(self):
        return self.rect
