from abc import ABC, abstractmethod
from config import AzureConfig


class _CloudConnector(ABC):
    @abstractmethod
    def scale_node_pools(self, node_pools_amount: dict = AzureConfig.NODE_POOLS_AMOUNT):
        pass