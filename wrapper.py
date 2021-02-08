"""
Proxy class library

This is a proxy library with basically 1 purpose:
Create proxy objects that have a UUID, so created and managed classes can be easily printed and managed,
especially for builtins
"""

import functools
import uuid

from typing import *

def wrap_class(type: type) -> type:
    class NewClass:
        type=type

        def __init__(self, *args, **kwargs):
            self.instance = type(*args, **kwargs)
            self.id = uuid.uuid4()

        def __repr__(self) -> str:
            return f"[Wrap({type}): {repr(self.instance)} @{self.id}]"

        def __str__(self)  -> str:
            return f"[wrap]{self.instance}"
        
        def __getattribute__(self, name: str) -> Any:
            # Lookup any instance or type variable
            if name in ["id", "instance"]:
                return object.__getattribute__(self, name)
            elif name in ["__repr__", "__str__"]:
                return functools.partial(
                    object.__getattribute__(self, name),
                    self
                )
            elif name == "type": return type
            else:
                return type.__getattribute__(self.instance, name)
    
    NewClass.__name__ = "Wrap_" + type.__name__
    return NewClass

            

if __name__ == "__main__":
    class Test:
        def __init__(self, foo):
            self.foo = foo
        def __repr__(self):
            return f"Test(foo={self.foo})"
        
        def double(self):
            return self.foo * 2

    print("Test: ",Test(1))
    WTest = wrap_class(Test)
    print ("WTest class: ", WTest)
    print("WTest Instance: ", WTest(1))
    print ("WTest internals:", repr(WTest(1)))
    print ("WTest Method Call double=", WTest(2).double())


    WList = wrap_class(list)
    print(
        "Wlist class: ", WList,
        "\nWlist Instance: ", WList(),
        "\nWList Internals: ", repr(WList())
    )