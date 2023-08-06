from .infrastructure.DiContainer import DiContainer
from .marshalling.Marshaller import Marshaller
from .marshalling.diagram.CellListSchema import CellListSchema
from .diagram.DiagramManager import DiagramManager


class Garden:

	def __init__(self):
		self.__container = DiContainer()


	@Marshaller.marshal_with(CellListSchema)
	def get_diagram(self) -> dict:
		diagram = self.__container.get(DiagramManager)
		return diagram.get_cells()