# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# WAV sounds/music https://freesound.org/ (Attribution 3.0 Unported)
# Future TimeSplitters font is licensed under the 1001Fonts Free For Commercial Use License (FFC)
# Released under a "Simplified BSD" license

import sys
import pygame
from bomb import Bomb
from explosion import Explosion
from diamond import Diamond
from wall import Wall
from death import Death
from inkblot import Inkblot
from random import randint

def check_keydown_events(event, wof_settings, screen, hero, bombs):
    """Respond to key presses"""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        hero.moving_right = True
    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
        hero.moving_left = True
    if event.key == pygame.K_UP or event.key == pygame.K_w:
        hero.moving_up = True
    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
        hero.moving_down = True
    elif event.key == pygame.K_SPACE:
        put_bomb(wof_settings,screen,hero,bombs)

def check_keyup_events(event, hero):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        hero.moving_right = False
    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
        hero.moving_left = False
    if event.key == pygame.K_UP or event.key == pygame.K_w:
        hero.moving_up = False
    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
        hero.moving_down = False


def check_events(wof_settings, screen, hero, bombs):
    """
    Watch for keyboard and mouse events.
    """
    for event in pygame.event.get():

        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            wof_settings.running = False    
            terminate()
#        elif (event.type == pygame.KEYUP and event.key == pygame.K_b):
#            wof_settings.running = False
#            return 'back'
#        elif (event.type == pygame.KEYUP and event.key == pygame.K_n):
#            wof_settings.running = False
#            return 'next'
#        elif (event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE):
#            wof_settings.running = False
#            return 'replay'
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, wof_settings, screen, hero, bombs)
            # control the Hero movements
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, hero)

def update_screen(wof_settings,screen,walls,hero,diamonds,bombs,explosions,inkblots,deaths):
    """
    Update images on the screen and flip to the new screen
    """
    screen.fill(wof_settings.bg_color)
    walls.draw(screen) 
    for bomb in bombs.sprites():
        bomb.draw_bomb()

    for explosion in explosions.sprites():
        explosion.draw_explosion()
            
    diamonds.draw(screen)
    
    for inkblot in inkblots.sprites():
        inkblot.draw_inkblot()
    
    hero.blitme()

    for death in deaths.sprites():
        death.draw_death()
    
    pygame.display.flip()

def put_bomb(wof_settings,screen,hero,bombs):
    # Create a new bomb and add it to the bombs group.
    if hero.alive and len(bombs) < wof_settings.bombs_allowed:
        new_bomb = Bomb(wof_settings, screen, hero)
        bombs.add(new_bomb)
        
def update_bombs(wof_settings,screen,bombs,explosions,sound_bomb):
    """
    Update animations of bombs and get rid of old bombs
    """
    bombs.update()
    # Get rid of bombs that have exploded
    for bomb in bombs.copy():
        if bomb.counter == wof_settings.bomb_timer:
            sound_bomb.play()
            bomb.counter = 0
            new_explosion = Explosion(wof_settings,screen,bomb)
            bombs.remove(bomb)
            explosions.add(new_explosion)
            
def update_explosions(explosions,diamonds,hero,deaths):
    """
    Update animations of exposions
    """
    explosions.update()
    
    # Get rid of explosions
    for explosion in explosions.copy():
        if explosion.done == True:
            explosion.counter = 0
            explosion.done = False # Check if there is an explosion "process" finished
            destroy(explosions,diamonds,hero,deaths) # If the explosion hits an object, then remove it
            explosions.remove(explosion)

def destroy(explosions,inkblots,hero,deaths):
    """
    Destroy objects if the explosion hits them
    """
    explosion_hits_inkblot = pygame.sprite.groupcollide(explosions,inkblots,False,True,pygame.sprite.collide_mask)
    explosion_hits_hero = pygame.sprite.spritecollideany(hero,explosions,pygame.sprite.collide_mask)
    explosion_hits_death = pygame.sprite.groupcollide(explosions,deaths,False,True,pygame.sprite.collide_mask)
    
    if explosion_hits_hero != None:
        hero.alive = False
            
def create_diamonds(wof_settings,screen,diamonds,levelMap):
    """
    Create a set of diamonds
    """
       
    diamond_width = wof_settings.element_width
    diamond_height = wof_settings.element_height
    
    # Place the diamonds to the field
    for diamond_position in levelMap['diamond']:
        diamond = Diamond(screen)
        diamond.x = diamond_position[1] * diamond_width
        diamond.y = diamond_position[0] * diamond_height
        diamond.rect.x = diamond.x
        diamond.rect.y = diamond.y
        diamonds.add(diamond)            

def update_diamonds(hero,diamonds,sound_diamond):
    # Check for hero has hit any bullets
    # If so, get rid of the diamond
    
    if hero.alive:
        if pygame.sprite.spritecollide(hero, diamonds, True, pygame.sprite.collide_mask):
            # Sound to play when the diamond picked up
            sound_diamond.play()
         
def create_walls(wof_settings,screen,walls,levelMap):
    """
    Create walls
    """
    
    block_width = wof_settings.element_width
    block_height = wof_settings.element_height       
    
    # Create the top and bottom walls
    for block_position in levelMap['wall']:
        block = Wall(screen)
        block.x = block_position[1] * block_width
        block.y = block_position[0] * block_height
        block.rect.x = block.x
        block.rect.y = block.y
        walls.add(block)
        


