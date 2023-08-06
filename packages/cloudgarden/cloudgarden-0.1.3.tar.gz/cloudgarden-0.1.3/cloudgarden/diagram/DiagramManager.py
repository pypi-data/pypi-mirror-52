from typing import List
from ..aws.AwsManager import AwsManager
from ..aws.AwsResource import AwsResource
from .DiagramCellList import DiagramCellList
from .DiagramLink import DiagramLink


class DiagramManager:

	def __init__(self, aws_manager: AwsManager):
		self.__aws_manager = aws_manager


	def get_cells(self) -> DiagramCellList:
		return DiagramCellList(
			self.__get_elements(),
			self.__get_links()
		)


	def __get_elements(self) -> List[AwsResource]:
		aws = self.__aws_manager

		stacks = aws.get_stacks()
		resources = [
			*aws.get_lambdas(),
			*aws.get_dynamo_db(),
			*aws.get_sns(),
			*aws.get_sqs()
		]

		for stack in stacks:
			for resource in stack.children:
				if resource in resources:
					resources.remove(resource)

		return [
			*stacks,
			*resources
		]


	def __get_links(self) -> List[DiagramLink]:
		aws = self.__aws_manager
		links = []

		for subscription in aws.get_sns_subscriptions():
			source = aws.get_resource_by_arn(subscription.data['TopicArn'])
			target = aws.get_resource_by_arn(subscription.data['Endpoint'])

			if source and target:
				link = DiagramLink(source, target)
				links.append(link)

		return links