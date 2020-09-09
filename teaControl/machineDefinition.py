from enum import Enum, auto
from dataclasses import dataclass


class Motor(Enum):
    Up = auto()
    Down = auto()
    Halt = auto()


class Plate(Enum):
    On = auto()
    Off = auto()


@dataclass
class Inputs:
    top: bool
    bottom: bool
    back: bool
    temp: float


@dataclass
class Outputs:
    motor: Motor
    plate: Plate
