#Modern GUI elements with improved styling and hover effects
#Enhanced UI components for MCSkinStudio

import pygame
from pygame.locals import *

class ModernButton:
    def __init__(self, text, code, pos, mcskin2d, width=None, height=32):
        self.text = text
        self.code = code
        self.pos = pos
        self.mcskin2d = mcskin2d
        self.height = height
        self.width = width or (mcskin2d.fontrenderer.sizesmall(text)[0] + 20)
        
        self.rect = pygame.Rect(pos, (self.width, self.height))
        self.hovered = False
        self.pressed = False
        
        # Modern color scheme
        self.bg_color = (70, 70, 70)
        self.bg_hover = (90, 90, 90)
        self.bg_pressed = (50, 50, 50)
        self.border_color = (120, 120, 120)
        self.text_color = (240, 240, 240)
        self.text_shadow = (30, 30, 30)
        
    def update(self):
        mouse_pos = self.mcskin2d.mousehandler.getpos()
        mouse_pressed = self.mcskin2d.inputengine.mouseispushed(1)
        mouse_clicked = self.mcskin2d.inputengine.mousepushed(1)
        
        # Check if mouse is over button
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.pressed = self.hovered and mouse_pressed
        
        # Execute action on click
        if self.hovered and mouse_clicked:
            for line in self.code:
                try:
                    exec(line)
                except:
                    pass
    
    def render(self):
        surface = pygame.Surface((self.width, self.height))
        surface.set_colorkey((0, 0, 0))
        
        # Choose colors based on state
        if self.pressed:
            bg_color = self.bg_pressed
        elif self.hovered:
            bg_color = self.bg_hover
        else:
            bg_color = self.bg_color
        
        # Draw button background with rounded corners effect
        pygame.draw.rect(surface, bg_color, (2, 2, self.width-4, self.height-4))
        pygame.draw.rect(surface, self.border_color, (0, 0, self.width, self.height), 2)
        
        # Add subtle gradient effect
        if not self.pressed:
            # Top highlight
            pygame.draw.line(surface, (min(255, bg_color[0] + 20), min(255, bg_color[1] + 20), min(255, bg_color[2] + 20)), 
                           (2, 2), (self.width-3, 2))
            # Bottom shadow
            pygame.draw.line(surface, (max(0, bg_color[0] - 20), max(0, bg_color[1] - 20), max(0, bg_color[2] - 20)), 
                           (2, self.height-3), (self.width-3, self.height-3))
        
        # Render text with shadow
        text_surface = self.mcskin2d.fontrenderer.rendersmall(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_x = (self.width - text_rect.width) // 2
        text_y = (self.height - text_rect.height) // 2
        
        # Adjust position if pressed
        if self.pressed:
            text_x += 1
            text_y += 1
        else:
            # Draw text shadow
            shadow_surface = self.mcskin2d.fontrenderer.rendersmall(self.text, True, self.text_shadow)
            surface.blit(shadow_surface, (text_x + 1, text_y + 1))
        
        surface.blit(text_surface, (text_x, text_y))
        
        return surface
    
    def getsurface(self):
        return self.render()
    
    def getpos(self):
        return self.pos
    
    def getrect(self):
        return self.rect


class ModernSlider:
    def __init__(self, label, length, pos, mcskin2d, min_val=0, max_val=255):
        self.label = label
        self.pos = pos
        self.length = length
        self.height = 24
        self.mcskin2d = mcskin2d
        self.min_val = min_val
        self.max_val = max_val
        self.value = max_val
        
        self.rect = pygame.Rect(pos, (length, self.height))
        self.slider_pos = length - 10  # Start at max value
        self.dragging = False
        
        # Modern colors
        self.track_color = (60, 60, 60)
        self.track_filled = (100, 150, 200)
        self.handle_color = (200, 200, 200)
        self.handle_hover = (220, 220, 220)
        self.text_color = (240, 240, 240)
        
    def update(self):
        mouse_pos = self.mcskin2d.mousehandler.getpos()
        mouse_pressed = self.mcskin2d.inputengine.mouseispushed(1)
        mouse_clicked = self.mcskin2d.inputengine.mousepushed(1)
        
        # Handle dragging
        if mouse_clicked and self.rect.collidepoint(mouse_pos):
            self.dragging = True
        
        if not mouse_pressed:
            self.dragging = False
        
        if self.dragging:
            relative_x = mouse_pos[0] - self.pos[0]
            self.slider_pos = max(5, min(self.length - 5, relative_x))
            
            # Calculate value
            progress = (self.slider_pos - 5) / (self.length - 10)
            self.value = int(self.min_val + progress * (self.max_val - self.min_val))
            return True
        
        return False
    
    def set_value(self, value):
        self.value = max(self.min_val, min(self.max_val, value))
        progress = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.slider_pos = 5 + progress * (self.length - 10)
    
    def get_value(self):
        return self.value
    
    def render(self):
        surface = pygame.Surface((self.length, self.height))
        surface.set_colorkey((0, 0, 0))
        
        # Draw track
        track_rect = (5, self.height//2 - 3, self.length - 10, 6)
        pygame.draw.rect(surface, self.track_color, track_rect)
        
        # Draw filled portion
        filled_width = self.slider_pos - 5
        if filled_width > 0:
            filled_rect = (5, self.height//2 - 3, filled_width, 6)
            pygame.draw.rect(surface, self.track_filled, filled_rect)
        
        # Draw handle
        mouse_pos = self.mcskin2d.mousehandler.getpos()
        handle_rect = pygame.Rect(self.slider_pos - 5, self.height//2 - 8, 10, 16)
        is_hovered = handle_rect.move(self.pos).collidepoint(mouse_pos)
        
        handle_color = self.handle_hover if is_hovered or self.dragging else self.handle_color
        pygame.draw.rect(surface, handle_color, (self.slider_pos - 5, self.height//2 - 8, 10, 16))
        pygame.draw.rect(surface, (80, 80, 80), (self.slider_pos - 5, self.height//2 - 8, 10, 16), 1)
        
        # Draw label
        if self.label:
            label_surface = self.mcskin2d.fontrenderer.rendersmall(self.label, True, self.text_color)
            surface.blit(label_surface, (2, 2))
        
        return surface
    
    def getsurface(self):
        return self.render()
    
    def getpos(self):
        return self.pos
    
    def getrect(self):
        return self.rect


class ModernColorDisplay:
    def __init__(self, pos, mcskin2d, size=(60, 60)):
        self.pos = pos
        self.size = size
        self.mcskin2d = mcskin2d
        self.color = [255, 255, 255]
        self.rect = pygame.Rect(pos, size)
        
    def update(self, color):
        self.color = list(color)
    
    def render(self):
        surface = pygame.Surface(self.size)
        
        # Fill with current color
        surface.fill(self.color)
        
        # Add modern border with depth
        border_color = (120, 120, 120)
        pygame.draw.rect(surface, border_color, (0, 0, self.size[0], self.size[1]), 3)
        
        # Add inner highlight
        pygame.draw.rect(surface, (200, 200, 200), (2, 2, self.size[0]-4, self.size[1]-4), 1)
        
        return surface
    
    def getsurface(self):
        return self.render()
    
    def getpos(self):
        return self.pos
    
    def getrect(self):
        return self.rect