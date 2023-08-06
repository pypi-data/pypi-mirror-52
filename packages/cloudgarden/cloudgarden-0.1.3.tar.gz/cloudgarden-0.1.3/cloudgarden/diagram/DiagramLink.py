from ..aws.AwsResource import AwsResource


class DiagramLink:

	def __init__(self, source: AwsResource, target: AwsResource):
		self.source = source
		self.target = target