from marshmallow import Schema, fields
from .ElementSchema import ElementSchema
from .LinkSchema import LinkSchema


class CellListSchema(Schema):
	elements = fields.Nested(ElementSchema, many=True)
	links = fields.Nested(LinkSchema, many=True)