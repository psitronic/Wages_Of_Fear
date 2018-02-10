# Bitmap images http://pixabay.com/
# WAV sounds/music https://freesound.org/ (Attribution 3.0 Unported)
# Released under a "Simplified BSD" license

import pygame
from pygame.sprite import Sprite
from random import randint

class Inkblot(Sprite):
    """A class to represent a diamond"""
    
    def __init__(self,screen):
        """
        Initialize the inkblot and set its random position
        """
        
        super().__init__()
        self.screen = screen
        
        self.image = pygame.image.load('images/paint-splatter.bmp')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect.centerx = self.rect.width
        self.rect.centery = self.rect.height
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        self.changePosition = False
        self.counter = 0
        
    def update(self):
        """
        Create an inkblot animation
        """
        self.counter += 1
        if self.counter == 400:
            self.changePosition = True
            self.counter = 0
            
    def draw_inkblot(self):
        """Draw the inkblot to the screen."""
        self.screen.blit(self.image,self.rect)

