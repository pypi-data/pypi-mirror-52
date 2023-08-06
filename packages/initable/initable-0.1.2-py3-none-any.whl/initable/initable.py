import inspect

from ._vendor import funcutils


class InitializableWrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __get__(self, instance, owner):
        if instance is None:
            instance = owner  # return caller's class

        return self.wrapped.__get__(instance, owner)


def get_class_defining_method(method):
    if inspect.ismethod(method):
        for cls in inspect.getmro(method.__self__.__class__):
            if cls.__dict__.get(method.__name__) is method:
                return cls
        method = method.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(method):
        cls = getattr(
            inspect.getmodule(method),
            method.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0]
        )
        if isinstance(cls, type):
            return cls
    # handle special descriptor objects
    return getattr(method, '__objclass__', None)


def initializable(func, *args, **kwargs):
    @InitializableWrapper
    @funcutils.wraps(func)
    def wrapper(caller, *args, **kwargs):
        class_defining_wrapped = get_class_defining_method(func)

        if class_defining_wrapped is not None \
                and not isinstance(caller, class_defining_wrapped):
            # create instance of method's defining class
            caller = class_defining_wrapped()
        caller.func(*args, **kwargs)

        return caller

    return wrapper
