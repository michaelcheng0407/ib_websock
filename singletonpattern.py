from __future__ import annotations #This line is not needed when python 4.0 is out
from enum import Enum, unique, auto, IntEnum
from abc import ABC, abstractmethod
from typing import Set
import threading

class Singleton(ABC):
    _instance:Singleton = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs) -> Singleton:
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    print("a single instance is created")
                    cls._instance = super().__new__(cls)
        return cls._instance

    @abstractmethod
    def __init__(self):
        pass
    
    @classmethod
    def getInstance(cls) -> Singleton:
        if cls._instance:
            return cls._instance
        else:
            cls._instance = cls()
            return cls._instance

class CountClass():

    def __init__(self):
        self.b = 0

    def addCount(self):
        self.b += 1

class A(Singleton, CountClass):
    def __init__(self):
        CountClass.__init__(self)
        print("A init")
    
    @classmethod
    def test(cls):
        print("A Test called")

class B(Singleton):
    def __init__(self):
        print("B init")

    @classmethod
    def test(cls):
        print("B Test called")

if __name__ == '__main__':

    a = A.getInstance()
    a.addCount()
    print(a.b)
    a1 = A.getInstance()
    a1.addCount()
    print(a1.b)
    print(f"Is a same as a1: {a is a1}")
    b = B()
    b1 = A()
