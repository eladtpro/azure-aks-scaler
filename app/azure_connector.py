import json
import os
from azure.mgmt.containerservice import ContainerServiceClient
from azure.identity import ManagedIdentityCredential, DefaultAzureCredential

from cloud_connectors import _CloudConnector
from config import AzureConfig
from pool import Pool, PoolEncoder


class _AzureConnector(_CloudConnector):
    def __init__(self) -> None:
        super().__init__()
        self._aks_client: ContainerServiceClient = self.__connect_to_cluster()

    @staticmethod
    def __connect_to_cluster():
        if "KUBERNETES_SERVICE_HOST" in os.environ:
            # Running in AKS container
            creds = ContainerServiceClient(
            ManagedIdentityCredential(client_id=AzureConfig.AZURE_CLIENT_ID), AzureConfig.SUBSCRIPTION_ID)
        else:
            # Running locally
            creds = ContainerServiceClient(
            DefaultAzureCredential(), AzureConfig.SUBSCRIPTION_ID
        )


        return creds
    
    def list_node_pools(self):
        pools = []
        node_pools = self._aks_client.agent_pools.list(AzureConfig.RESOURCE_GROUP, AzureConfig.CLUSTER_NAME)
        for aks_pool in node_pools:
            pool = Pool(aks_pool.name, aks_pool.count, aks_pool.mode, aks_pool.type, aks_pool.os_type, aks_pool.vm_size)
            pools.append(pool)
            print(pool)

        return json.dumps(pools, cls=PoolEncoder)

    def scale_node_pools(self, node_pools_amount: dict = AzureConfig.NODE_POOLS_AMOUNT):
        for node_name, count in node_pools_amount.items():
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
        return node_pools_amount
