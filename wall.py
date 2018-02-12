# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# WAV sounds/music https://freesound.org/ (Attribution 3.0 Unported)
# Released under a "Simplified BSD" license

import pygame
from pygame.sprite import Sprite

class Wall(Sprite):
    """A class to create blocks and walls in the game"""
    
    def __init__(self,screen):
        """
        Create a block/wall object at the specified position
        """
        
        super().__init__()
        self.screen = screen
                
        self.image = pygame.image.load('images/vinyl.png')
        
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.screen_rect = screen.get_rect()
        
        self.rect.centerx = self.rect.width
        self.rect.centery = self.rect.height
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def draw_wall(self):
        """Draw the wall/blocks to the screen."""
        self.screen.blit(self.image,self.rect)
