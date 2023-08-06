from marshmallow import fields
from .CellSchema import CellSchema


class ElementSchema(CellSchema):
	type = fields.Function(lambda obj: type(obj).__name__)