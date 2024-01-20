from xpt2046 import Touch
from machine import idle, Pin, SPI  # type: ignore
from time import sleep
from util import Pos, Color

class UI(object):
    def __init__(self, display, spi2):
        self.display = display
        self.touch = Touch(spi2, cs=Pin(5), int_pin=Pin(0),
                           int_handler=self.touchscreen_press)
        self.scenes = {}
        self.current_scene = ""
        
    def render_ui(self):
        if self.current_scene == "":
            self.display.fill_rectangle(0, 0, 320, 240, Color(255, 255, 255).to_color565())
            return
        
        if self.current_scene in self.scenes:
            self.scenes[self.current_scene].render_scene(self.display)
                    
    def add_scene(self, scene):
        self.scenes[scene.uid] = scene
        
    def set_current_scene(self, scene_id):
        self.current_scene = scene_id
    
    def touchscreen_press(self, y, x):
        if self.current_scene in self.scenes:
            scene = self.scenes[self.current_scene]
            for widget in scene.widgets:
                if widget.widget_type == "button" and widget.is_pressed(x, y):
                    widget.when_pressed(self.display)

class Scene(object):
    def __init__(self, uid, bg_color = Color(255, 255, 255)):
        self.uid = uid
        self.bg_color = bg_color
        self.widgets = []
    
    def render_scene(self, display):
        display.fill_rectangle(0, 0, 320, 240, self.bg_color.to_color565())
        for widget in self.widgets:
            widget.render_widget(display)
    
    def add_widget(self, widget):
        self.widgets.append(widget)
            
class Widget(object):
    def __init__(self, widget_type):
        """
        Args:
            widget_type: string -> "button", "label"
        """
        self.widget_type = widget_type
        
    def render_widget(self):
        pass

class Button(Widget):
    def __init__(self, uid, coord, width, height, label, border_color, bg_color, font_color, font, touch_handler):
        """
        Args:
            uid: string -> unique button id
            coord: Pos -> top left position of the button
            width: number -> button width
            height: number -> button height
            label: string -> text displayed inside button
            border_color: Color -> color of button border
            bg_color: Color -> color of button background
            font_color: Color -> color of button text
            font: XglcdFont -> font of button text
            touch_handler: function -> function executed after button pressed
        """
        super().__init__("button")
        self.uid = uid
        self.coord = coord
        self.width = width
        self.height = height
        self.top_left = self.coord
        self.bottom_right = Pos(self.coord.x + self.width, self.coord.y + self.height)
        self.label = label
        self.border_color = border_color
        self.bg_color = bg_color
        self.pressed_color = bg_color.darker()
        self.font_color = font_color
        self.font = font
        self.touch_handler = touch_handler

    def get_bound_box(self):
        return (self.top_left, self.bottom_right)
    
    def is_pressed(self, x, y):
        return (self.top_left.x <= x and x < self.bottom_right.x) and (self.top_left.y <= y and y < self.bottom_right.y)

    def when_pressed(self, display):
        self.render_widget(display, self.pressed_color)
        sleep(.3)
        self.render_widget(display, self.bg_color)
        self.touch_handler()

    def render_widget(self, display, button_color=None):
        if button_color is None:
            button_color = self.bg_color
        display.fill_rectangle(self.coord.x, self.coord.y, self.width, self.height, button_color.to_color565())
        text_width = self.font.measure_text(self.label)
        text_height = self.font.height
        text_x = self.coord.x + int((self.width - text_width) / 2)
        text_y = self.coord.y + int((self.height - text_height) / 2)
        display.draw_text(text_x, text_y, self.label, self.font, 
                          self.font_color.to_color565(), background=button_color.to_color565(), landscape=False)
        display.draw_hline(self.coord.x, self.coord.y, self.width, self.border_color.to_color565())
        display.draw_hline(self.coord.x, self.coord.y + self.height, self.width, self.border_color.to_color565())
        display.draw_vline(self.coord.x, self.coord.y, self.height, self.border_color.to_color565())
        display.draw_vline(self.coord.x + self.width, self.coord.y, self.height, self.border_color.to_color565())
  
class Label(Widget):
    def __init__(self, uid, coord, width, height, label, border_color, bg_color, font_color, font):
        """
        Args:
            uid: string -> unique button id
            coord: Pos -> top left position of the button
            width: number -> button width
            height: number -> button height
            label: string -> text displayed inside button
            border_color: Color -> color of button border
            bg_color: Color -> color of button background
            font_color: Color -> color of button text
            font: XglcdFont -> font of button text
        """
        super().__init__("label")
        self.uid = uid
        self.coord = coord
        self.width = width
        self.height = height
        self.top_left = self.coord
        self.bottom_right = Pos(self.coord.x + self.width, self.coord.y + self.height)
        self.label = label
        self.border_color = border_color
        self.bg_color = bg_color
        self.font_color = font_color
        self.font = font

    def get_bound_box(self):
        return (self.top_left, self.bottom_right)

    def render_widget(self, display, box_color=None):
        if box_color is None:
            box_color = self.bg_color
        display.fill_rectangle(self.coord.x, self.coord.y, self.width, self.height, box_color.to_color565())
        text_width = self.font.measure_text(self.label)
        text_height = self.font.height
        text_x = self.coord.x + int((self.width - text_width) / 2)
        text_y = self.coord.y + int((self.height - text_height) / 2)
        display.draw_text(text_x, text_y, self.label, self.font, 
                          self.font_color.to_color565(), background=box_color.to_color565(), landscape=False)
        display.draw_hline(self.coord.x, self.coord.y, self.width, self.border_color.to_color565())
        display.draw_hline(self.coord.x, self.coord.y + self.height, self.width, self.border_color.to_color565())
        display.draw_vline(self.coord.x, self.coord.y, self.height, self.border_color.to_color565())
        display.draw_vline(self.coord.x + self.width, self.coord.y, self.height, self.border_color.to_color565())
    
    def change_text(self, new_text):
        self.label = new_text
    
    
    
    
    
