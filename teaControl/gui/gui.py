from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.clock import Clock

from teaControl.config import UPDATE_INTERVAL
from teaControl.machineDefinition import Outputs, Motor, Plate

WIDTH = 480
HEIGHT = 320


Window.size = (WIDTH, HEIGHT)
Window.fullscreen = True
Window.show_cursor = False

class Gui:
    def __init__(self, machine):
        self.app = Gui.TeaApp()
        self.app.machine = machine
        self.machine = machine
        event = Clock.schedule_interval(self.update_machine, UPDATE_INTERVAL)


        self.app.run()

    class TeaApp(App):
        temperature = StringProperty("TEMP")

        def motorUp(self, _button):
            outputs = Outputs(Motor.Up, Plate.Off)
            self.machine.controlDevices(outputs, force=True)

        def motorDown(self, _button):
            outputs = Outputs(Motor.Down, Plate.Off)
            self.machine.controlDevices(outputs, force=True)

        def setTemperature(self, temperature):
            self.temperature = str(temperature)

    def update_machine(self, machine):
        inputs = self.machine.getSensorValues()
        self.app.setTemperature("{} °C".format(round(inputs.temp)))
