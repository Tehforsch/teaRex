from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config

from teaControl.config import UPDATE_INTERVAL
from teaControl.machineDefinition import Outputs, Motor, Plate

import os

os.environ['KIVY_WINDOW'] = 'egl_rpi'


WIDTH = 480
HEIGHT = 320

Window.size = (WIDTH, HEIGHT)
Window.fullscreen = True
Window.show_cursor = False

class WrongDisplaySettingException(BaseException):
    def __init__(self, text):
        self.text = text

def ensureProperKivySettings():
    """We need to comment out the '%(name)s = probesysfs' line in ~/.kivy/config.ini and
    it's not possible to use a local setting for this for some reason (https://github.com/kivy/kivy/issues/5697).
    This function makes sure this setting isnt on"""
    if "%(name)s" in Config["input"]:
        raise WrongDisplaySettingException("Comment out the %(name)s = probesysfs,provider=hidinput line in ~/.kivy/config.ini")

ensureProperKivySettings()

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
            print("hi")
            self.temperature = "ROFL"
            # outputs = Outputs(Motor.Up, Plate.Off)
            # self.machine.controlDevices(outputs, force=True)

        def motorDown(self, _button):
            print("ho")
            self.temperature = "POFL"
            # outputs = Outputs(Motor.Down, Plate.Off)
            # self.machine.controlDevices(outputs, force=True)

        def setTemperature(self, temperature):
            self.temperature = str(temperature)

    def on_mouse_pos(self, pos):
        print(pos)

    def update_machine(self, machine):
        inputs = self.machine.getSensorValues()
        self.app.setTemperature("{} °C".format(round(inputs.temp)))

