import pygame, os, sys, string
import scoring
from pygame.locals import *
from time import sleep

pygame.init()
pygame.display.set_mode((534,480))
font = pygame.font.Font(None, 18)
font2 = pygame.font.Font(None, 3)

'''Load image resources'''
#TODO: Incorporate tiles/squares into a single .png
try:
    #Creates a dictionary of images of tiles stored as values, each key being a letter of the alphabet
    tile_load = {}
    for i in xrange(ord('a'), ord('z')+1):
        tile_load[chr(i)] = pygame.image.load('graphics/tile_%s.gif' % (chr(i))).convert()
    tile_load['?'] = pygame.image.load('graphics/tile_blank.gif').convert()
    
    #Define board square image resources
    square_blank = pygame.image.load('graphics/square_blank.gif').convert()
    square_dl = pygame.image.load('graphics/square_dl.gif').convert()
    square_tl = pygame.image.load('graphics/square_tl.gif').convert()
    square_dw = pygame.image.load('graphics/square_dw.gif').convert()
    square_tw = pygame.image.load('graphics/square_tw.gif').convert()
    square_start = pygame.image.load('graphics/square_start.gif').convert()

    button_nor = pygame.image.load('graphics/button.gif').convert()
    button_ovr = pygame.image.load('graphics/button_ovr.gif').convert()
    rack_img = pygame.image.load('graphics/rack.gif').convert()
    rack_img.set_colorkey((255,255,255))
    background = pygame.image.load('graphics/background.gif').convert()
    switch_bg = pygame.image.load('graphics/switch_bg.gif').convert()
    blank_bg = pygame.image.load('graphics/blank.gif').convert()
    choose_bg = pygame.image.load('graphics/choose_bg.gif').convert()
    shaded = pygame.image.load('graphics/shaded.gif').convert()
    shaded.set_colorkey((255,255,255))
    prompt_box_image = pygame.image.load('graphics/prompt_box.gif').convert()
    
except pygame.error:
    sys.exit('Missing game sprites!')
    
class IterRegisitry(type):
    def __iter__(cls):
        return iter(cls._registry)

class Tile_obj(pygame.sprite.Sprite):
    
    __metaclass__ = IterRegisitry
    _registry = []
    
    def __init__(self, position,letter):

      # Call pygame.sprite.Sprite.__init__ to do some internal work
        pygame.sprite.Sprite.__init__(self)

        self._registry.append(self)
        self.image = tile_load[letter]
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        
        self.rect.x = position[0]
        self.rect.y = position[1] 
        self.last_position = (position[0],position[1])
        
        self.dragged = False 
        self.visible = True
        self.locked = False
        self.swap = False
        #set ownership, player 0 or player 1
        self.owner = 0
        self.ltr = letter.upper()
        self.value = scoring.TILE_VALUES[self.ltr]
        self.coord = (0,0)
        
        if self.ltr == '?': self.blank = True
        else: self.blank = False
        
    def mouseOver(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) :return True
        return False
    
    def move(self, pos, offset):
    
      # Move the rectangle by the specified amount
        self.rect.x = pos[0] - offset[0]
        self.rect.y = pos[1] - offset[1]
        
    def draw(self, surface):
        """ Draw the button to a surface """
        if self.visible : surface.blit(self.image, self.rect)


class Square_obj(pygame.sprite.Sprite):

    def __init__(self, position,type):

      # Call pygame.sprite.Sprite.__init__ to do some internal work
        pygame.sprite.Sprite.__init__(self)

        self.image = type
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1] 
        self.coord = (0,0)
        
        self.occupied = False
        
    def mouseOver(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) : 
            return True
            
    def draw(self, surface):
        """ Draw the button to a surface """
        surface.blit(self.image, self.rect)
        
