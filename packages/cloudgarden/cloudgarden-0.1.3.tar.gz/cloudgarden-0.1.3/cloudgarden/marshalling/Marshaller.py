from functools import wraps
from marshmallow import Schema


class Marshaller:

	@staticmethod
	def marshal_with(schemaClass: Schema):
		def marshall(func):
			@wraps(func)
			# async def wrapper(*args, **kwargs):
			def wrapper(*args, **kwargs):
				# obj = await func(*args, **kwargs)
				obj = func(*args, **kwargs)
				schema = schemaClass()
				dump = schema.dump(obj)
				return dump

			return wrapper
		return marshall