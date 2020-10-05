class CallCounter(type):
    register = {}
    functions = {}

    @staticmethod
    def count_decorate(f, names):
        def g(*args, **kwargs):
            CallCounter.register[names] = CallCounter.register[names]+1
            g.calls = CallCounter.register[names]
            return f(*args, **kwargs)
        CallCounter.functions[names] = g
        return g

    def __new__(mcs, name, bases, local):
        for attr in local:
            value = local[attr]
            if callable(value):
                f_names = (name, attr)
                value.calls = 0
                CallCounter.register[f_names] = value.calls
                local[attr] = CallCounter.count_decorate(value, f_names)

        def clear(*args):
            for attr in local:
                value = local[attr]
                if callable(value):
                    f_names = (name, attr)
                    value.calls = 0
                    CallCounter.register[f_names] = 0

        cls = type.__new__(mcs, name, bases, local)
        cls.clear = clear
        return cls

    @staticmethod
    def ranking(number):
        if number <= 0:
            return
        rank = sorted(CallCounter.register.items(), key=lambda kv: (-kv[1], kv[0][0], kv[0][1]))
        rank = [x for x in rank if x[1] > 0]
        if len(rank) < number:
            raise Exception("Too few methods have been called!")
        for x in rank[:number]:
            print("{}() --> {}".format(".".join(x[0]), x[1]))

    @staticmethod
    def ideal():
        rank = sorted(CallCounter.register.items(), key=lambda kv: (-kv[1], kv[0][0], kv[0][1]))
        rank = [x for x in rank if x[1] > 0]
        if len(rank) < 3:
            raise Exception("Too few methods have been called!")
        func = dict([("_".join(x[0]), CallCounter.functions[x[0]]) for x in rank[:3]])
        cls = type.__new__(CallCounter, "Ideal", (), func)
        return cls
