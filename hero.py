# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# WAV sounds/music https://freesound.org/ (Attribution 3.0 Unported)
# Future TimeSplitters font is licensed under the 1001Fonts Free For Commercial Use License (FFC)
# Released under a "Simplified BSD" license

import pygame
from pygame.sprite import Sprite
from random import randint

class Hero(Sprite):
    """
    
    """
    def __init__(self,wof_settings,screen,position):
        """
        The Hero's settings initialization
        """
        super().__init__()
        self.screen = screen
        self.wof_settings = wof_settings
        
        self.image = pygame.image.load('images/penguin.bmp')

        self.rect = self.image.get_rect()
        
        self.screen_rect = screen.get_rect()
        
        self.rect.x = position[1] * wof_settings.element_width
        self.rect.y = position[0] * wof_settings.element_height
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        
        self.alive = True
        self.flyawayx = randint(-1,1)
        self.flyawayy = randint(-1,1)
        
    def update(self, walls):
        """
        Update the hero position
        """
        
        if self.alive:
            if self.moving_right:
                self.rect.x += self.wof_settings.hero_speed_factor
            if self.moving_left:
                self.rect.x -= self.wof_settings.hero_speed_factor
            
            # check if we hit the wall/block
            hero_hit_wall = pygame.sprite.spritecollide(self, walls, False,pygame.sprite.collide_mask)        
            for wall in hero_hit_wall:
                if self.moving_right:
                    self.rect.right = wall.rect.left
                if self.moving_left:
                    self.rect.left = wall.rect.right


            if self.moving_up:
                self.rect.y -= self.wof_settings.hero_speed_factor
            if self.moving_down:
                self.rect.y += self.wof_settings.hero_speed_factor
            
            # check if we hit the wall/block
            hero_hit_wall = pygame.sprite.spritecollide(self, walls, False,pygame.sprite.collide_mask)        
            for wall in hero_hit_wall:
                if self.moving_up:
                    self.rect.top = wall.rect.bottom
                if self.moving_down:
                    self.rect.bottom = wall.rect.top

        else:
            # if killed then fly away
            self.rect.x += self.flyawayx*3
            self.rect.y += self.flyawayy*3
            self.image = pygame.transform.rotate(self.image,90)
                
    def blitme(self):
        """
        """
        self.screen.blit(self.image,self.rect)