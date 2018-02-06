# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# Released under a "Simplified BSD" license

import pygame
from wof_settings import GameSettings
from hero import Hero
import functions as fns

def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    wof_settings = GameSettings()
    screen = pygame.display.set_mode((wof_settings.width, wof_settings.height))
    pygame.display.set_caption("The Wages of Fear")
    
    hero = Hero(wof_settings,screen) # create the hero

    while True:
        fns.check_events(hero)
        hero.update()
        fns.update_screen(wof_settings, screen, hero)

run_game()