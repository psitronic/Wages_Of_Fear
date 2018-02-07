# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# Released under a "Simplified BSD" license

import pygame
from pygame.sprite import Sprite

class Bomb(Sprite):
    """A class to manage bombs thrown by the hero"""
    
    def __init__(self,wof_settings,screen,hero):
        """
        Create a bomb object at the hero's current position
        """
        
        super().__init__()
        self.screen = screen
        
        self.bomb_timer = wof_settings.bomb_timer
        
        self.bomb_images = []
        
        for n in range(5):
            self.bomb_images.append(pygame.image.load('images/bomb_'+str(n+1)+'.bmp'))
        
        self.index = 0
        self.bomb_image = self.bomb_images[self.index]
        self.rect = self.bomb_image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.rect.centerx = hero.rect.centerx
        self.rect.centery = hero.rect.centery
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        self.counter = 0

    def update(self):
        """
        Create a bomb animation
        """
        self.counter += 1
        self.index += 1
        if self.index >= len(self.bomb_images):
            self.index = 0
        self.bomb_image = self.bomb_images[self.index]
            
    def draw_bomb(self):
        """Draw the bomb to the screen."""
        self.screen.blit(self.bomb_image,self.rect)

        