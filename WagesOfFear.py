# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# Released under a "Simplified BSD" license

import pygame
from pygame.sprite import Group
from wof_settings import GameSettings
from hero import Hero
import functions as fns

def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    wof_settings = GameSettings()
    screen = pygame.display.set_mode((wof_settings.width, wof_settings.height))
    pygame.display.set_caption("The Wages of Fear")
    sound_diamond = pygame.mixer.Sound('sounds/crystal.wav')
    sound_bomb = pygame.mixer.Sound('sounds/explosion.wav')

    
    hero = Hero(wof_settings,screen) # create the hero
    bombs = Group() # Make a group to store bombs in
    diamonds = Group() # Make a group to store all diamonds in
    
    # Create the diamonds
    fns.create_diamonds(wof_settings,screen,diamonds)

    while wof_settings.running:
        # check if keys pressed or released
        fns.check_events(wof_settings,screen,hero,bombs)
        
        hero.update()
        fns.update_diamonds(hero,diamonds,sound_diamond)
        fns.update_bombs(wof_settings,bombs,sound_bomb)
        fns.update_screen(wof_settings, screen, hero, diamonds,bombs)

if __name__ == '__main__':
    run_game()