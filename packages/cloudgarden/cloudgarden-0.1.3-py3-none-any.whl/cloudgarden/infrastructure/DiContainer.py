from __future__ import annotations
import inspect


class DiContainer:

	def __init__(self):
		self.__services = {}


	def get(self, cls: type, **kwargs):
		service_key = cls.__qualname__

		if service_key in self.__services:
			return self.__services[service_key]

		signature = inspect.signature(cls.__init__)
		inject = {}

		for key, param in signature.parameters.items():
			if param.name in ('self', 'args', 'kwargs'):
				continue

			if param.name in kwargs:
				inject[param.name] = kwargs[param.name]
				continue

			if param.default != inspect.Parameter.empty:
				continue

			#
			# maybe try https://docs.scipy.org/doc/numpy/reference/generated/numpy.isscalar.html
			#

			inject[param.name] = self.get(param.annotation)

			# raise ValueError(f'Unable to create instance of {param.annotation}')

		instance = cls(**inject)
		self.__services[service_key] = instance
		return instance
