import time
from typing import Callable, Tuple, List
from teaControl.machineDefinition import Inputs, Outputs

State = Callable[[Inputs, float], Tuple[Outputs, str]]


class StateMachine:
    def __init__(self, states: List[State]) -> None:
        self.states = states
        self.currentState = states[0]
        self.stateStartTime = time.time()

    def update(self, inputs: Inputs) -> Outputs:
        stateTime = time.time() - self.stateStartTime
        outputs, newStateName = self.currentState(inputs, stateTime)
        if self.currentState.__name__ != newStateName:
            self.changeState(self.findState(newStateName))
        return outputs

    def findState(self, stateName: str) -> State:
        return next(state for state in self.states if state.__name__ == stateName)

    def changeState(self, state: State) -> None:
        self.currentState = state
        self.stateTime = time.time()
