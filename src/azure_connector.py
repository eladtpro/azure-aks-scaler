# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from azure.mgmt.containerservice import ContainerServiceClient
from azure.identity import DefaultAzureCredential

from cloud_connectors import _CloudConnector
from config import AzureConfig


class _AzureConnector(_CloudConnector):
    def __init__(self) -> None:
        super().__init__()
        self._aks_client: ContainerServiceClient = self._connect_to_cluster()

    @staticmethod
    def _connect_to_cluster():
        return ContainerServiceClient(
            DefaultAzureCredential(), AzureConfig.SUBSCRIPTION_ID
        )

    def scale_node_pool_to_zero(self):
        for node_name in AzureConfig.NODE_POOLS_AMOUNT.keys():
            node_pool = self._aks_client.agent_pools.get(
                AzureConfig.RESOURCE_GROUP, AzureConfig.CLUSTER_NAME, node_name
            )
            node_pool.count = 0
            print(f'scaling node pool {node_name} to {node_pool.count}')
            pool = self._aks_client.agent_pools.begin_create_or_update(
                AzureConfig.RESOURCE_GROUP, 
                AzureConfig.CLUSTER_NAME, 
                node_name, 
                node_pool
            )
            print(pool.result())

    def scale_node_pool_up(self):
        for node_name, count in AzureConfig.NODE_POOLS_AMOUNT.items():
            node_pool = self._aks_client.agent_pools.get(
                AzureConfig.RESOURCE_GROUP,
                AzureConfig.CLUSTER_NAME,
                node_name
            )
            node_pool.count = count
            print(f'scaling node pool {node_name} to {node_pool.count}')
            pool = self._aks_client.agent_pools.begin_create_or_update(
                AzureConfig.RESOURCE_GROUP,
                AzureConfig.CLUSTER_NAME,
                node_name,
                node_pool,
            )
            print(pool.result())
