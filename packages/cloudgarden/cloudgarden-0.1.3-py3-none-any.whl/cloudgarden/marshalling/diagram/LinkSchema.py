from marshmallow import Schema, fields
from .CellSchema import CellSchema


class LinkSchema(Schema):
	element_schema = CellSchema(only=('id', 'arn'))

	source = fields.Nested(element_schema)
	target = fields.Nested(element_schema)