def read_levels(wof_settings):
    
    mf = open(wof_settings.levels_file, 'r')
    
    # Each level must end with a blank line
    content = mf.readlines() + ['\r\n']
    mf.close()
    
    #create a dictionary containing corrdinates of various elements
    level_map = {'wall':[],
                 'diamond':[],
                 'inkblot':[],
                 'death':[],
                 'hero':(),
                 'exit':()}
    
    levels = []
    levelNum = 0
    
    for lineNum in range(len(content)):
        # Process each line that was in the level file.
        total_num_lines = wof_settings.height/wof_settings.element_height
        line = content[lineNum].rstrip('\r\n')
        lineNumShifted = lineNum -  total_num_lines* levelNum

        for symbolNum in range(len(line)):
            if line[symbolNum] == "#":
                level_map['wall'].append((lineNumShifted,symbolNum))
            if line[symbolNum] == "d":
                level_map['diamond'].append((lineNumShifted,symbolNum))
            if line[symbolNum] == "i":
                level_map['inkblot'].append((lineNumShifted,symbolNum))
            if line[symbolNum] == "p":
                level_map['death'].append((lineNumShifted,symbolNum))
            if line[symbolNum] == "h":
                level_map['hero'] = (lineNumShifted,symbolNum)
            if line[symbolNum] == "e":
                level_map['exit'] = (lineNumShifted,symbolNum)
            
                
        if lineNumShifted == (total_num_lines - 1) and lineNum !=0:
            levelNum += 1
            levels.append(level_map)
            level_map = {'wall':[],
                         'diamond':[],
                         'inkblot':[],
                         'death':[],
                         'hero':(),
                         'exit':()}
            

    return levels

def create_inkblots(wof_settings,screen,inkblots,levelMap):
    """
    Create a set of spatters
    """
    
    inkblot_width = wof_settings.element_width
    inkblot_height = wof_settings.element_height        
    
    # Create inkblots
    for inkblot_position in levelMap['inkblot']:
        inkblot = Inkblot(screen)
        inkblot.x = inkblot_position[1] * inkblot_width
        inkblot.y = inkblot_position[0] * inkblot_height
        inkblot.rect.x = inkblot.x
        inkblot.rect.y = inkblot.y
        inkblots.add(inkblot)

def update_inkblots(inkblots,walls,diamonds,hero,levelMap,sound_blot):
    """
    Update animations of inkblots and change their positions
    """
    inkblots.update()
    
    for inkblot in inkblots.copy():
        if inkblot.changePosition:
            newPosX = randint(1, 20)
            newPosY = randint(1, 15)
            if (newPosY,newPosX) not in levelMap['wall']:
                inkblot.rect.x = newPosX * 32
                inkblot.rect.y = newPosY * 32
                inkblot.changePosition = False
    
    inkblot_hits_hero = pygame.sprite.spritecollide(hero,inkblots,True,pygame.sprite.collide_mask) 
    
    if inkblot_hits_hero:
        sound_blot.play()
        hero.alive = False

def create_deaths(wof_settings,screen,deaths,levelMap):
    """
    Create a set of deaths
    """
    
    death_width = wof_settings.element_width
    death_height = wof_settings.element_height        
    
    # Create deaths
    for death_position in levelMap['death']:
        death = Death(wof_settings,screen)
        death.x = death_position[1] * death_width
        death.y = death_position[0] * death_height
        death.rect.x = death.x
        death.rect.y = death.y
        deaths.add(death)

    
def update_deaths(hero,deaths,walls,inkblots,diamonds):
    deaths.update(walls,inkblots,diamonds)
    
    death_hits_hero = pygame.sprite.spritecollide(hero,deaths,True,pygame.sprite.collide_mask) 
    
    if death_hits_hero:
        hero.alive = False

def start_screen(screen,wof_settings):
    """
    Display the instructions screen
    """
    text = ['Collect bitcoins and kill monsters.',
            '',
            'Arrow or WASD keys to move, Space to throw a bomb.',
            'Backspace to reset level, Esc to quit.',
            'N for next level, B to go back a level.',
            '',
            'Press any key to start the game or Esc to quit.']
    
    title_image = 'images/bitcoin.bmp'
    
    text_font = 'fonts/Future TimeSplitters.otf'
    text_font_size = 26
    displayTextToScreen(wof_settings,screen,title_image,text,text_font,text_font_size)
            
def level_screen(screen,wof_settings, current_level):
    """
    Display the level screen
    """
    
    title_image = 'images/bitcoin.bmp'
    level_text = 'Level %i' % (current_level + 1)
    text = [level_text,
            '',
            'Press any key to play or Esc to quit.']
    
    text_font = 'fonts/Future TimeSplitters.otf'
    text_font_size = 26
    
    displayTextToScreen(wof_settings,screen,title_image,text,text_font,text_font_size)

def displayTextToScreen(wof_settings,screen,title_image,text,text_font,text_font_size):            
    """
    Display the level screen
    """
    
    # Position the title image
    title_rect = pygame.image.load(title_image).get_rect()
    top_coord = 50
    title_rect.top = top_coord
    title_rect.centerx = wof_settings.width/2
    top_coord += title_rect.height
    
    # Start with drawing a blank color to the entire window:
    screen.fill(wof_settings.titleScreenBgColor)
    
    # Title image
    screen.blit(pygame.image.load(title_image), title_rect)
    
    # Position and draw the text
    for i in range(len(text)):
        title_font = pygame.font.Font(text_font, text_font_size)
        text_surf = title_font.render(text[i], 1, wof_settings.titleTextColor)
        text_rect = text_surf.get_rect()
        top_coord += 10
        text_rect.top = top_coord
        text_rect.centerx = wof_settings.width/2
        top_coord += text_rect.height
        screen.blit(text_surf, text_rect)
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return # user has pressed a key, so return.
            
            # Display the contents to the actual screen.
            pygame.display.flip()         
            
def terminate():
    pygame.quit()
    sys.exit(0)