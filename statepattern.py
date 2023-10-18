from __future__ import annotations #This line is not needed when python 4.0 is out
from enum import Enum, unique, auto, IntEnum
from abc import ABC, abstractmethod



class StateId(Enum):
    START = 0
    GET_ACC_INFO = auto()
    ENTRY = auto()
    EXIT = auto()

class StateMap():
    StateTransitionMap = {}
    StateTransitionMap[StateId.START] = [StateId.GET_ACC_INFO]
    StateTransitionMap[StateId.GET_ACC_INFO] = [StateId.ENTRY, StateId.EXIT]
    StateTransitionMap[StateId.ENTRY] = [StateId.EXIT]
    StateTransitionMap[StateId.EXIT] = [StateId.ENTRY]

    @classmethod
    def allowChange(cls, currentState: AbstractState, nextState: AbstractState) -> bool:
        if  nextState.id in cls.StateTransitionMap[currentState.id]:
            print(f"Changing state from {currentState.id} to {nextState.id}")
            return True
        else:
            print(f"Not Allow changing state {currentState.id} to {nextState.id}")
            return False

class Context:
    current_state: None
    def __init__(self) -> None:
        self.current_state = StartState()
    
    def changeState(self, state) -> None:
        if StateMap.allowChange(self.current_state, state):
            self.current_state.onExitState()
            state.context = self
            self.current_state = state
            self.current_state.onEnterState()
    
    def action(self):
        self.current_state.action()

class AbstractState(ABC):
    @property
    def id(self) -> StateId:
        return self._id

    @id.setter
    def id(self, id: StateId) -> None:
        self._id = id

    @property
    def executeActionOnStateChange(self) -> bool:
        return self._executeActionOnStateChange

    @executeActionOnStateChange.setter
    def id(self, executeActionOnStateChange: bool) -> None:
        self._executeActionOnStateChange = executeActionOnStateChange

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def action(self) -> None:
        pass
    
    #To be overrided if nesscessary 
    def onExitState(self) -> None:
        pass
    
    #To be overrided if nesscessary 
    def onEnterState(self) -> None:
        pass

class StartState(AbstractState):
    def __init__(self) -> None:
        self.id = StateId.START
    
    def action(self) -> None:
        pass

class UpdateAccountInfoState(AbstractState):
    def __init__(self) -> None:
        self.id = StateId.GET_ACC_INFO
    
    def action(self) -> None:
        pass

if __name__ == '__main__':
    context = Context()
    context.changeState(StartState())
    context.changeState(UpdateAccountInfoState())