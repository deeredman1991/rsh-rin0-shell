##############
##rin0 shell##
##############

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window, Keyboard
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.label import Label
import json
    
with open('settings.json', 'r') as infile:
    SETTINGS = json.load(infile)

class Shell(Widget):
    def __init__(self):
        super(Shell, self).__init__()
        
        self.size = Window.size
        
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
        self.workingdir = "C:\working\dir\goes\here>"
        self.command = ''
        self.cursor = '_'
        
        self.command_line = Label(font_name = SETTINGS["Font Path"], font_size = SETTINGS["Font Size"])
        
        self.add_widget(self.command_line)
        
        self.log = Label(font_name = SETTINGS["Font Path"], font_size = SETTINGS["Font Size"])
        self.add_widget(self.log)
        
        Clock.schedule_interval(self.update, 1.0/60.0)
        Clock.schedule_interval(self.blink_cursor, 1.0/2)
        
    def blink_cursor(self, *ignore):
        if self.cursor == '_':
            self.cursor = ' '
        elif self.cursor == ' ':
            self.cursor = '_'
        
    def update(self, *ignore):
        self.size = Window.size
        
        #Draw Command Line
        self.command_line.text_size = self.command_line.size
        self.command_line.width = self.width
        self.command_line.height = self.command_line.font_size
        self.command_line.text = self.workingdir + self.command + self.cursor
        self.command_line.color = (SETTINGS["Text Colors"]["Command Line"]["Red"],
                                   SETTINGS["Text Colors"]["Command Line"]["Green"],
                                   SETTINGS["Text Colors"]["Command Line"]["Blue"], 1)
        #Draw Command Line Background
        with self.command_line.canvas.before:
            Color(SETTINGS["Background Colors"]["Command Line"]["Red"],
                  SETTINGS["Background Colors"]["Command Line"]["Green"],
                  SETTINGS["Background Colors"]["Command Line"]["Blue"], 1)
            Rectangle(pos=self.command_line.pos, size = self.command_line.size)
        
        #Draw Log
        self.log.text_size = self.log.size
        self.log.width = self.width
        self.log.height = self.height - self.command_line.font_size
        self.log.y = self.command_line.height
        self.log.color = (SETTINGS["Text Colors"]["Log"]["Red"],
                          SETTINGS["Text Colors"]["Log"]["Green"],
                          SETTINGS["Text Colors"]["Log"]["Blue"], 1)
        #Draw Log Background
        with self.log.canvas.before:
            Color(SETTINGS["Background Colors"]["Log"]["Red"],
                  SETTINGS["Background Colors"]["Log"]["Green"],
                  SETTINGS["Background Colors"]["Log"]["Blue"], 1)
            Rectangle(pos=self.log.pos, size = self.log.size)
            
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
            
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode)
        print(modifiers)
        ignorekeys = ['shift', 'capslock', 'backspace']
        try:
            if len(modifiers) == 1 and modifiers[0] == 'shift':
                text = text.capitalize()
                
            if keycode[1] == 'enter':
                self.log.text += '{}{}\n'.format(self.workingdir, self.command)
                #!!! -> Process Commands Here <- !!!#
                output = 'output goes here'
                self.log.text += output + '\n\n'
                self.command = ''
                
            if keycode[1] == 'backspace':
                self.command = self.command[:-1]
                
            if keycode[1] not in ignorekeys:
                self.command += text
        except:
            print("Fired exception!!!")
            
class ShellApp(App):
    def build(self):
        self.shell = Shell()
        self.title = 'Rin0 Shell'
        self.icon = 'images/icon.png'
        #background_color = (0, 0, 0, 1) #Red, Green, Blue, Alpha
        #Window.clearcolor = (background_color)
        return self.shell
        
    def on_resize(self, width, height):
        self.shell.size = Window.size
    

if __name__ == '__main__':
    ShellApp().run()