"""ILI9341 demo (simple touch demo)."""
from ili9341 import Display, color565
from xpt2046 import Touch
from machine import idle, Pin, SPI  # type: ignore
from ui import UI, Scene, Button, Label
from util import Pos, Color
from xglcd_font import XglcdFont

wire_length = 1
breadboard_spacing = 0.1
strip_length = 2

def test():
    """Test code."""
    spi1 = SPI(1, baudrate=60000000, sck=Pin(10), mosi=Pin(11))
    display = Display(spi1, dc=Pin(21), cs=Pin(13), rst=Pin(20), width=320, height=240, rotation=90)
    spi2 = SPI(0, baudrate=1000000, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    cascadia24 = XglcdFont('/CascadiaCode19x35.c', 19, 35)
    cascadia18 = XglcdFont('/CascadiaCode14x26.c', 14, 26)
    cascadia12 = XglcdFont('/CascadiaCode9x18.c', 9, 18)

    ui = UI(display, spi2)
    
    home_scene = Scene("home", Color(255, 255, 255))
    home_label = Label("home", Pos(0, 0), 319, 30, "Home",
                       Color(50, 100, 200), Color(50, 100, 200), Color(255, 255, 255), cascadia18)
    home_scene.add_widget(home_label)
    def cutwire_handler():
        ui.set_current_scene("cutwire")
        print("move to cutwire")
        ui.render_ui()
    def settings_handler():
        ui.set_current_scene("settings")
        print("move to settings")
        ui.render_ui()
    cutwire_button = Button("cutwire", Pos(20, 85), 130, 100, "Cut Wire", Color(0, 0, 0),
                         Color(50, 100, 200), Color(255, 255, 255), cascadia18, cutwire_handler)
    settings_button = Button("settings", Pos(180, 85), 130, 100, "Settings", Color(0, 0, 0),
                         Color(50, 100, 200), Color(255, 255, 255), cascadia18, settings_handler)
    home_scene.add_widget(cutwire_button)
    home_scene.add_widget(settings_button)
    ui.add_scene(home_scene)
    
    cutwire_scene = Scene("cutwire", Color(255, 255, 255))
    cutwire_label = Label("cutwire", Pos(0, 0), 319, 30, "Set Wire Length",
                       Color(50, 100, 200), Color(50, 100, 200), Color(255, 255, 255), cascadia18)
    wire_length_label = Label("wire length", Pos(100, 85), 120, 30, f"{wire_length} Holes",
                       Color(255, 255, 255), Color(255, 255, 255), Color(0, 0, 0), cascadia18)
    def minus_handler():
        global wire_length
        if wire_length > 1:
            wire_length -= 1
        wire_length_label.change_text(f"{wire_length} Holes")
        wire_length_label.render_widget(display)
    def plus_handler():
        global wire_length
        wire_length += 1
        wire_length_label.change_text(f"{wire_length} Holes")
        wire_length_label.render_widget(display)
    minus_button = Button("cutwire", Pos(40, 85), 40, 30, "-", Color(0, 0, 0),
                         Color(50, 100, 200), Color(255, 255, 255), cascadia18, minus_handler)
    plus_button = Button("settings", Pos(240, 85), 40, 30, "+", Color(0, 0, 0),
                         Color(50, 100, 200), Color(255, 255, 255), cascadia18, plus_handler)
    cutwire_scene.add_widget(plus_button)
    cutwire_scene.add_widget(minus_button)
    cutwire_scene.add_widget(wire_length_label)
    cutwire_scene.add_widget(cutwire_label)
    def back_handler():
        ui.set_current_scene("home")
        ui.render_ui()
    back_button = Button("back", Pos(20, 180), 100, 40, "< Back", Color(50, 100, 200),
                         Color(255, 255, 255), Color(50, 100, 200), cascadia18, back_handler)
    cutwire_scene.add_widget(back_button)
    def cut_handler():
        ui.set_current_scene("home")
        ui.render_ui()
    cut_button = Button("cut", Pos(200, 180), 100, 40, "Cut >", Color(0, 0, 0),
                         Color(50, 100, 200), Color(255, 255, 255), cascadia18, cut_handler)
    cutwire_scene.add_widget(cut_button)
    ui.add_scene(cutwire_scene)
    
    settings_scene = Scene("settings", Color(255, 255, 255))
    cutwire_label = Label("settings", Pos(0, 0), 319, 30, "Settings",
                       Color(50, 100, 200), Color(50, 100, 200), Color(255, 255, 255), cascadia18)
    space_label = Label("breadboard spacing", Pos(40, 40), 200, 30, f"Breadboard Hole Spacing",
                       Color(255, 255, 255), Color(255, 255, 255), Color(0, 0, 0), cascadia12)
    spacing_label = Label("spacing", Pos(100, 75), 120, 30, f"{breadboard_spacing} in",
                       Color(255, 255, 255), Color(255, 255, 255), Color(0, 0, 0), cascadia18)
    def spacing_minus_handler():
        global breadboard_spacing
        if breadboard_spacing > 0:
            breadboard_spacing -= 0.1
        spacing_label.change_text(f"{breadboard_spacing} in")
        spacing_label.render_widget(display)
    def spacing_plus_handler():
        global breadboard_spacing
        breadboard_spacing += 0.1
        spacing_label.change_text(f"{breadboard_spacing} in")
        spacing_label.render_widget(display)
    minus_button = Button("minus", Pos(40, 75), 40, 30, "-", Color(0, 0, 0),
                         Color(50, 100, 200), Color(255, 255, 255), cascadia18, spacing_minus_handler)
    plus_button = Button("plus", Pos(240, 75), 40, 30, "+", Color(0, 0, 0),
                         Color(50, 100, 200), Color(255, 255, 255), cascadia18, spacing_plus_handler)
    settings_scene.add_widget(plus_button)
    settings_scene.add_widget(minus_button)
    settings_scene.add_widget(space_label)
    settings_scene.add_widget(spacing_label)
    settings_scene.add_widget(cutwire_label)
    strip_header_label = Label("strip header", Pos(40, 100), 100, 30, f"Strip Length",
                       Color(255, 255, 255), Color(255, 255, 255), Color(0, 0, 0), cascadia12)
    strip_label = Label("spacing", Pos(100, 130), 120, 30, f"{strip_length} in",
                       Color(255, 255, 255), Color(255, 255, 255), Color(0, 0, 0), cascadia18)
    def strip_minus_handler():
        global strip_length
        if strip_length > 0:
            strip_length -= 0.1
        strip_label.change_text(f"{strip_length} cm")
        strip_label.render_widget(display)
    def strip_plus_handler():
        global strip_length
        strip_length += 0.1
        strip_label.change_text(f"{strip_length} cm")
        strip_label.render_widget(display)
    minus_button = Button("minus", Pos(40, 130), 40, 30, "-", Color(0, 0, 0),
                         Color(50, 100, 200), Color(255, 255, 255), cascadia18, strip_minus_handler)
    plus_button = Button("plus", Pos(240, 130), 40, 30, "+", Color(0, 0, 0),
                         Color(50, 100, 200), Color(255, 255, 255), cascadia18, strip_plus_handler)
    settings_scene.add_widget(plus_button)
    settings_scene.add_widget(minus_button)
    settings_scene.add_widget(strip_header_label)
    settings_scene.add_widget(strip_label)
    settings_scene.add_widget(cutwire_label)
    def back_handler():
        ui.set_current_scene("home")
        ui.render_ui()
    back_button = Button("back", Pos(20, 180), 100, 40, "< Back", Color(50, 100, 200),
                         Color(255, 255, 255), Color(50, 100, 200), cascadia18, back_handler)
    settings_scene.add_widget(back_button)
    ui.add_scene(settings_scene)
    
    ui.set_current_scene("home")
    ui.render_ui()
    
    try:
        while True:
            idle()

    except KeyboardInterrupt:
        print("\nCtrl-C pressed.  Cleaning up and exiting...")
    finally:
        display.cleanup()


test()
