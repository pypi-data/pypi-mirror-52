from __future__ import annotations
from ..AwsResource import AwsResource


class DynamoDb(AwsResource):

	TYPE = 'AWS::DynamoDB::Table'

	def get_stack_member_id(self) -> str:
		return self.get_name()