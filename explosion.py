# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# WAV sounds/music https://freesound.org/ (Attribution 3.0 Unported)
# Released under a "Simplified BSD" license

import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """A class to manage bombs explosion"""
    
    def __init__(self,wof_settings,screen,bomb):
        """
        Create a explosion object at the exploded bomb position
        """
        
        super().__init__()
        self.screen = screen
                
        self.explosion_image = pygame.image.load('images/explosion.bmp')
        
        self.rect = self.explosion_image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.rect.centerx = bomb.rect.centerx
        self.rect.centery = bomb.rect.centery
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        self.counter = 0
        self.done = False

    def update(self):
        """
        Create a explosion animation
        """
        self.counter += 1
        if self.counter == 30:
            self.done = True
            
    def draw_explosion(self):
        """Draw the explosion to the screen."""
        self.screen.blit(self.explosion_image,self.rect)

