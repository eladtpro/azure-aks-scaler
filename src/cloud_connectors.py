from abc import ABC, abstractmethod


class _CloudConnector(ABC):
    @abstractmethod
    def scale_node_pool_to_zero(self):
        pass

    @abstractmethod
    def scale_node_pool_up(self):
        pass