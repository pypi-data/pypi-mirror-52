from __future__ import annotations
from ..AwsResource import AwsResource


class Lambda(AwsResource):

	TYPE = 'AWS::Lambda::Function'

	def get_stack_member_id(self) -> str:
		return self.get_name()