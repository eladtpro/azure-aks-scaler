import json
import os
from azure.mgmt.containerservice import ContainerServiceClient
from azure.identity import ManagedIdentityCredential, DefaultAzureCredential

from config import AzureConfig
from pool import Pool, PoolEncoder


class AzureConnector:
    def __init__(self, managed=True, req_client_id=None) -> None:
        self._aks_client: ContainerServiceClient = self.__connect_to_cluster(managed, req_client_id)

    @staticmethod
    def __connect_to_cluster(managed=True, req_client_id=None):
        if "KUBERNETES_SERVICE_HOST" in os.environ and managed:
            # Running in AKS container
            client_id = req_client_id or AzureConfig.AZURE_MANAGED_CLIENT_ID 
            creds = ContainerServiceClient(
            ManagedIdentityCredential(client_id=client_id), AzureConfig.SUBSCRIPTION_ID)

            print(f'running at managed identity: {AzureConfig.AZURE_MANAGED_CLIENT_ID}')
        else:
            # Running locally
            creds = ContainerServiceClient(
            DefaultAzureCredential(), AzureConfig.SUBSCRIPTION_ID)

            print(f'running at default azure credential: {AzureConfig.SUBSCRIPTION_ID}, client_id: {AzureConfig.AZURE_MANAGED_CLIENT_ID}')
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
