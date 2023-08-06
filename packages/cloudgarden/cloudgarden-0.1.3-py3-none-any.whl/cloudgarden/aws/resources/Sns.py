from __future__ import annotations
from ..AwsResource import AwsResource


class Sns(AwsResource):

	TYPE = 'AWS::SNS::Topic'

	def get_stack_member_id(self) -> str:
		return self.arn