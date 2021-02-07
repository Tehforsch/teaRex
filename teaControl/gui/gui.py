from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty

WIDTH = 480
HEIGHT = 320


Window.size = (WIDTH, HEIGHT)
# Window.fullscreen = True


class TeaApp(App):
    temperature = StringProperty("TEMP")

    def motorUp(self, _button):
        self.temperature = "SO NICE"

    def motorDown(self, _button):
        self.temperature = "SO NOT NICE"

    def setTemperature(self, temperature):
        self.temperature = str(temperature)


if __name__ == "__main__":
    app = TeaApp()
    app.run()
