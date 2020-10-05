class private(object):
    def __init__(self, *args, **kwargs):
        self._privates = args

    def __call__(self, f):
        p = self

        class Inner(f):
            def __init__(self, *args, **kwargs):
                object.__setattr__(self, "_obj", f(*args, **kwargs))

            def __getattribute__(self, item):
                _privates = object.__getattribute__(p, "_privates")
                _obj = object.__getattribute__(self, "_obj")
                # print(_obj.__dict__)
                # print(_obj.__class__.__dict__)
                if item not in _privates:
                    try:
                        return object.__getattribute__(_obj, item)
                    except AttributeError:
                        pass
                    return type.__getattribute__(_obj.__class__, item)
                else:
                    raise TypeError("Pobranie atrybutu prywatnego: {}".format(item))

            def __setattr__(self, key, value):
                global _obj
                _privates = object.__getattribute__(p, "_privates")
                _obj = object.__getattribute__(self, "_obj")
                if key not in _privates:
                    object.__setattr__(_obj, key, value)
                else:
                    raise TypeError("Modyfikacja atrybutu prywatnego: {}".format(key))
        return Inner
