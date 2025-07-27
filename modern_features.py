#Enhanced UI features for MCSkinStudio
#Keyboard shortcuts, tooltips, and modern layout improvements

import pygame
from pygame.locals import *

class KeyboardShortcutsPanel:
    """Display keyboard shortcuts in a modern panel"""
    def __init__(self, pos, mcskin2d):
        self.pos = pos
        self.mcskin2d = mcskin2d
        self.visible = False
        self.shortcuts = [
            ("Ctrl+S", "Save skin"),
            ("Ctrl+Z", "Undo"),
            ("Ctrl+Y", "Redo"),
            ("Ctrl+O", "Open skin"),
            ("F1", "Toggle help"),
            ("Space", "Eyedropper tool"),
        ]
        self.width = 200
        self.height = len(self.shortcuts) * 25 + 40
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(pos, (self.width, self.height))
        
    def toggle_visibility(self):
        self.visible = not self.visible
    
    def render(self):
        if not self.visible:
            return pygame.Surface((0, 0))
        
        self.surface.fill((60, 60, 60))
        pygame.draw.rect(self.surface, (100, 100, 100), (0, 0, self.width, self.height), 2)
        
        # Title
        title = self.mcskin2d.fontrenderer.rendersmall("Keyboard Shortcuts", True, (255, 255, 255))
        self.surface.blit(title, (10, 10))
        
        # Shortcuts
        y_offset = 35
        for shortcut, description in self.shortcuts:
            # Shortcut key
            key_text = self.mcskin2d.fontrenderer.rendersmall(shortcut, True, (150, 200, 255))
            self.surface.blit(key_text, (10, y_offset))
            
            # Description
            desc_text = self.mcskin2d.fontrenderer.rendersmall(description, True, (200, 200, 200))
            self.surface.blit(desc_text, (80, y_offset))
            
            y_offset += 25
        
        return self.surface
    
    def getsurface(self):
        return self.render()
    
    def getpos(self):
        return self.pos if self.visible else (0, 0)


class StatusBar:
    """Modern status bar showing current tool and color info"""
    def __init__(self, pos, mcskin2d, width=800):
        self.pos = pos
        self.width = width
        self.height = 25
        self.mcskin2d = mcskin2d
        self.surface = pygame.Surface((width, self.height))
        self.rect = pygame.Rect(pos, (width, self.height))
        
    def render(self, current_color, tool="Brush"):
        self.surface.fill((35, 35, 35))
        
        # Status text
        color_text = f"RGB({current_color[0]}, {current_color[1]}, {current_color[2]})"
        tool_text = f"Tool: {tool}"
        
        # Render status info
        color_surface = self.mcskin2d.fontrenderer.rendersmall(color_text, True, (200, 200, 200))
        tool_surface = self.mcskin2d.fontrenderer.rendersmall(tool_text, True, (200, 200, 200))
        
        self.surface.blit(tool_surface, (10, 5))
        self.surface.blit(color_surface, (120, 5))
        
        # Color preview
        color_rect = (self.width - 50, 5, 15, 15)
        pygame.draw.rect(self.surface, current_color, color_rect)
        pygame.draw.rect(self.surface, (100, 100, 100), color_rect, 1)
        
        return self.surface
    
    def getsurface(self, current_color=[255, 255, 255], tool="Brush"):
        return self.render(current_color, tool)
    
    def getpos(self):
        return self.pos


class ModernToolPalette:
    """Modern tool palette with icons and hover effects"""
    def __init__(self, pos, mcskin2d):
        self.pos = pos
        self.mcskin2d = mcskin2d
        self.tools = [
            ("Brush", "✏️"),
            ("Eraser", "🗑️"),
            ("Fill", "🪣"),
            ("Picker", "🎯"),
            ("Line", "📏"),
            ("Rectangle", "⬜"),
        ]
        self.selected_tool = 0
        self.tool_size = 40
        self.width = 50
        self.height = len(self.tools) * (self.tool_size + 5) + 10
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(pos, (self.width, self.height))
        
    def update(self):
        mouse_pos = self.mcskin2d.mousehandler.getpos()
        mouse_clicked = self.mcskin2d.inputengine.mousepushed(1)
        
        if mouse_clicked and self.rect.collidepoint(mouse_pos):
            relative_y = mouse_pos[1] - self.pos[1] - 5
            tool_index = relative_y // (self.tool_size + 5)
            if 0 <= tool_index < len(self.tools):
                self.selected_tool = tool_index
                return True
        return False
    
    def render(self):
        self.surface.fill((50, 50, 50))
        pygame.draw.rect(self.surface, (80, 80, 80), (0, 0, self.width, self.height), 2)
        
        mouse_pos = self.mcskin2d.mousehandler.getpos()
        
        y_offset = 5
        for i, (tool_name, icon) in enumerate(self.tools):
            tool_rect = (5, y_offset, self.tool_size, self.tool_size)
            
            # Check if mouse is hovering
            abs_rect = pygame.Rect(tool_rect[0] + self.pos[0], tool_rect[1] + self.pos[1], 
                                 tool_rect[2], tool_rect[3])
            is_hovered = abs_rect.collidepoint(mouse_pos)
            is_selected = i == self.selected_tool
            
            # Choose colors
            if is_selected:
                bg_color = (100, 150, 200)
            elif is_hovered:
                bg_color = (70, 70, 70)
            else:
                bg_color = (60, 60, 60)
            
            # Draw tool button
            pygame.draw.rect(self.surface, bg_color, tool_rect)
            pygame.draw.rect(self.surface, (120, 120, 120), tool_rect, 1)
            
            # Draw icon (simplified text for now since we can't render emoji easily)
            icon_text = self.mcskin2d.fontrenderer.rendersmall(tool_name[:1], True, (255, 255, 255))
            icon_rect = icon_text.get_rect()
            icon_x = tool_rect[0] + (tool_rect[2] - icon_rect.width) // 2
            icon_y = tool_rect[1] + (tool_rect[3] - icon_rect.height) // 2
            self.surface.blit(icon_text, (icon_x, icon_y))
            
            y_offset += self.tool_size + 5
        
        return self.surface
    
    def get_selected_tool(self):
        return self.tools[self.selected_tool][0] if self.tools else "Brush"
    
    def getsurface(self):
        return self.render()
    
    def getpos(self):
        return self.pos
    
    def getrect(self):
        return self.rect


