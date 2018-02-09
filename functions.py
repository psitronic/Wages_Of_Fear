# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# WAV sounds/music https://freesound.org/ (Attribution 3.0 Unported)
# Released under a "Simplified BSD" license

import sys
import pygame
from bomb import Bomb
from explosion import Explosion
from diamond import Diamond
from wall import Wall
from random import randint, randrange

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
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, wof_settings, screen, hero, bombs)
            # control the Hero movements
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, hero)

def update_screen(wof_settings,screen,walls,hero,diamonds,bombs,explosions):
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
    hero.blitme()
    pygame.display.flip()

def put_bomb(wof_settings,screen,hero,bombs):
    # Create a new bomb and add it to the bombs group.
    if len(bombs) < wof_settings.bombs_allowed:
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
            
def update_explosions(explosions,diamonds,hero):
    """
    Update animations of exposions
    """
    explosions.update()
    
    # Get rid of explosions
    for explosion in explosions.copy():
        if explosion.done == True:
            explosion.counter = 0
            explosion.done = False # Check if there is an explosion "process" finished
            destroy(explosions,diamonds,hero) # If the explosion hits an object, then remove it
            explosions.remove(explosion)

def destroy(explosions,diamonds,hero):
    """
    Destroy objects if the explosion hits them
    """
    explosion_hits_diamonds = pygame.sprite.groupcollide(explosions,diamonds,False,True,pygame.sprite.collide_mask)
    explosion_hits_hero = pygame.sprite.spritecollideany(hero,explosions,pygame.sprite.collide_mask) 
    
    if explosion_hits_hero != None:
        hero.alive = False
            
def put_diamond(wof_settings,screen,diamonds,walls):
    # Create a diamond and place it to the random position
    # Spacing between a diamond and the edges is equal to two diamond widths or heights

    diamond = Diamond(wof_settings, screen)
    diamond_width = diamond.rect.width
    diamond_height = diamond.rect.height

    diamond.x = randrange(2*diamond_width, wof_settings.width - 2*diamond_width)
    diamond.y = randrange(2*diamond_height, wof_settings.height - 2*diamond_height)
    diamond.rect.x = diamond.x
    diamond.rect.y = diamond.y
    
    # check if the position is occupied
    diamond_hit_diamond = pygame.sprite.spritecollideany(diamond, diamonds)
    diamond_hit_walls = pygame.sprite.spritecollideany(diamond, walls)

    if diamond_hit_diamond == None and diamond_hit_walls == None:
        diamonds.add(diamond)
        return True
    else:
        diamond.kill()
        return False

def create_diamonds(wof_settings,screen,diamonds,walls):
    """
    Create a random set of diamonds
    """
    maxDiamonds = randint(wof_settings.min_diamonds,wof_settings.max_diamonds)
    total = 0 
    
    while total < maxDiamonds:
        if put_diamond(wof_settings,screen,diamonds,walls):
            total += 1
            

def update_diamonds(hero,diamonds,sound_diamond):
    # Check for hero has hit any bullets
    # If so, get rid of the diamond
    
    if hero.alive:
        if pygame.sprite.spritecollide(hero, diamonds, True, pygame.sprite.collide_mask):
         # Sound to play when the diamond picked up
         sound_diamond.play()
         
def create_walls(wof_settings,screen,walls):
    """
    Create walls and randomly distributed barriers 
    """
    
    level_map = readLevelsFile(wof_settings.levels_file)
    
    block = Wall(wof_settings,screen)
    
    block_width = block.rect.width
    block_height = block.rect.height        
    
    # Create the top and bottom walls
    for block_position in level_map:
        block = Wall(wof_settings,screen)
        block.x = block_position[1] * block_width
        block.y = block_position[0] * block_height
        block.rect.x = block.x
        block.rect.y = block.y
        walls.add(block)
        


def readLevelsFile(filename):
    mf = open(filename, 'r')
    # Each level must end with a blank line
    content = mf.readlines() + ['\r\n']
    mf.close()
    level_map = []
    for lineNum in range(len(content)):
        # Process each line that was in the level file.
        line = content[lineNum].rstrip('\r\n')
        
        for symbolNum in range(len(line)):
            if line[symbolNum] == "#":
                level_map.append((lineNum,symbolNum))
                
    return level_map