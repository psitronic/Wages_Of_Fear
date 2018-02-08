# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# WAV sounds/music https://freesound.org/ (Attribution 3.0 Unported)
# Released under a "Simplified BSD" license

import pygame

class Hero(object):
    """
    
    """
    def __init__(self,wof_settings,screen):
        """
        The Hero's settings initialization
        """
        self.screen = screen
        self.wof_settings = wof_settings
        
        self.image = pygame.image.load('images/penguin.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        
        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
    def update(self):
        """
        Update the hero position
        """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.wof_settings.hero_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.wof_settings.hero_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.wof_settings.hero_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.wof_settings.hero_speed_factor
            
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

            
    def blitme(self):
        """
        """
        self.screen.blit(self.image,self.rect)