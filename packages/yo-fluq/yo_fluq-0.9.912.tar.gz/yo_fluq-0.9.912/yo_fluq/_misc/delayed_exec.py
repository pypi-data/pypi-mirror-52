from typing import TypeVar, Callable, Any

T = TypeVar('T')

def feed_to_fluent_callable(obj, collector: T) -> T:
    field_name = 'exec'
    existing = None
    if hasattr(collector,field_name):
        existing = getattr(collector,field_name)
        if not isinstance(existing,DelayedExecution):
            if existing is not None:
                raise ValueError("Collector instance already has attribute `{0}`, and it's not of type DelayedExecution. Specify another name for the finalizing field".format(field_name))
        else:
            if existing.initialized:
                raise ValueError('Collector was already initialized.')
            existing._initialize(collector,obj)

    if existing is None:
        ex = DelayedExecution()
        ex._initialize(collector,obj)
        setattr(collector,field_name,ex)
    return collector

class DelayedExecution:
    def __init__(self):
        self.call = None
        self.argument = None
        self.initialized = False

    def _initialize(self, call, argument):
        self.call = call
        self.argument = argument
        self.initialized = True

    def _check_initialization(self):
        if not self.initialized:
            raise ValueError('DelayedExecution was not initialized')

    def result(self):
        self._check_initialization()
        return self.call(self.argument)

    def feed(self, next_call: Callable[[Any],T]) -> T:
        self._check_initialization()
        return next_call(self.call(self.argument))

    def feed_to_fluent_callable(self, next_collector: T) -> T:
        self._check_initialization()
        return feed_to_fluent_callable(self.call(self.argument), next_collector)



