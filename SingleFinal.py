class Singleton(type):
	obj = {}

	def __call__(cls, *args, **kwargs):
		_name = cls.__name__
		if _name not in Singleton.obj:
			Singleton.obj[_name] = object.__new__(cls)
			Singleton.obj[_name].__init__(*args, **kwargs)
		return Singleton.obj[_name]


class Final(type):
	def __new__(mcs, name, bases, dict):
		if mcs in [x.__class__ for x in bases]:
			raise TypeError("Cannot inherit from final class")
		return type.__new__(mcs, name, bases, dict)
