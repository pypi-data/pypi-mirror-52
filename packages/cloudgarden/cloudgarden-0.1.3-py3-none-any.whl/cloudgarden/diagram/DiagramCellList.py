from typing import List
from ..aws.AwsResource import AwsResource
from .DiagramLink import DiagramLink


class DiagramCellList:

	def __init__(self, elements: List[AwsResource], links: List[DiagramLink]):
		self.elements = elements
		self.links = links