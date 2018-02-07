# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# Released under a "Simplified BSD" license

class GameSettings(object):
    """
    Settings for the game 'Wages of Fear'
    """
    def __init__(self):
        """
        The game's settings initialization
        """
        
        # Screen settings
        self.width = 640
        self.height = 480
        self.bg_color = (230,230,230)
        
        # Hero settings
        self.hero_speed_factor = 0.75
        
        # Diamonds settings
        self.min_diamonds = 5
        self.max_diamonds = 10
        
        # Bomb settings
        self.bomb_timer = 1000 # wait before the bomb explodes
        self.bombs_allowed = 3 # number of available bombs at a time
        
        self.running = True