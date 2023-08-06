from marshmallow import Schema, fields


class CellSchema(Schema):
	id = fields.Function(lambda obj: obj.get_id())
	name = fields.Function(lambda obj: obj.get_name())
	children = fields.Nested('self', many=True)

	class Meta:
		additional = ('arn',)