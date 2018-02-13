# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# WAV sounds/music https://freesound.org/ (Attribution 3.0 Unported)
# Future TimeSplitters font is licensed under the 1001Fonts Free For Commercial Use License (FFC)
# Released under a "Simplified BSD" license

import pygame
from pygame.sprite import Group
from wof_settings import GameSettings
from hero import Hero
import functions as fns
    
def run_level(levels,current_level,wof_settings,screen):    
    # select the current level map
    levelMap = levels[current_level]
    
    # load sounds for events
    sound_diamond = pygame.mixer.Sound(wof_settings.sound_diamond)
    sound_bomb = pygame.mixer.Sound(wof_settings.sound_bomb)
    sound_blot = pygame.mixer.Sound(wof_settings.sound_blot)

    # start and play background music - infinit loop
    pygame.mixer.music.load(wof_settings.bckg_music)
    pygame.mixer.music.play(-1)

    # create groups and objects
    walls = Group()  # Make a group to store walls
    hero = Hero(wof_settings,screen) # create the hero
    bombs = Group() # Make a group to store bombs in
    diamonds = Group() # Make a group to store all diamonds in
    explosions = Group() # Make a group to store all explosions in
    inkblots = Group() # Make a group to store all inkblots in
    deaths = Group() # # Make a group to store all deaths in
    
    # Create Walls according to the level map
    fns.create_walls(wof_settings,screen,walls,levelMap)
    # Create Diamonds according to the level map
    fns.create_diamonds(wof_settings,screen,diamonds,levelMap)
    # Create Inkblots according to the level map
    fns.create_inkblots(wof_settings,screen,inkblots,levelMap)
    # Create Deaths according to the level map
    fns.create_deaths(wof_settings,screen,deaths,levelMap)

    while wof_settings.running:
        # here is the game logic
        fns.check_events(wof_settings,screen,hero,bombs) # check if keys pressed or released        
        hero.update(walls) # update Hero position and state
        fns.update_inkblots(inkblots,walls,diamonds,hero,levelMap,sound_blot)
        fns.update_deaths(hero,deaths,walls,inkblots,diamonds)
        fns.update_diamonds(hero,diamonds,sound_diamond)
        fns.update_bombs(wof_settings,screen,bombs,explosions,sound_bomb)
        fns.update_explosions(explosions,inkblots,hero,deaths)
        
        fns.update_screen(wof_settings, screen, walls,hero, diamonds,bombs,explosions,inkblots,deaths)

    return status

def run_game():
    # Initialize game and create a screen object
    pygame.init()
    wof_settings = GameSettings() # set the game settings
    screen = pygame.display.set_mode((wof_settings.width, wof_settings.height))
    pygame.display.set_caption(wof_settings.caption)
    
    fns.start_screen(screen,wof_settings) # show the title screen
    
    # read the level map from the text file
    # input: text file name
    # return: a dictionary with coordinates of the game elements
    levels = fns.read_levels(wof_settings)
    current_level = 0
    
    while True:
        #fns.level_screen(screen,wof_settings)        
        status = run_level(levels,current_level,wof_settings,screen)
        
        if status in ('done','next'):
            current_level += 1
            if current_level >= len(levels):
                cureent_level = 0
        elif status == 'back':
            current_level -= 1
            if current_level < 0:
                current_level = len(levels) - 1
        elif status == 'replay':
            pass

if __name__ == '__main__':
    run_game()