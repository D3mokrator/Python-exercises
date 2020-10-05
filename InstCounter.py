def inst(wrapped):
    class MetaWrapper(type):
        def __getattr__(cls, item):
            return type.__getattribute__(wrapped, item)

    class ClsWrapper(metaclass=MetaWrapper):
        _counter = 0

        @staticmethod
        def num_of_inst():
            print("Liczba instancji klasy {}: {}".format(wrapped.__name__, ClsWrapper._counter))

        def __init__(self, *args, **kwargs):
            self.instance = wrapped(*args, **kwargs)
            ClsWrapper._counter = ClsWrapper._counter + 1

        def __getattribute__(self, item):
            try:
                x = super(ClsWrapper, self).__getattribute__(item)
            except AttributeError:
                pass
            else:
                return x
            x = self.instance.__getattribute__(item)
            return x

        def __str__(self):
            return self.instance.__str__()

    return ClsWrapper