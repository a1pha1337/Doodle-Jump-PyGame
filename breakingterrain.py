import pygame
import terrain

class BreakingTerrain(terrain.Terrain):
    def onCollisionEnter(self, obj):
        if (super().onCollisionEnter(obj)):
            self.kill()
            return True
        else:
            return False