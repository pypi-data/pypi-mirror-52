from __future__ import annotations
from ..AwsResource import AwsResource


class Sqs(AwsResource):

	TYPE = 'AWS::SQS::Queue'

	def get_stack_member_id(self) -> str:
		return self.data.url.replace('https://', 'https://sqs.').replace('queue.', '')