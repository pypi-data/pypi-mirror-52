from abc import *
from concurrent.futures import Future as Future1
from asyncio import (Future as Future2, 
                    get_event_loop,
                    iscoroutine)
class Thenable(metaclass=ABCMeta):
    @abstractmethod
    def then(self, resolve=None, reject=None):
        pass
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Thenable:
            if any("then" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented

def promisify(x, loop=get_event_loop()):
    from promise import Promise
    if isinstance(x, Promise):
        return x
    if iscoroutine(x):
        x = loop.create_task(x) 
    if isinstance(x, (Future1, Future2)):
        if x.done():
            p = Promise().set_value(x.result())
        else:
            p = Promise()
            def then(onResolve=None, onReject=None):
                if not onResolve:
                    onResolve = lambda v:v
                if not onReject:
                    onReject = lambda r:r
                def callback(future):
                    if future._result:
                        onResolve(future._result)
                    elif future._exception:
                        onReject(future._exception)
                x.add_done_callback(callback)
            p.then = then
        p._task = [x]
        return p
    else:
        return x

