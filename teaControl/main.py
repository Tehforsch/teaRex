from typing import Dict, Any
import sys
import time

from teaControl import teaProgram
from teaControl.machineDefinition import Inputs, Outputs, Motor, Plate
from teaControl.testMachine import TestMachine
from teaControl.hardwareMachine import Machine


def getInputsFromSensors() -> Inputs:
    return Inputs(top=False, bottom=True, back=True, temp=0)


def setOutputs(outputs: Outputs) -> None:
    print(outputs)


def run(settings: Dict[str, Any]) -> None:
    program = teaProgram.getTeaProgram(**settings)
    # machine = TestMachine()
    with Machine() as machine:
        while True:
            inputs = machine.getSensorValues()
            outputs = program.update(inputs)
            machine.controlDevices(outputs)
            print(program.currentState.__name__)
            print(
                "Temp={:.02f}".format(inputs.temp),
                ("Top," if inputs.top else "") + ("Bottom," if inputs.bottom else "") + ("Back," if inputs.back else ""),
                f"Motor={outputs.motor}",
                f"Plate={outputs.plate}",
            )
            time.sleep(0.10)


def testSensors() -> None:
    with Machine() as machine:
        while True:
            inputs = machine.getSensorValues()
            print(inputs)
            time.sleep(1)


def testControls() -> None:
    with Machine() as machine:
        outputs = Outputs(Motor.Halt, Plate.Off)
        while True:
            inp = input("Up/Down/Halt/On/Off:\n")
            if inp == "Up":
                outputs.motor = Motor.Up
            if inp == "Down":
                outputs.motor = Motor.Down
            if inp == "Halt":
                outputs.motor = Motor.Halt
            if inp == "On":
                outputs.plate = Plate.On
            if inp == "Off":
                outputs.plate = Plate.Off
            print(outputs)
            machine.controlDevices(outputs, force=True)


print(sys.argv)
if len(sys.argv) == 2 and sys.argv[1] == "sensors":
    testSensors()
if len(sys.argv) == 2 and sys.argv[1] == "controls":
    testControls()
else:
    settings = {"steepTemperature": 80, "steepTime": 120, "keepWarm": True}
    run(settings)
