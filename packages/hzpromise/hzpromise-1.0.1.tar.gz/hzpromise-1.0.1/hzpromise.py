from asyncio.coroutines import iscoroutinefunction
from asyncio import get_event_loop
from thenable import *
from threading import Lock
PENDING = "PENDING"
REJECTED = "REJECTED"
FULFILLED = "FULFILLED"

# TODO: add lock to supply threadsafe  √ 

class Promise:
    def __init__(self, executor=None):
        self._state = PENDING
        self.value = None
        self.reason = None
        self._onFulfilledCallbacks = []
        self._onRejectedCallbacks = []
        self._lock = Lock()
        self._task = []
        if executor:
            try:
                if iscoroutinefunction(executor):
                    loop = get_event_loop()
                    coro = executor(self.set_value, self.set_reason)
                    self._task.append(loop.create_task(coro))
                else:
                    executor(self.set_value, self.set_reason)
            except Exception as e:
                self.set_reason(e)
    def set_value(self, value):
        with self._lock:
            assert self._state == PENDING
            self.value = value
            self._state = FULFILLED
            for callback in self._onFulfilledCallbacks:
                callback(value)
    def set_reason(self, reason):
        with self._lock:
            assert self._state == PENDING
            assert isinstance(reason, BaseException)
            self.reason = reason
            self._state = REJECTED
            for callback in self._onRejectedCallbacks:
                callback(reason)
    def resolve(self, x):
        if isinstance(x,  Promise):
            assert x is not self
            if x._state == PENDING:
                x.then(self.resolve, self.set_reason)
            else:
                try:
                    if x.reason:
                        self.set_reason(x.reason)
                    else:
                        self.set_result(x.value)
                except Exception as e:
                    self.set_result(e)
        else:
            x = promisify(x)
            if isinstance(x, Thenable):
                try:
                    x.then(self.resolve, self.set_reason)
                    self._task.extend(x._task)
                except Exception as e:
                    self.set_reason(e)
            else:
                try:
                    self.set_value(x)
                except Exception as e:
                    self.set_reason(e)
    def then(self, onFulfilled=None, onRejected=None):
        if onFulfilled == None:
            onFulfilled = lambda v:v
        if onRejected == None:
            onRejected = lambda r:r
        new_Promise = None
        def executor(resolve, reject):
            if self._state == FULFILLED:
                try:
                    x = onFulfilled(self.value)
                    new_Promise.resolve(x)
                except Exception as e:
                    reject(e)
            if self._state == REJECTED:
                try:
                    x = onRejected(self.reason)
                    new_Promise.resolve(x)
                except Exception as e:
                    reject(e)
            if self._state == PENDING:
                def _resolve(value):
                    try:
                        x = onFulfilled(value)
                        new_Promise.resolve(x)
                    except Exception as e:
                        reject(e)
                def _reject(reason):
                    try:
                        x = onRejected(value)
                        new_Promise.resolve(x)
                    except Exception as e:
                        reject(e)
                self._onFulfilledCallbacks.append(_resolve)
                self._onRejectedCallbacks.append(_reject)
        new_Promise = Promise(executor)
        return new_Promise
    @staticmethod
    def race(promises):
        '''just like first_complete, return a promise which will fulfilled when the first of the given promises is fulfilled or rejected
        '''
        def raises(reason):
            raise reason
        def executor(resolve, reject):
            for promise in promises:
                promise.then(lambda v:resolve(v), reject)
        return Promise(executor)
    @staticmethod
    def all(promises):
        '''just like wait, return a promise which will fulfilled when allthe promises if fulfilled or at least one is rejected, the err then set to the new promise
        '''
        def gen(resolve):
            values = []
            def save(value):
                values.append(value)
                if len(values) == len(promises):
                    resolve(values)
            return save
        def executor(resolve, reject):
            done = gen(resolve)
            for promise in promises:
                promise.then(done, reject)
        return Promise(executor) 






