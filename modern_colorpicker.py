#Enhanced Color Picker with HSV support and modern design
#Modern UI update for MCSkinStudio

import pygame
import math
import colorsys
from pygame.locals import *

class ModernColorPicker:
    def __init__(self, pos, mcskin2d):
        self.pos = pos
        self.mcskin2d = mcskin2d
        self.hsv = [0.0, 1.0, 1.0]  # Hue, Saturation, Value
        self.rgb = [255, 255, 255]
        
        # Create surfaces for different components
        self.hue_bar_width = 20
        self.hue_bar_height = 200
        self.sv_square_size = 180
        
        # Create HSV picker surface
        self.surface = pygame.Surface((self.sv_square_size + self.hue_bar_width + 10, max(self.sv_square_size, self.hue_bar_height)))
        self.surface.set_colorkey((0, 0, 0))
        
        # Create color wheel/square surfaces
        self.sv_surface = pygame.Surface((self.sv_square_size, self.sv_square_size))
        self.hue_surface = pygame.Surface((self.hue_bar_width, self.hue_bar_height))
        
        self.rect = pygame.Rect(pos, self.surface.get_size())
        
        # Initialize surfaces
        self._create_hue_bar()
        self._create_sv_square()
        
        # Cursor positions
        self.hue_cursor_y = 0
        self.sv_cursor_x = self.sv_square_size
        self.sv_cursor_y = 0
        
    def _create_hue_bar(self):
        """Create the vertical hue selection bar"""
        for y in range(self.hue_bar_height):
            hue = y / self.hue_bar_height
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
            pygame.draw.line(self.hue_surface, color, (0, y), (self.hue_bar_width, y))
    
    def _create_sv_square(self):
        """Create the saturation/value selection square"""
        for x in range(self.sv_square_size):
            for y in range(self.sv_square_size):
                saturation = x / self.sv_square_size
                value = 1.0 - (y / self.sv_square_size)
                rgb = colorsys.hsv_to_rgb(self.hsv[0], saturation, value)
                color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
                self.sv_surface.set_at((x, y), color)
    
    def _update_rgb_from_hsv(self):
        """Convert HSV to RGB and update"""
        rgb = colorsys.hsv_to_rgb(self.hsv[0], self.hsv[1], self.hsv[2])
        self.rgb = [int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)]
    
    def update(self):
        """Handle mouse input and update color selection"""
        mouse_pos = self.mcskin2d.mousehandler.getpos()
        mouse_pressed = self.mcskin2d.inputengine.mouseispushed(1)
        
        if mouse_pressed and self.rect.collidepoint(mouse_pos):
            relative_pos = (mouse_pos[0] - self.pos[0], mouse_pos[1] - self.pos[1])
            
            # Check if clicking on hue bar
            hue_bar_rect = pygame.Rect(self.sv_square_size + 5, 0, self.hue_bar_width, self.hue_bar_height)
            if hue_bar_rect.collidepoint(relative_pos):
                # Update hue
                self.hue_cursor_y = relative_pos[1]
                self.hsv[0] = self.hue_cursor_y / self.hue_bar_height
                self._create_sv_square()  # Update SV square with new hue
                self._update_rgb_from_hsv()
                return True
                
            # Check if clicking on SV square
            sv_rect = pygame.Rect(0, 0, self.sv_square_size, self.sv_square_size)
            if sv_rect.collidepoint(relative_pos):
                # Update saturation and value
                self.sv_cursor_x = relative_pos[0]
                self.sv_cursor_y = relative_pos[1]
                self.hsv[1] = self.sv_cursor_x / self.sv_square_size
                self.hsv[2] = 1.0 - (self.sv_cursor_y / self.sv_square_size)
                self._update_rgb_from_hsv()
                return True
        
        return False
    
    def render(self):
        """Render the color picker"""
        self.surface.fill((0, 0, 0))
        
        # Draw SV square
        self.surface.blit(self.sv_surface, (0, 0))
        
        # Draw hue bar
        self.surface.blit(self.hue_surface, (self.sv_square_size + 5, 0))
        
        # Draw borders
        pygame.draw.rect(self.surface, (100, 100, 100), (0, 0, self.sv_square_size, self.sv_square_size), 2)
        pygame.draw.rect(self.surface, (100, 100, 100), (self.sv_square_size + 5, 0, self.hue_bar_width, self.hue_bar_height), 2)
        
        # Draw cursors
        # SV cursor
        cursor_color = (255, 255, 255) if self.hsv[2] < 0.5 else (0, 0, 0)
        pygame.draw.circle(self.surface, cursor_color, (int(self.sv_cursor_x), int(self.sv_cursor_y)), 6, 2)
        
        # Hue cursor
        hue_cursor_x = self.sv_square_size + 5 + self.hue_bar_width // 2
        pygame.draw.circle(self.surface, (255, 255, 255), (hue_cursor_x, int(self.hue_cursor_y)), 8, 2)
        pygame.draw.circle(self.surface, (0, 0, 0), (hue_cursor_x, int(self.hue_cursor_y)), 8, 1)
        
        return self.surface
    
    def get_rgb(self):
        """Get current RGB color"""
        return self.rgb
    
    def set_rgb(self, rgb):
        """Set color from RGB values"""
        self.rgb = list(rgb)
        # Convert RGB to HSV
        hsv = colorsys.rgb_to_hsv(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)
        self.hsv = list(hsv)
        
        # Update cursor positions
        self.hue_cursor_y = self.hsv[0] * self.hue_bar_height
        self.sv_cursor_x = self.hsv[1] * self.sv_square_size
        self.sv_cursor_y = (1.0 - self.hsv[2]) * self.sv_square_size
        
        # Update SV square
        self._create_sv_square()
    
    def getsurface(self):
        return self.render()
    
    def getpos(self):
        return self.pos
    
    def getrect(self):
        return self.rect