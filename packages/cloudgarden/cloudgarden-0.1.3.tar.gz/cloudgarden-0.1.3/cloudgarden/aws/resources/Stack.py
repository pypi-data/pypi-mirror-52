from __future__ import annotations
from ..AwsResource import AwsResource


class Stack(AwsResource):

	def __init__(self, arn: str, data: dict = None):
		super().__init__(arn, data)

		self.children = []