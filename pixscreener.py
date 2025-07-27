import sys
import pygame

class pixscreener:
    def __init__(self):
        # Cross-platform implementation using pygame
        pass
        
    def getpixel(self, pos):
        # For cross-platform compatibility, we'll use pygame to get pixel color
        try:
            # Get the current display surface
            screen = pygame.display.get_surface()
            if screen and pos[0] >= 0 and pos[1] >= 0 and pos[0] < screen.get_width() and pos[1] < screen.get_height():
                color = screen.get_at(pos)
                return (color[0], color[1], color[2])
            else:
                return (0, 0, 0)  # Return black if position is invalid
        except:
            return (0, 0, 0)  # Return black as fallback


if __name__ == "__main__":
    thepixscreener = pixscreener()
    while 1: print(thepixscreener.getpixel((100, 100)))
