#MCSkin2D, a kind of funny skin editor!
#Programmed by SapperEngineer

import tkinter.filedialog as filedialog

import pygame
from pygame.locals import *
pygame.init()

import drawboard
import colorselector
import inputengine
import contentloader
import messhandler
import mousehandler
import fontrenderer
import gui
import skinpreview
import colorshower
import pixscreener
import swatch
from buttonactions import *

# Import modern UI components
import modern_gui
import modern_colorpicker
import modern_features

class mcskin2d():
    def __init__(self):
        self.filedialog = filedialog
        self.pygame = pygame #Needed for external modules's benefit
        self.tv = self.pygame.display.set_mode((800, 500), DOUBLEBUF)


        #Initialize variables
        self.contentloader = contentloader.contentloader(self)
        self.drawboard = drawboard.drawboard((0, 0), self)
        
        # Use modern color picker instead of old one
        self.modern_colorpicker = modern_colorpicker.ModernColorPicker((550, 50), self)
        self.colorselector = colorselector.colorselector((598, 290), self)  # Keep as backup
        
        self.inputengine = inputengine.inputengine()
        self.messhandler = messhandler.messhandler(self)
        self.mousehandler = mousehandler.mousehandler()
        self.fontrenderer = fontrenderer.fontrenderer("MC", self)
        self.skinpreview = skinpreview.skinpreview((640, 0), self)
        
        # Use modern color display
        self.modern_colorshow = modern_gui.ModernColorDisplay((10, 350), self, (80, 80))
        self.colorshower = colorshower.colorshower((10, 330), self)  # Keep as backup
        
        self.pixscreener = pixscreener.pixscreener()
        self.swatchpanel = swatch.swatches((220, 325), self)

        #Initialize modern gui elements
        self.modern_buttons = []
        self.modern_buttons.append(modern_gui.ModernButton("Save", SAVESKIN, (9, 450), self, width=80))
        self.modern_buttons.append(modern_gui.ModernButton("Undo", UNDO, (95, 450), self, width=60))
        self.modern_buttons.append(modern_gui.ModernButton("Redo", REDO, (160, 450), self, width=60))
        self.modern_buttons.append(modern_gui.ModernButton("Help", GETHELP, (225, 450), self, width=60))
        self.modern_buttons.append(modern_gui.ModernButton("Save Model", SAVEMODEL, (640, 350), self, width=100))
        
        # Initialize traditional gui stuff (kept for compatibility)
        self.guibuffer = []
        self.guibuffer.append(gui.button(" Save", SAVESKIN, (9, 471), self))
        self.guibuffer.append(gui.button(" Undo", UNDO, (70, 471), self))
        self.guibuffer.append(gui.button(" Redo", REDO, (131, 471), self))
        self.guibuffer.append(gui.button(" ^^^Current Color", NOTHING, (3, 374), self))
        self.guibuffer.append(gui.button(" SaveIm", SAVEMODEL, (719, 326), self))
        self.guibuffer.append(gui.button(" Credits and Help", GETHELP, (8, 427), self))
        self.guibuffer.append(gui.button(" -> ", SHIFTRIGHT, (763, 290), self))
        self.guibuffer.append(gui.button(" <- ", SHIFTLEFT, (642, 290), self))

        # Modern RGB/HSV sliders
        self.modern_sliders = {}
        self.modern_sliders['r'] = modern_gui.ModernSlider("Red", 200, (300, 400), self, 0, 255)
        self.modern_sliders['g'] = modern_gui.ModernSlider("Green", 200, (300, 430), self, 0, 255)
        self.modern_sliders['b'] = modern_gui.ModernSlider("Blue", 200, (300, 460), self, 0, 255)
        
        # Additional modern features
        self.keyboard_shortcuts = modern_features.KeyboardShortcutsPanel((600, 50), self)
        self.status_bar = modern_features.StatusBar((0, 475), self, 800)
        self.tool_palette = modern_features.ModernToolPalette((10, 50), self)
        self.file_panel = modern_features.ModernFilePanel((10, 200), self)
        self.current_tool = "Brush"

        # Keep original sliders for compatibility
        self.rgbbuffer = {}
        self.rgbbuffer['r'] = gui.slider("                               R", 255, (220, 420), self)
        self.rgbbuffer['g'] = gui.slider("                               G", 255, (220, 445), self)
        self.rgbbuffer['b'] = gui.slider("                               B", 255, (220, 470), self)
        self.rgbbuffer['re'] = gui.textvariable((50, 23), (476, 420), self)
        self.rgbbuffer['ge'] = gui.textvariable((50, 23), (476, 445), self)
        self.rgbbuffer['be'] = gui.textvariable((50, 23), (476, 470), self)



        #Flip screen to start all changes
        self.tv.fill((45, 45, 45))  # Modern dark background instead of light gray
        pygame.display.flip()

        pygame.display.set_caption("MCSkinStudio - Modern Edition")
        pygame.display.set_icon(self.contentloader.steveico)
        self.mousehandler.changecursor(mousehandler.cursors.regmouse)

    def mainloop(self):
        while 1:
            #Render stuff with modern dark theme
            self.tv.fill((45, 45, 45))  # Modern dark background
    
            #RENDER CODE - Modern UI with fallback to classic
            self.messhandler.registermesses([
                self.tv.blit(self.contentloader.mcwood, (0, 320)),
                # Render modern color picker
                self.tv.blit(self.modern_colorpicker.getsurface(), self.modern_colorpicker.getpos()),
                # Render modern color display
                self.tv.blit(self.modern_colorshow.getsurface(), self.modern_colorshow.getpos()),
                # Keep classic elements for compatibility
                self.tv.blit(self.contentloader.TranspImage, self.drawboard.getpos()),
                self.tv.blit(self.drawboard.getgriddedsurface(), self.drawboard.getpos()),
                self.tv.blit(self.contentloader.mcmelon, self.skinpreview.getpos()),
                self.tv.blit(self.skinpreview.getsurface(), self.skinpreview.getpos()),
                self.tv.blit(self.swatchpanel.getsurface(), self.swatchpanel.getpos())
            ])

            # Render modern buttons
            for button in self.modern_buttons:
                self.messhandler.registermess(self.tv.blit(button.getsurface(), button.getpos()))

            # Render modern sliders
            for slider_key in self.modern_sliders:
                slider = self.modern_sliders[slider_key]
                self.messhandler.registermess(self.tv.blit(slider.getsurface(), slider.getpos()))
            
            # Render modern features
            self.messhandler.registermess(self.tv.blit(self.tool_palette.getsurface(), self.tool_palette.getpos()))
            self.messhandler.registermess(self.tv.blit(self.file_panel.getsurface(), self.file_panel.getpos()))
            self.messhandler.registermess(self.tv.blit(self.keyboard_shortcuts.getsurface(), self.keyboard_shortcuts.getpos()))
            self.messhandler.registermess(self.tv.blit(self.status_bar.getsurface(self.drawboard.color, self.current_tool), self.status_bar.getpos()))

            # Keep classic GUI elements hidden for now (for compatibility)
            # for element in self.guibuffer:
            #     self.messhandler.registermess(self.tv.blit(element.getsurface(), element.getpos()))

            # for element in self.rgbbuffer:
            #     self.messhandler.registermess(self.tv.blit(self.rgbbuffer[element].getsurface(), self.rgbbuffer[element].getpos()))

            

            self.messhandler.cleanmesses() #Update them all

            #START INPUT CODE
            self.inputengine.copybuffer()
            if not (self.inputengine.mouseispushed(1) and self.inputengine.mouseispushed(3)):self.mousehandler.update()
            else:self.mousehandler.updateondisplay()
            self.inputengine.killifrequest()

            self.drawboard.draw()
            
            # Update modern UI components
            # Update modern color picker
            if self.modern_colorpicker.update():
                new_rgb = self.modern_colorpicker.get_rgb()
                self.drawboard.color = new_rgb
                # Sync with modern sliders
                self.modern_sliders['r'].set_value(new_rgb[0])
                self.modern_sliders['g'].set_value(new_rgb[1])
                self.modern_sliders['b'].set_value(new_rgb[2])
            
            # Update modern color display
            self.modern_colorshow.update(self.drawboard.color)

            self.skinpreview.update()
            self.swatchpanel.update()

            # Update modern buttons
            for button in self.modern_buttons:
                button.update()
            
            # Update modern features
            if self.tool_palette.update():
                self.current_tool = self.tool_palette.get_selected_tool()
            
            self.file_panel.update()
            
            # Update modern sliders
            for slider_key in self.modern_sliders:
                slider = self.modern_sliders[slider_key]
                if slider.update():
                    # Update drawboard color when sliders change
                    if slider_key == 'r':
                        self.drawboard.color[0] = slider.get_value()
                    elif slider_key == 'g':
                        self.drawboard.color[1] = slider.get_value()
                    elif slider_key == 'b':
                        self.drawboard.color[2] = slider.get_value()
                    
                    # Update modern color picker when sliders change
                    self.modern_colorpicker.set_rgb(self.drawboard.color)

            # Keep legacy color selector for compatibility with classic mode
            newcol = self.colorselector.getcol()
            if newcol: 
                self.drawboard.color = list(newcol)
                # Sync with modern components
                self.modern_colorpicker.set_rgb(self.drawboard.color)
                self.modern_sliders['r'].set_value(self.drawboard.color[0])
                self.modern_sliders['g'].set_value(self.drawboard.color[1])
                self.modern_sliders['b'].set_value(self.drawboard.color[2])

            # Keep classic GUI update for compatibility (hidden)
            for element in self.guibuffer: #GUI UPDATE
                element.update()

            for element in self.rgbbuffer: #GUI UPDATE
                if self.rgbbuffer[element].update():
                    if element == 'r':
                        self.drawboard.color[0] = self.rgbbuffer[element].getvalue()
                        self.rgbbuffer[element + 'e'].setvalue(self.rgbbuffer[element].getvalue())

                    if element == 'g':
                        self.drawboard.color[1] = self.rgbbuffer[element].getvalue()
                        self.rgbbuffer[element + 'e'].setvalue(self.rgbbuffer[element].getvalue())

                    if element == 'b':
                        self.drawboard.color[2] = self.rgbbuffer[element].getvalue()
                        self.rgbbuffer[element + 'e'].setvalue(self.rgbbuffer[element].getvalue())

            # Modern keyboard shortcuts
            keys_pressed = pygame.key.get_pressed()
            
            # F1 - Toggle help/shortcuts
            if self.inputengine.keypushed(K_F1):
                self.keyboard_shortcuts.toggle_visibility()
            
            # Ctrl+S - Save
            if keys_pressed[K_LCTRL] and self.inputengine.keypushed(K_s):
                self.file_panel._save_skin()
            
            # Ctrl+O - Open
            if keys_pressed[K_LCTRL] and self.inputengine.keypushed(K_o):
                self.file_panel._open_skin()
            
            # Ctrl+Z - Undo (if implemented)
            if keys_pressed[K_LCTRL] and self.inputengine.keypushed(K_z):
                try:
                    for line in UNDO:
                        exec(line)
                except:
                    pass
            
            # Legacy keyboard shortcuts
            if self.inputengine.charpushed(chr(19)):
                #Save image
                try:
                    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Minecraft Skin PNG file", ".png")])
                    pygame.image.save(pygame.transform.scale(self.drawboard.getsurface(), (64, 32)), filename)
                except:pass

            if self.inputengine.charpushed(chr(12)):
                filename = filedialog.askopenfilename()
                newsurf = pygame.image.load(filename).convert_alpha()
                self.drawboard.surface = newsurf

            if self.inputengine.mouseispushed(1) and self.inputengine.mouseispushed(3) and not self.mousehandler.getrect().colliderect(self.drawboard.getrect()):
                newcolor = self.drawboard.color = list(self.pixscreener.getpixel(self.mousehandler.getposondisplay()))
                self.rgbbuffer['r'].setslider(newcolor[0])
                self.rgbbuffer['g'].setslider(newcolor[1])
                self.rgbbuffer['b'].setslider(newcolor[2])



            self.inputengine.delbuffer()
            #END INPUT CODE


#Start the program
program = mcskin2d()
program.mainloop()
