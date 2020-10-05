from functools import partial

class MRO:
    def __init__(self, obj):
        self.obj = obj

    @staticmethod
    def get_tree(cls):
        l = [cls]
        for x in l:
            for i in range(len(x.__bases__)):
                t = x.__bases__[-1*i-1]
                if t != object and t not in l:
                    l.append(t)
        return l

    def __getattribute__(self, item):
        obj = object.__getattribute__(self, "obj")
        cls = obj.__class__
        if item in obj.__dict__:
            return obj.__dict__[item]

        l = MRO.get_tree(cls)
        for x in l:
            if item in x.__dict__:
                f = x.__dict__[item]
                if callable(f):
                    return partial(f, obj)
                else:
                    return f
        object.__getattribute__(obj, item)