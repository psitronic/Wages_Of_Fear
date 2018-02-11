# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# WAV sounds/music https://freesound.org/ (Attribution 3.0 Unported)
# Released under a "Simplified BSD" license

import pygame
from pygame.sprite import Sprite
from random import randint

class Death(Sprite):
    """
    
    """
    def __init__(self,wof_settings,screen):
        """
        The Death's settings initialization
        """
        super().__init__()
        self.screen = screen
        self.wof_settings = wof_settings
        
        self.image = pygame.image.load('images/pacman.bmp')

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.screen_rect = screen.get_rect()
        
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.hitWall = False
 
        self.deltaX = 1
        self.deltaY = 1

        
    def update(self, walls,inkblots):
        """
        Update the death position
        """
        old_x = self.rect.centerx
        old_y = self.rect.centery
        
        self.rect.centerx += self.deltaX * self.wof_settings.death_speed_factor
        self.rect.centery += self.deltaY * self.wof_settings.death_speed_factor
        
        if not pygame.sprite.spritecollide(self, walls, False,pygame.sprite.collide_mask) and not pygame.sprite.spritecollide(self, inkblots, False):
            old_x = self.rect.centerx
            old_y = self.rect.centery
        else:
            self.rect.centerx = old_x
            self.rect.centery = old_y
            choise = randint(0,3)
            if choise == 0:
                self.deltaX = 1
            if choise == 1:
                self.deltaX =-1
            if choise == 2:
                self.deltaY = 1
            if choise == 3:
                self.deltaY =-1
                
    def draw_death(self):
        """
        """
        self.screen.blit(self.image,self.rect)