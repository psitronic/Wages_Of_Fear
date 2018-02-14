# 'Wages of Fear'
# By Andrey Sidorenko spintronic@tuta.io
# The game inspired by 'Jeux et casse-tête à programmer' (Jacques Arsac, 1985)
# Bitmap images http://pixabay.com/
# WAV sounds/music https://freesound.org/ (Attribution 3.0 Unported)
# Future TimeSplitters font is licensed under the 1001Fonts Free For Commercial Use License (FFC)
# Released under a "Simplified BSD" license

class GameStats():
    """
    Track statistics for Wages of Fear
    """
    
    def __init__(self):
        """
        Initialize statistics
        """
        
        self.reset_stats()
        self.diamonds_collected = 0
        self.inkblots_killed = 0
        self.deaths_killed = 0
        
    def reset_stats(self):
        """
        Reset statistcis that can be changed during the game
        """
        self.diamonds_collected = 0
        self.inkblots_killed = 0
        self.deaths_killed = 0
        
    def diamond_collected(self):
        """
        Count the number of collected diamonds
        """
        self.diamonds_collected += 1
        
    def inkblot_killed(self):
        """
        Count the number of killed inkblots
        """
        self.inkblots_collected += 1
        
    def death_killed(self):
        """
        Count the number of killed deaths
        """
        self.deaths_killed += 1