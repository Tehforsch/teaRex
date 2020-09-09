from typing import Optional, Tuple
from teaControl.stateMachine import StateMachine
from teaControl.machineDefinition import Motor, Plate, Outputs, Inputs

# Make code more readable by loading enums into namespace (could update globals() dict but this is more explicit and theres only five anyways)
Up = Motor.Up
Down = Motor.Down
Halt = Motor.Halt
On = Plate.On
Off = Plate.Off


def getTeaProgram(steepTemperature: float, steepTime: float, keepWarm: bool, minDrinkTemp: float = 50, maxDrinkTemp: float = 70) -> StateMachine:
    def setup(inputs: Inputs, stateTime: float) -> Outputs:
        if not inputs.top:
            return Outputs(Up, Off), "setup"
        return Outputs(Halt, Off), "boil"

    def boil(inputs: Inputs, stateTime: float) -> Outputs:
        assert inputs.top
        if inputs.temp < steepTemperature:
            return Outputs(Halt, On), "boil"
        else:
            return Outputs(Halt, Off), "sieveIn"

    def sieveIn(inputs: Inputs, stateTime: float) -> Outputs:
        if not inputs.bottom:
            return Outputs(Down, Off), "sieveIn"
        else:
            return Outputs(Halt, Off), "steep"

    def steep(inputs: Inputs, stateTime: float) -> Outputs:
        assert inputs.bottom
        if stateTime < steepTime:
            return Outputs(Halt, Off), "steep"
        else:
            return Outputs(Halt, Off), "sieveOut"

    def sieveOut(inputs: Inputs, stateTime: float) -> Outputs:
        if not inputs.top:
            return Outputs(Up, Off), "sieveOut"
        else:
            if keepWarm:
                return Outputs(Halt, Off), "waitForCooldown"
            else:
                return Outputs(Halt, Off), "off"

    def off(inputs: Inputs, stateTime: float) -> Outputs:
        return Outputs(Halt, Off), "off"

    def waitForCooldown(inputs: Inputs, stateTime: float) -> Outputs:
        assert inputs.top
        if inputs.temp < minDrinkTemp:
            return Outputs(Halt, Off), "waitForHeatup"
        else:
            return Outputs(Halt, Off), "waitForCooldown"

    def waitForHeatup(inputs: Inputs, stateTime: float) -> Outputs:
        assert inputs.top
        if inputs.temp > maxDrinkTemp:
            return Outputs(Halt, On), "waitForCooldown"
        else:
            return Outputs(Halt, On), "waitForCooldown"

    return StateMachine([setup, boil, sieveIn, steep, sieveOut, off, waitForCooldown, waitForHeatup])
