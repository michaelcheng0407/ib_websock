from __future__ import annotations #This line is not needed when python 4.0 is out
from enum import Enum, unique, auto, IntEnum
from abc import ABC, abstractmethod
from typing import Set

class Subject:
    observers: Set[Observer] = set()
    def attach(self, observer: Observer) -> None:
        self.observers.add(observer)

    def detach(self, observer: Observer) -> None:
        self.observers.discard(observer)     

    def notifyAll(self):
        [obs.onNotify(self) for obs in self.observers]

class Observer(ABC):
    @abstractmethod
    def onNotify(self, subject: Subject) -> None:
        pass

class Obs1(Observer):
    def __init__(self, id: int) -> None:
        self.id = id
    
    def onNotify(self, subject: Subject) -> None:
        print(f"Observer {self.id} is notified")

if __name__ == '__main__':
    subject = Subject()
    obs1 = Obs1(1)
    obs2 = Obs1(2)
    subject.attach(obs1)
    subject.attach(obs2)
    print(subject.observers)
    subject.notifyAll()
    subject.detach(obs1)
    subject.notifyAll()