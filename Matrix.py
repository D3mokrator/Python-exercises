class Matrix:
    def __init__(self, size, values):
        self.size = size
        self.values = []
        for x in range(size):
            self.values.append([0]*size)
        if values is not None:
            for x in range(size):
                for y in range(size):
                    self.values[x][y] = values[x][y]

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, item):
        self.values[key] = item

    def __add__(self, other):
        size = self.size
        result = Matrix(size, self.values)
        for x in range(size):
            for y in range(size):
                result.values[x][y] += other.values[x][y]
        return result

    def __mul__(self, other):
        size = self.size
        if isinstance(other, Matrix):
            result = Matrix(size, None)
            for x in range(size):
                for y in range(size):
                    for k in range(size):
                        result.values[x][y] += self.values[x][k]*other.values[k][y]
            return result
        else:
            result = Matrix(size, self.values)
            for x in range(size):
                for y in range(size):
                    result.values[x][y] *= other
            return result

    def __mod__(self, other):
        size = self.size
        result = Matrix(size, self.values)
        for x in range(size):
            for y in range(size):
                result.values[x][y] = result.values[x][y] % other
        return result

    def __pow__(self, other):
        size = self.size
        if other == 0:
            result = Matrix(size, None)
            for x in range(size):
                result.values[x][x] = 1
            return result
        elif (other % 2) == 1:
            return self*((self**((other-1)//2))*(self**((other-1)//2)))
        else:
            return (self**(other//2))*(self**(other//2))

    def __iter__(self):
        for x in range(self.size):
            for y in range(self.size):
                yield self.values[x][y]
    
    def __str__(self):
        size = self.size
        s = str(size)
        lines = [" ".join([str(y) for y in x]) for x in self.values]
        return s + "\n" + "\n".join(lines)