class ModernFilePanel:
    """Modern file operations panel"""
    def __init__(self, pos, mcskin2d):
        self.pos = pos
        self.mcskin2d = mcskin2d
        self.width = 150
        self.height = 120
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(pos, (self.width, self.height))
        
        # File operation buttons
        self.buttons = [
            ("New", self._new_skin),
            ("Open", self._open_skin),
            ("Save", self._save_skin),
            ("Export", self._export_skin),
        ]
        self.button_height = 25
        
    def _new_skin(self):
        # Clear the drawing board
        self.mcskin2d.drawboard.surface = self.mcskin2d.contentloader.Char.copy()
        
    def _open_skin(self):
        # Open file dialog
        try:
            filename = self.mcskin2d.filedialog.askopenfilename(
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if filename:
                new_surface = pygame.image.load(filename).convert_alpha()
                self.mcskin2d.drawboard.surface = new_surface
        except:
            pass
    
    def _save_skin(self):
        # Save current skin
        try:
            filename = self.mcskin2d.filedialog.asksaveasfilename(
                defaultextension=".png", 
                filetypes=[("PNG files", "*.png")]
            )
            if filename:
                pygame.image.save(
                    pygame.transform.scale(self.mcskin2d.drawboard.getsurface(), (64, 32)), 
                    filename
                )
        except:
            pass
    
    def _export_skin(self):
        # Export at full resolution
        try:
            filename = self.mcskin2d.filedialog.asksaveasfilename(
                defaultextension=".png", 
                filetypes=[("PNG files", "*.png")]
            )
            if filename:
                pygame.image.save(self.mcskin2d.drawboard.getsurface(), filename)
        except:
            pass
    
    def update(self):
        mouse_pos = self.mcskin2d.mousehandler.getpos()
        mouse_clicked = self.mcskin2d.inputengine.mousepushed(1)
        
        if mouse_clicked and self.rect.collidepoint(mouse_pos):
            relative_y = mouse_pos[1] - self.pos[1] - 10
            button_index = relative_y // (self.button_height + 5)
            if 0 <= button_index < len(self.buttons):
                try:
                    self.buttons[button_index][1]()  # Execute button function
                except:
                    pass
                return True
        return False
    
    def render(self):
        self.surface.fill((55, 55, 55))
        pygame.draw.rect(self.surface, (90, 90, 90), (0, 0, self.width, self.height), 2)
        
        # Title
        title = self.mcskin2d.fontrenderer.rendersmall("File", True, (255, 255, 255))
        self.surface.blit(title, (10, 5))
        
        # Buttons
        mouse_pos = self.mcskin2d.mousehandler.getpos()
        y_offset = 30
        
        for i, (button_name, _) in enumerate(self.buttons):
            button_rect = (5, y_offset, self.width - 10, self.button_height)
            
            # Check hover
            abs_rect = pygame.Rect(button_rect[0] + self.pos[0], button_rect[1] + self.pos[1],
                                 button_rect[2], button_rect[3])
            is_hovered = abs_rect.collidepoint(mouse_pos)
            
            # Draw button
            bg_color = (75, 75, 75) if is_hovered else (65, 65, 65)
            pygame.draw.rect(self.surface, bg_color, button_rect)
            pygame.draw.rect(self.surface, (100, 100, 100), button_rect, 1)
            
            # Button text
            text = self.mcskin2d.fontrenderer.rendersmall(button_name, True, (255, 255, 255))
            text_x = button_rect[0] + 10
            text_y = button_rect[1] + (button_rect[3] - text.get_height()) // 2
            self.surface.blit(text, (text_x, text_y))
            
            y_offset += self.button_height + 5
        
        return self.surface
    
    def getsurface(self):
        return self.render()
    
    def getpos(self):
        return self.pos
    
    def getrect(self):
        return self.rect