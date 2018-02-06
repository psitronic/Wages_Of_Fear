# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# Released under a "Simplified BSD" license

class GameSettings():
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
        self.hero_speed_factor = 0.5