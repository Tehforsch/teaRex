from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

WIDTH = 480
HEIGHT = 320


class TestApp(App):
    def build(self):
        Window.size = (WIDTH, HEIGHT)
        # Window.fullscreen = True

        layout = FloatLayout(size=(WIDTH, HEIGHT))
        buttons = []
        buttons.append(Button(text="Tee machen", pos=(100, 50), size=(10, 70)))
        buttons.append(Button(text="Tee matschen", pos=(400, 50), size=(10, 20)))
        buttons[0].bind(on_press=makeTea)
        for button in buttons:
            layout.add_widget(button)
        return layout


def makeTea(_button):
    print("hey was geht so baby")


TestApp().run()
