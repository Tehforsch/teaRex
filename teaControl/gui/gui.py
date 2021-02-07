from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.clock import Clock

from teaControl.config import UPDATE_INTERVAL

WIDTH = 480
HEIGHT = 320


Window.size = (WIDTH, HEIGHT)
Window.fullscreen = True
Window.show_cursor = False

class Gui:
    def __init__(self, machine):
        self.app = Gui.TeaApp()
        self.machine = machine
        event = Clock.schedule_interval(self.update_machine, UPDATE_INTERVAL)


        self.app.run()

    class TeaApp(App):
        temperature = StringProperty("TEMP")

        def motorUp(self, _button):
            self.temperature = "SO NICE"

        def motorDown(self, _button):
            self.temperature = "SO NOT NICE"

        def setTemperature(self, temperature):
            self.temperature = str(temperature)

    def update_machine(self, machine):
        inputs = self.machine.getSensorValues()
        self.app.setTemperature("{} °C".format(round(inputs.temp)))
