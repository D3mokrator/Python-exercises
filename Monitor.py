class monit:
    book = []
    inst = 0
    internal = {}
    lev = {}

    def __init__(self, level):
        self.level = level

    def __call__(self, f):
        p = self
        if f not in monit.internal:
            monit.lev[f] = p.level

            def inner(*args):
                depth = monit.inst
                monit.inst = depth+1
                layers = monit.book
                while len(layers)-1 < depth + 1:
                    layers.append([])
                if len(layers[depth]) > 0:
                    layers[depth][-1][5] = len(layers[depth+1])-1
                if depth > 0 and layers[depth-1][-1][4] is None:
                    layers[depth-1][-1][4] = len(layers[depth])

                layers[depth].append([None, None, None, f, None, None])
                entry = layers[depth][-1]
                res = f(*args)
                entry[0], entry[1], entry[2] = res, monit.inst, args
                monit.inst = depth
                return res

            monit.internal[f] = inner
            return inner
        else:
            return monit.internal[f]


def report(level, indent="->", limits=None):
    def prnt(entry, depth):
        if monit.lev[entry[3]] > level:
            return
        begin, end = 1, None
        if limits is not None and monit.internal[entry[3]] in limits:
            begin, end = limits[monit.internal[entry[3]]]
        if end is None:
            end = len(layers)
        if begin <= depth+1 <= end:
            print("{}{}({})".format(indent*depth, entry[3].__name__, ",".join(map(str,entry[2]))))
        if depth+1 <= end and entry[4] is not None:
            if entry[5] is None:
                entry[5] = len(layers[depth+1])-1
            for i in range(entry[4], entry[5]+1):
                prnt(layers[depth+1][i], depth+1)
        if begin <= depth+1 <= end:
            print("{}return {}".format(indent*depth, entry[0]))

    layers = monit.book
    if len(layers) > 0:
        for x in layers[0]:
            prnt(x, 0)


def clear():
    monit.book.clear()
