##############
##rin0 shell##
##############

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window, Keyboard
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.label import Label


class Shell(Widget):
    def __init__(self):
        super(Shell, self).__init__()
        
        self.size = Window.size
        
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
        #with self.canvas:
        #    Color(0.2, 0.7, 0.2)
        #    Rectangle(pos=(0,0), size=self.size)
        
        self.command = "C:\working\dir\goes\here>_"
        self.command_line = Label(text = self.command)
        self.add_widget(self.command_line)
        
        self.log = Label()
        self.add_widget(self.log)
        
        Clock.schedule_interval(self.update, 1.0/60.0)
        Clock.schedule_interval(self.blink_cursor, 1.0/2)
        
    def blink_cursor(self, *ignore):
        if self.command[-1] == '_':
            self.command = self.command[:-1] + ' '
        elif self.command[-1] == ' ':
            self.command = self.command[:-1] + '_'
        
    def update(self, *ignore):
        self.size = Window.size
        
        '''
        with self.canvas:
            Color(0.5, 0.5, 1.0)
            Rectangle(pos=(0,0), size=self.size)
        '''
        
        self.command_line.text_size = self.command_line.size
        self.command_line.text = self.command
        self.command_line.width = self.width
        self.command_line.height = self.command_line.font_size
        
        #self.log.pos = (0, self.command_line.height)
        self.log.width = self.width
        self.log.height = self.height-self.command_line.height
        #self.log.pos = (0, self.command_line.height)
        #self.log.x = 0
            
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
            
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode)
        print(modifiers)
        ignorekeys = ['shift', 'capslock']
        try:
            if len(modifiers) == 1 and modifiers[0] == 'shift':
                text = text.capitalize()
                
            if keycode[1] == 'enter':
                self.log.text += '\n{}'.format(self.command[:-1])
                #!!! -> Process Commands Here <- !!!#
                self.command = '>_'
                
            if keycode[1] not in ignorekeys:
                self.command = self.command[:-1]
                self.command += text + '_'
        except:
            pass
            
class ShellApp(App):
    def build(self):
        self.shell = Shell()
        self.title = 'Rin0 Shell'
        return self.shell
        
    def on_resize(self, width, height):
        self.shell.size = Window.size
    

if __name__ == '__main__':
    ShellApp().run()