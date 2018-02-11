# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# WAV sounds/music https://freesound.org/ (Attribution 3.0 Unported)
# Released under a "Simplified BSD" license

import pygame
from pygame.sprite import Group
from wof_settings import GameSettings
from hero import Hero
import functions as fns

def run_game():
    # Initialize game and create a screen object
    pygame.init()
    wof_settings = GameSettings()
    screen = pygame.display.set_mode((wof_settings.width, wof_settings.height))
    pygame.display.set_caption("The Wages of Fear")
    
    # load sounds for events
    sound_diamond = pygame.mixer.Sound('sounds/coin.wav')
    sound_bomb = pygame.mixer.Sound('sounds/explosion.wav')
    sound_blot = pygame.mixer.Sound('sounds/splash.wav')
    
    # play background music - infinit loop
    pygame.mixer.music.load('sounds/background-music.mp3')
    pygame.mixer.music.play(-1)

    # create groups and objects
    walls = Group()  # Make a group to store walls
    hero = Hero(wof_settings,screen) # create the hero
    bombs = Group() # Make a group to store bombs in
    diamonds = Group() # Make a group to store all diamonds in
    explosions = Group()
    inkblots = Group()
    deaths = Group()
    
    # Create walls and barriers
    levelMap = fns.create_walls(wof_settings,screen,walls)
    # Create the diamonds
    fns.create_diamonds(wof_settings,screen,diamonds,walls)
    
    fns.create_inkblots(screen,inkblots,walls,diamonds,hero)

    fns.create_deaths(wof_settings,screen,deaths,walls,inkblots,levelMap)

    while wof_settings.running:
        # here is the game logic
        # check if keys pressed or released
        fns.check_events(wof_settings,screen,hero,bombs)        
        hero.update(walls)
        fns.update_inkblots(inkblots,walls,diamonds,hero,levelMap,sound_blot)
        fns.update_deaths(hero,deaths,walls,inkblots)
        fns.update_diamonds(hero,diamonds,sound_diamond)
        fns.update_bombs(wof_settings,screen,bombs,explosions,sound_bomb)
        fns.update_explosions(explosions,inkblots,hero,deaths)
        fns.update_screen(wof_settings, screen, walls,hero, diamonds,bombs,explosions,inkblots,deaths)

if __name__ == '__main__':
    run_game()