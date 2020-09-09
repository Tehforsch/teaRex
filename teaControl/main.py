from typing import Dict, Any
import time

from teaControl import teaProgram
from teaControl.machineDefinition import Inputs, Outputs
from teaControl.testMachine import TestMachine
from teaControl.hardwareMachine import Machine


def getInputsFromSensors() -> Inputs:
    return Inputs(top=False, bottom=True, back=True, temp=0)


def setOutputs(outputs: Outputs) -> None:
    print(outputs)


def run(settings: Dict[str, Any]) -> None:
    program = teaProgram.getTeaProgram(**settings)
    machine = TestMachine()
    while True:
        inputs = machine.getSensorValues()
        outputs = program.update(inputs)
        machine.controlDevices(outputs)
        print(program.currentState.__name__)
        print(
            "Temp={:.02f}".format(inputs.temp),
            "Position={:.02f}".format(machine.position),
            ("Top," if inputs.top else "") + ("Bottom," if inputs.bottom else "") + ("Back," if inputs.back else ""),
            f"Motor={outputs.motor}",
            f"Plate={outputs.plate}",
        )
        time.sleep(0.10)


# settings = {"steepTemperature": 80, "steepTime": 120, "keepWarm": True}
# run(settings)
