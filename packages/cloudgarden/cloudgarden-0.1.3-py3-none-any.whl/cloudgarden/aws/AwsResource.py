from __future__ import annotations
from abc import ABC
from hashlib import sha1


class AwsResource(ABC):

	def __init__(self, arn: str, data: dict = None):
		self.arn = arn
		self.data = data


	def get_id(self) -> str:
		return sha1(self.arn.encode('utf-8')).hexdigest()


	def get_name(self) -> str:
		chunks = self.arn.split(':')
		chunks = chunks[-1].split('/')
		return chunks[-1]


	def get_stack_member_id(self) -> str:
		return self.arn


