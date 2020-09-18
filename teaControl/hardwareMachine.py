import time
from typing import Any, List, Callable
from teaControl.machineDefinition import Inputs, Outputs, Motor, Plate
from teaControl.config import (
    MOTOR_A_PIN,
    MOTOR_B_PIN,
    MOTOR_E_PIN,
    TOUCH_SENSOR_BOTTOM_PIN,
    TOUCH_SENSOR_TOP_PIN,
    TOUCH_SENSOR_BACK_PIN,
    RELAY_PIN,
    PLATE_SWITCH_TIMEOUT,
    ADDRESS,
    REGISTER_AMBIENT_TEMP,
    REGISTER_OBJECT_TEMP,
    REGISTER_OBJECT2_TEMP,
    TIME_BETWEEN_TRIES,
    NUM_VALUES_TO_AVERAGE_OVER,
    MAX_NUM_TRIES,
    MAX_ALLOWED_ERROR,
)

from smbus import SMBus
import RPi.GPIO as GPIO


class InaccuracyError(Exception):
    pass


class Machine:
    def __init__(self) -> None:
        self.currentState = Outputs(Motor.Halt, Plate.Off)
        self.bus = SMBus(1)

    def getSensorValues(self) -> Inputs:
        temp = self.tryRead(self.readObjectTempStable)
        top = self.readPin(TOUCH_SENSOR_TOP_PIN)
        bottom = self.readPin(TOUCH_SENSOR_BOTTOM_PIN)
        back = self.readPin(TOUCH_SENSOR_BACK_PIN)
        return Inputs(top=top, bottom=bottom, back=back, temp=temp)

    def controlDevices(self, controls: Outputs, force: bool = False) -> None:
        print(self.currentState)
        if force or controls.motor != self.currentState.motor:
            print(controls.motor)
            if controls.motor == Motor.Up:
                self.motorUp()
            if controls.motor == Motor.Down:
                self.motorDown()
            if controls.motor == Motor.Halt:
                self.motorHalt()
        if controls.plate != self.currentState.plate:
            self.switchPlateState()
        self.currentState = Outputs(controls.motor, controls.plate)

    def readPin(self, pin: int) -> bool:
        return GPIO.input(pin)

    def motorUp(self) -> None:
        GPIO.output(MOTOR_A_PIN, GPIO.LOW)
        GPIO.output(MOTOR_B_PIN, GPIO.HIGH)
        GPIO.output(MOTOR_E_PIN, GPIO.HIGH)

    def motorDown(self) -> None:
        GPIO.output(MOTOR_A_PIN, GPIO.HIGH)
        GPIO.output(MOTOR_B_PIN, GPIO.LOW)
        GPIO.output(MOTOR_E_PIN, GPIO.HIGH)

    def motorHalt(self) -> None:
        GPIO.output(MOTOR_A_PIN, GPIO.LOW)
        GPIO.output(MOTOR_B_PIN, GPIO.LOW)
        GPIO.output(MOTOR_E_PIN, GPIO.LOW)

    def turnRelayOn(self) -> None:
        GPIO.output(RELAY_PIN, GPIO.HIGH)

    def turnRelayOff(self) -> None:
        GPIO.output(RELAY_PIN, GPIO.LOW)

    def switchPlateState(self) -> None:
        self.turnRelayOn()
        time.sleep(PLATE_SWITCH_TIMEOUT)
        self.turnRelayOff()

    def getAverage(self, values: List[float]) -> float:
        return sum(values) / len(values)

    def read16(self, register: int) -> float:
        return self.bus.read_word_data(ADDRESS, register)

    def readTemp(self, register: int) -> float:
        return self.read16(register) * 0.02 - 273.15

    def readTempStable(self, register: int) -> float:
        values: List[float] = []
        numTries = 0
        while len(values) < NUM_VALUES_TO_AVERAGE_OVER:
            numTries += 1
            try:
                time.sleep(TIME_BETWEEN_TRIES)
                values.append(self.readTemp(register))
            except IOError as err:
                if numTries >= MAX_NUM_TRIES:
                    raise err
                continue
        error = max(values) - min(values)
        if error > MAX_ALLOWED_ERROR:
            raise InaccuracyError("High temperature deviation")
        return self.getAverage(values)

    def readObjectTempStable(self) -> float:
        return self.readTempStable(REGISTER_OBJECT_TEMP)

    def tryRead(self, readFunc: Callable[..., float]) -> float:
        try:
            return readFunc()
        except IOError as err:
            print("IO error")
            raise err
        except InaccuracyError as err:
            print("Inaccuracy error")
            raise err
        return 0

    def __enter__(self) -> None:
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(RELAY_PIN, GPIO.OUT)
        GPIO.setup(MOTOR_A_PIN, GPIO.OUT)
        GPIO.setup(MOTOR_B_PIN, GPIO.OUT)
        GPIO.setup(MOTOR_E_PIN, GPIO.OUT)
        GPIO.setup(TOUCH_SENSOR_TOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(TOUCH_SENSOR_BOTTOM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(TOUCH_SENSOR_BACK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        return self

    def __exit__(self, type: Any, value: Any, traceback: Any) -> Any:
        """Make sure we turn the plate off and clean up GPIO pins whenever we shut down."""
        self.motorHalt()
        if self.currentState.plate == Plate.On:
            self.switchPlateState()
        GPIO.cleanup()