class Button(pygame.sprite.Sprite):
    
    __metaclass__ = IterRegisitry
    _registry = []    

    def __init__(self, name, position):

      # Call pygame.sprite.Sprite.__init__ to do some internal work
        pygame.sprite.Sprite.__init__(self)
        
        self._registry.append(self)
        self.name = name
        self.image = button_nor
        self.image.set_colorkey((0, 0, 255))
        self.image_ovr = button_ovr
        self.image_ovr.set_colorkey((0, 0, 255))
        
      # Create a rectangle
        self.rect = pygame.Rect(0,0,54,22)

      # Position the rectangle
        self.rect.x = position[0]
        self.rect.y = position[1] 
        
        self.visible = True
        self.label = font.render(name, 1, (255,255,255))
        self.label_rect = self.label.get_rect()
        self.label_pos = (self.rect.centerx - (self.label_rect.w / 2), self.rect.centery - (self.label_rect.h / 2))

        self.focus = False
    
    def draw(self, surface):
        """ Draw the button to a surface """
        self.visible = True
        if self.focus :
            surface.blit(self.image_ovr, self.rect)
        else:
            surface.blit(self.image, self.rect)
        
        surface.blit(self.label, self.label_pos)
        
    def mouseOver(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and self.visible: 
            return True
    
    def buttonClick(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                sleep(.2)
                return True
        return False
        
class Label_obj(pygame.sprite.Sprite):
    
    __metaclass__ = IterRegisitry
    _registry = []    
    last_focus = None

    def __init__(self, name = '', position = (0,0), size = 18, color = (255,255,255), clickable = False, link = None):

      # Call pygame.sprite.Sprite.__init__ to do some internal work
        pygame.sprite.Sprite.__init__(self)
        
        self.visible = False
        self.name = name
        self.size = size
        self.clickable = clickable
        self.centered = False
        self.link = link
        self.color = color
        self.s_color = (255,0,255)
        self.c_color = self.color
        self.position = position
        self.text = font.render(self.name, self.size, self.c_color)
        self.rect = pygame.Rect(0,0,self.text.get_width(),self.text.get_height())
      # Position the rectangle
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.focus = False
        self.last_focus = False
        self._registry.append(self)

    def draw(self, surface):
        """ Draw the button to a surface """
        if self.visible :
            self.c_color = self.color
            if self.focus and self.clickable: 
                self.c_color = self.s_color
                Label_obj.last_focus = self
            label = font.render(self.name, self.size, self.c_color)
            label_cen = label.get_rect()
            label_cen.centerx = surface.get_rect().centerx + (label_cen.centerx /4)
            label_cen.centery = surface.get_rect().centery - 10
            if self.centered :
                surface.blit(label, label_cen)
            else:
                surface.blit(label, self.position)
                
    def mouseOver(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and self.visible: 
            return True
    
    def buttonClick(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                sleep(.2)
                return True
        return False
        
        
class Prompt_box(pygame.sprite.Sprite):

    def __init__(self, position, message):

      # Call pygame.sprite.Sprite.__init__ to do some internal work
        pygame.sprite.Sprite.__init__(self)
        
        self.image = prompt_box_image
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1] 
        self.message = message
        self.visible = False
        self.button = Button('OK', (self.rect.centerx-25, self.rect.centery +20 ))
        
    def draw(self, surface):
        """ Draw the button to a surface """
        if self.visible :
            self.text = Label_obj(self.message,
                            (self.rect.centerx ,self.rect.centery),18,
                            (255,255,255),True)
            surface.blit(self.image, self.rect)
            self.text.draw(surface)
            self.button.draw(surface)
            if self.button.buttonClick() :
                self.visible = False
        
        
class Rack_slot(pygame.sprite.Sprite):

    def __init__(self, position):

      # Call pygame.sprite.Sprite.__init__ to do some internal work
        pygame.sprite.Sprite.__init__(self)

      # Create a rectangle
        self.rect = pygame.Rect(0,0,32,32)

      # Position the rectangle
        self.rect.x = position[0]
        self.rect.y = position[1] 
        
        self.occupied = False
        
class Game_info:
    
    gameCnt = 0

    def __init__(self, id, player_2, match):
        self.id = id
        self.player_2 = player_2
        self.match = match
        Game_info.gameCnt += 1
        self.num = Game_info.gameCnt
        
        self.active = False
      
      
# input lib
class ConfigError(KeyError): pass

class Config:
    """ A utility for configuration """
    def __init__(self, options, *look_for):
        assertions = []
        for key in look_for:
            if key[0] in options.keys(): exec('self.'+key[0]+' = options[\''+key[0]+'\']')
            else: exec('self.'+key[0]+' = '+key[1])
            assertions.append(key[0])
        for key in options.keys():
            if key not in assertions: raise ConfigError(key+' not expected as option')

class Input:
    
    __metaclass__ = IterRegisitry
    _registry = []
    
    """ A text input for pygame apps """
    def __init__(self, **options):
        """ Options: x, y, font, color, restricted, maxlength, prompt """
        self.options = Config(options, ['x', '0'], ['y', '0'], ['font', 'pygame.font.Font(None, 20)'],
                              ['color', '(0,0,0)'], ['password','False'], ['restricted', '\'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\\\'()*+,-./:;<=>?@[\]^_`{|}~\''],
                              ['maxlength', '-1'], ['prompt', '\'\''], ['size', '(0,0,300,20)'], ['visible', 'False'])
        self.x = self.options.x; self.y = self.options.y
        self.font = self.options.font
        self.color = self.options.color
        self.s_color = (255,0,255)
        self.c_color = self.options.color
        self.password = self.options.password
        self.restricted = self.options.restricted
        self.maxlength = self.options.maxlength
        self.prompt = self.options.prompt; self.value = ''
        self.shifted = False
        self.rect = pygame.Rect(0,0,8*self.maxlength,15)
      # Position the rectangle
        self.rect.x = self.x
        self.rect.y = self.y
        self.focus = False
        self.visible = self.options.visible
        self._registry.append(self)

    def set_pos(self, x, y):
        """ Set the position to x, y """
        self.x = x
        self.y = y

    def set_font(self, font):
        """ Set the font for the input """
        self.font = font

    def draw(self, surface):
        """ Draw the text input to a surface """
        if self.visible :
            self.c_color = self.color
            if self.focus : self.c_color = self.s_color
            if self.password  :
                text = self.font.render(self.prompt+ ('*' * len(self.value)), 1, self.c_color)
            else :
                text = self.font.render(self.prompt+ self.value, 1, self.c_color)
            surface.fill((255,255,255), self.rect, special_flags=0)
            surface.blit(text, (self.x, self.y))

    def update(self, events):
        """ Update the input based on passed events """
        for event in events:
            if event.type == KEYUP:
                if event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = False
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE: self.value = self.value[:-1]
                elif event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = True
                elif event.key == K_SPACE: self.value += ' '
                if not self.shifted:
                    if event.key == K_a and 'a' in self.restricted: self.value += 'a'
                    elif event.key == K_b and 'b' in self.restricted: self.value += 'b'
                    elif event.key == K_c and 'c' in self.restricted: self.value += 'c'
                    elif event.key == K_d and 'd' in self.restricted: self.value += 'd'
                    elif event.key == K_e and 'e' in self.restricted: self.value += 'e'
                    elif event.key == K_f and 'f' in self.restricted: self.value += 'f'
                    elif event.key == K_g and 'g' in self.restricted: self.value += 'g'
                    elif event.key == K_h and 'h' in self.restricted: self.value += 'h'
                    elif event.key == K_i and 'i' in self.restricted: self.value += 'i'
                    elif event.key == K_j and 'j' in self.restricted: self.value += 'j'
                    elif event.key == K_k and 'k' in self.restricted: self.value += 'k'
                    elif event.key == K_l and 'l' in self.restricted: self.value += 'l'
                    elif event.key == K_m and 'm' in self.restricted: self.value += 'm'
                    elif event.key == K_n and 'n' in self.restricted: self.value += 'n'
                    elif event.key == K_o and 'o' in self.restricted: self.value += 'o'
                    elif event.key == K_p and 'p' in self.restricted: self.value += 'p'
                    elif event.key == K_q and 'q' in self.restricted: self.value += 'q'
                    elif event.key == K_r and 'r' in self.restricted: self.value += 'r'
                    elif event.key == K_s and 's' in self.restricted: self.value += 's'
                    elif event.key == K_t and 't' in self.restricted: self.value += 't'
                    elif event.key == K_u and 'u' in self.restricted: self.value += 'u'
                    elif event.key == K_v and 'v' in self.restricted: self.value += 'v'
                    elif event.key == K_w and 'w' in self.restricted: self.value += 'w'
                    elif event.key == K_x and 'x' in self.restricted: self.value += 'x'
                    elif event.key == K_y and 'y' in self.restricted: self.value += 'y'
                    elif event.key == K_z and 'z' in self.restricted: self.value += 'z'
                    elif event.key == K_0 and '0' in self.restricted: self.value += '0'
                    elif event.key == K_1 and '1' in self.restricted: self.value += '1'
                    elif event.key == K_2 and '2' in self.restricted: self.value += '2'
                    elif event.key == K_3 and '3' in self.restricted: self.value += '3'
                    elif event.key == K_4 and '4' in self.restricted: self.value += '4'
                    elif event.key == K_5 and '5' in self.restricted: self.value += '5'
                    elif event.key == K_6 and '6' in self.restricted: self.value += '6'
                    elif event.key == K_7 and '7' in self.restricted: self.value += '7'
                    elif event.key == K_8 and '8' in self.restricted: self.value += '8'
                    elif event.key == K_9 and '9' in self.restricted: self.value += '9'
                    elif event.key == K_BACKQUOTE and '`' in self.restricted: self.value += '`'
                    elif event.key == K_MINUS and '-' in self.restricted: self.value += '-'
                    elif event.key == K_EQUALS and '=' in self.restricted: self.value += '='
                    elif event.key == K_LEFTBRACKET and '[' in self.restricted: self.value += '['
                    elif event.key == K_RIGHTBRACKET and ']' in self.restricted: self.value += ']'
                    elif event.key == K_BACKSLASH and '\\' in self.restricted: self.value += '\\'
                    elif event.key == K_SEMICOLON and ';' in self.restricted: self.value += ';'
                    elif event.key == K_QUOTE and '\'' in self.restricted: self.value += '\''
                    elif event.key == K_COMMA and ',' in self.restricted: self.value += ','
                    elif event.key == K_PERIOD and '.' in self.restricted: self.value += '.'
                    elif event.key == K_SLASH and '/' in self.restricted: self.value += '/'
                elif self.shifted:
                    if event.key == K_a and 'A' in self.restricted: self.value += 'A'
                    elif event.key == K_b and 'B' in self.restricted: self.value += 'B'
                    elif event.key == K_c and 'C' in self.restricted: self.value += 'C'
                    elif event.key == K_d and 'D' in self.restricted: self.value += 'D'
                    elif event.key == K_e and 'E' in self.restricted: self.value += 'E'
                    elif event.key == K_f and 'F' in self.restricted: self.value += 'F'
                    elif event.key == K_g and 'G' in self.restricted: self.value += 'G'
                    elif event.key == K_h and 'H' in self.restricted: self.value += 'H'
                    elif event.key == K_i and 'I' in self.restricted: self.value += 'I'
                    elif event.key == K_j and 'J' in self.restricted: self.value += 'J'
                    elif event.key == K_k and 'K' in self.restricted: self.value += 'K'
                    elif event.key == K_l and 'L' in self.restricted: self.value += 'L'
                    elif event.key == K_m and 'M' in self.restricted: self.value += 'M'
                    elif event.key == K_n and 'N' in self.restricted: self.value += 'N'
                    elif event.key == K_o and 'O' in self.restricted: self.value += 'O'
                    elif event.key == K_p and 'P' in self.restricted: self.value += 'P'
                    elif event.key == K_q and 'Q' in self.restricted: self.value += 'Q'
                    elif event.key == K_r and 'R' in self.restricted: self.value += 'R'
                    elif event.key == K_s and 'S' in self.restricted: self.value += 'S'
                    elif event.key == K_t and 'T' in self.restricted: self.value += 'T'
                    elif event.key == K_u and 'U' in self.restricted: self.value += 'U'
                    elif event.key == K_v and 'V' in self.restricted: self.value += 'V'
                    elif event.key == K_w and 'W' in self.restricted: self.value += 'W'
                    elif event.key == K_x and 'X' in self.restricted: self.value += 'X'
                    elif event.key == K_y and 'Y' in self.restricted: self.value += 'Y'
                    elif event.key == K_z and 'Z' in self.restricted: self.value += 'Z'
                    elif event.key == K_0 and ')' in self.restricted: self.value += ')'
                    elif event.key == K_1 and '!' in self.restricted: self.value += '!'
                    elif event.key == K_2 and '@' in self.restricted: self.value += '@'
                    elif event.key == K_3 and '#' in self.restricted: self.value += '#'
                    elif event.key == K_4 and '$' in self.restricted: self.value += '$'
                    elif event.key == K_5 and '%' in self.restricted: self.value += '%'
                    elif event.key == K_6 and '^' in self.restricted: self.value += '^'
                    elif event.key == K_7 and '&' in self.restricted: self.value += '&'
                    elif event.key == K_8 and '*' in self.restricted: self.value += '*'
                    elif event.key == K_9 and '(' in self.restricted: self.value += '('
                    elif event.key == K_BACKQUOTE and '~' in self.restricted: self.value += '~'
                    elif event.key == K_MINUS and '_' in self.restricted: self.value += '_'
                    elif event.key == K_EQUALS and '+' in self.restricted: self.value += '+'
                    elif event.key == K_LEFTBRACKET and '{' in self.restricted: self.value += '{'
                    elif event.key == K_RIGHTBRACKET and '}' in self.restricted: self.value += '}'
                    elif event.key == K_BACKSLASH and '|' in self.restricted: self.value += '|'
                    elif event.key == K_SEMICOLON and ':' in self.restricted: self.value += ':'
                    elif event.key == K_QUOTE and '"' in self.restricted: self.value += '"'
                    elif event.key == K_COMMA and '<' in self.restricted: self.value += '<'
                    elif event.key == K_PERIOD and '>' in self.restricted: self.value += '>'
                    elif event.key == K_SLASH and '?' in self.restricted: self.value += '?'

        if len(self.value) > self.maxlength and self.maxlength >= 0: self.value = self.value[:-1]

    def mouseOver(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) : return True
    
    def buttonClick(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) :
            if pygame.mouse.get_pressed()[0]:
                sleep(.2)
                return True
        return False