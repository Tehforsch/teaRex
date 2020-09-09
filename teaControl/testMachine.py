from teaControl.machineDefinition import Inputs, Outputs, Motor, Plate

dt = 0.01
FAKE_MOTOR_SPEED = 1
FAKE_HEATING_RATE = 30
FAKE_COOLING_RATE = 2


class TestMachine:
    def __init__(self) -> None:
        self.position = 1.0
        self.temp = 25.0
        self.back = True

    def getSensorValues(self) -> Inputs:
        top = self.position >= 1.0
        bottom = self.position <= 0.0
        back = self.back
        temp = self.temp

        return Inputs(top=top, bottom=bottom, back=back, temp=temp)

    def controlDevices(self, controls: Outputs) -> None:
        if controls.motor == Motor.Up:
            self.position += dt * FAKE_MOTOR_SPEED
        if controls.motor == Motor.Down:
            self.position -= dt * FAKE_MOTOR_SPEED
        if controls.plate == Plate.On:
            self.temp += dt * FAKE_HEATING_RATE
        if controls.plate == Plate.Off:
            self.temp -= dt * FAKE_COOLING_RATE
