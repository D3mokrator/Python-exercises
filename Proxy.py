from functools import partial

class Proxy:
    @staticmethod
    def get_tree(cls):
        l = [cls]
        for x in l:
            for t in x.__bases__:
                if t != object and t not in l:
                    l.append(t)
        return l

    def __init__(self, obj):
        object.__setattr__(self, "obj", obj)

    def __getattribute__(self, item):
        item = item.lower()
        obj = object.__getattribute__(self, "obj")
        if item == "obj":
            return obj
        for o in obj.__dict__:
            if item == o.lower():
                return obj.__dict__[o]
        for t in Proxy.get_tree(obj.__class__):
            for o in t.__dict__:
                if item == o.lower():
                    f = t.__dict__[o]
                    if callable(f):
                        return partial(f, self)
                    else:
                        return f
        return 42

    def __setattr__(self, name, value):
        item = name.lower()
        obj = object.__getattribute__(self, "obj")
        for o in obj.__dict__:
            if item == o.lower():
                obj.__dict__[o] = value
                return
        for t in Proxy.get_tree(obj.__class__):
            for o in t.__dict__:
                if item == o.lower():
                    obj.__dict__[o] = value
                    return
        obj.__dict__[item] = value
