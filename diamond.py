# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# WAV sounds/music https://freesound.org/ (Attribution 3.0 Unported)
# Released under a "Simplified BSD" license

import pygame
from pygame.sprite import Sprite


class Diamond(Sprite):
    """A class to represent a diamond"""
    
    def __init__(self,screen):
        """
        Initialize the diamond and set its random position
        """
        
        super().__init__()
        self.screen = screen
        
        self.image = pygame.image.load('images/bitcoin.bmp')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect.centerx = self.rect.width
        self.rect.centery = self.rect.height
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def blit_diamond(self):
        """Draw the diamond to the screen."""
        self.screen.blit(self.image,self.rect)
