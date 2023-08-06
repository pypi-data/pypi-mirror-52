from __future__ import annotations
import boto3
from typing import List, Optional, Type
from .AwsResource import AwsResource
from .resources.Lambda import Lambda
from .resources.Sns import Sns
from .resources.Sqs import Sqs
from .resources.DynamoDb import DynamoDb
from .resources.SnsSubscription import SnsSubscription
from .resources.Stack import Stack


class AwsManager:

	def __init__(self):
		self.__cache = {}


	def get_resource_by_arn(self, arn: str) -> Optional[AwsResource]:
		for resource in self.__get_resources():
			if resource.arn == arn:
				return resource


	def get_stacks(self) -> List[Stack]:
		if (self.__cache_has_key(Stack)):
			return self.__cache_get(Stack)

		for item in self.__get_boto3_resources('cloudformation', 'list_stacks'):
			if (item['StackStatus'] == 'DELETE_COMPLETE'):
				continue

			stack = Stack(item['StackId'])

			for resource in self.__get_boto3_resources('cloudformation', 'list_stack_resources', StackName=item['StackName']):
				if resource['ResourceType'] not in [Lambda.TYPE, Sqs.TYPE, DynamoDb.TYPE, Sns.TYPE]:
					continue

				for child in self.__get_simple_resources():
					mmm = child.get_stack_member_id()

					if child.get_stack_member_id() == resource['PhysicalResourceId']:
						stack.children.append(child)

			self.__cache_add(stack)

		return self.__cache_get(Stack)


	def get_lambdas(self) -> List[Lambda]:
		if (self.__cache_has_key(Lambda)):
			return self.__cache_get(Lambda)

		for item in self.__get_boto3_resources('lambda', 'list_functions'):
			resource = Lambda(item['FunctionArn'], item)
			self.__cache_add(resource)

		return self.__cache_get(Lambda)


	def get_sns(self) -> List[Sns]:
		if (self.__cache_has_key(Sns)):
			return self.__cache_get(Sns)

		for item in self.__get_boto3_resources('sns', 'list_topics'):
			resource = Sns(item['TopicArn'], item)
			self.__cache_add(resource)

		return self.__cache_get(Sns)


	def get_dynamo_db(self) -> List[DynamoDb]:
		if (self.__cache_has_key(DynamoDb)):
			return self.__cache_get(DynamoDb)

		client = boto3.resource('dynamodb')
		for item in client.tables.all():
			resource = DynamoDb(item.table_arn, item)
			self.__cache_add(resource)

		return self.__cache_get(DynamoDb)


	def get_sqs(self) -> List[Sqs]:
		if (self.__cache_has_key(Sqs)):
			return self.__cache_get(Sqs)

		client = boto3.resource('sqs')
		for item in client.queues.all():
			resource = Sqs(item.attributes['QueueArn'], item)
			self.__cache_add(resource)

		return self.__cache_get(Sqs)


	def get_sns_subscriptions(self) -> List[SnsSubscription]:
		if (self.__cache_has_key(SnsSubscription)):
			return self.__cache_get(SnsSubscription)

		client = boto3.resource('sns')
		for item in client.subscriptions.all():
			resource = SnsSubscription(item.arn, item.attributes)
			self.__cache_add(resource)

		return self.__cache_get(SnsSubscription)


	def __get_resources(self) -> List[AwsResource]:
		return [
			*self.__get_simple_resources(),
			*self.get_stacks(),
		]


	def __get_simple_resources(self) -> List[AwsResource]:
		return [
			*self.get_lambdas(),
			*self.get_sns(),
			*self.get_dynamo_db(),
			*self.get_sqs(),
			*self.get_sns_subscriptions()
		]


	# def __get_simple_resource_by_name(self, name: str) -> Optional[AwsResource]:
	# 	for resource in self.__get_simple_resources():
	# 		if resource.get_name() == name:
	# 			return resource


	def __cache_has_key(self, cls: type) -> bool:
		key = cls.__qualname__
		return key in self.__cache.keys()


	def __cache_get(self, cls: Type[T]) -> List[T]:
		key = cls.__qualname__
		return self.__cache[key]


	def __cache_add(self, obj: object):
		key = type(obj).__qualname__

		if key not in self.__cache.keys():
			self.__cache[key] = []

		self.__cache[key].append(obj)


	@classmethod
	def __get_boto3_resources(cls, service: str, method: str, **kwargs) -> list:
		client = boto3.client(service)
		paginator = client.get_paginator(method)
		pages = paginator.paginate(**kwargs)

		resources = []

		for page in pages:
			resources.extend(cls.__parse_boto3_response(page))

		return resources


	@staticmethod
	def __parse_boto3_response(response: dict) -> list:
		resources = []

		for key, value in response.items():
			if isinstance(value, list):
				resources.extend(value)

		return resources