# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# WAV sounds/music https://freesound.org/ (Attribution 3.0 Unported)
# Released under a "Simplified BSD" license

import pygame
from pygame.sprite import Sprite

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

        
    def update(self, walls):
        """
        Update the death position
        """
        if self.moving_right:
            self.rect.left += 2 * self.wof_settings.death_speed_factor
        if self.moving_left:
            self.rect.left -= self.wof_settings.death_speed_factor

        # check if we hit the wall/block
        death_hit_wall = pygame.sprite.spritecollide(self, walls, False,pygame.sprite.collide_mask)        
        for wall in death_hit_wall:
            if self.moving_right:
                self.rect.right = wall.rect.left
                self.moving_left = True
            if self.moving_left:
                self.rect.left = wall.rect.right
                self.moving_right = True


        if self.moving_up:
            self.rect.top += 2 * self.wof_settings.death_speed_factor
        if self.moving_down:
            self.rect.top -= self.wof_settings.death_speed_factor

        # check if we hit the wall/block
        death_hit_wall = pygame.sprite.spritecollide(self, walls, False,pygame.sprite.collide_mask)        
        for wall in death_hit_wall:
            if self.moving_down:
                self.rect.bottom = wall.rect.top
                self.moving_up = True
            if self.moving_up:
                self.rect.top = wall.rect.bottom
                self.moving_down = True

                
    def draw_death(self):
        """
        """
        self.screen.blit(self.image,self.rect)