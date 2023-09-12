# Azure AKS Scaler

![AKS Scaling](assets/featured.aks-lab-logo.png)

## Setting Workload Identity

> [Tutorial: Use a workload identity with an application on Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/learn/tutorial-kubernetes-workload-identity)

### Create an OpenID Connect provider on Azure Kubernetes Service (AKS)
> [Create an OpenID Connect provider on Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/use-oidc-issuer)

1. Update an AKS cluster with OIDC Issuer <br>
`az aks update -g myResourceGroup -n myAKSCluster --enable-oidc-issuer`

2. Show the OIDC Issuer URL <br>
`az aks show -n myAKScluster -g myResourceGroup --query "oidcIssuerProfile.issuerUrl" -otsv`

3. Get the OIDC Issuer URL and save it to an environmental variable <br>
`export AKS_OIDC_ISSUER="$(az aks show -n myAKSCluster -g "${RESOURCE_GROUP}" --query "oidcIssuerProfile.issuerUrl" -otsv)"`


### Export environmental variables

`export RESOURCE_GROUP="myResourceGroup" \`  <br>
`export LOCATION="westcentralus" \` <br>
`export CLUSTER_NAME="myManagedCluster" \` <br>
`export SERVICE_ACCOUNT_NAMESPACE="default" \` <br>
`export SERVICE_ACCOUNT_NAME="workload-identity-sa" \` <br>
`export SUBSCRIPTION="$(az account show --query id --output tsv)" \` <br>
`export USER_ASSIGNED_IDENTITY_NAME="userIdentity" \` <br>
`export FEDERATED_IDENTITY_CREDENTIAL_NAME="scalerFedIdentity"`


### Create a managed identity and grant permissions to access AKS api-controller
> [Assign a managed identity access to a resource using Azure CLI](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/howto-assign-access-cli)
> [Use a managed identity in Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/use-managed-identity)

1. Create a managed identity using the [az identity create](https://learn.microsoft.com/en-us/cli/azure/identity#az-identity-create) command. <br>
`az identity create --name "${USER_ASSIGNED_IDENTITY_NAME}" --resource-group "${RESOURCE_GROUP}" --location "${LOCATION}" --subscription "${SUBSCRIPTION}"`

2. Set the CLIENT_ID environment variable <br>
`export USER_ASSIGNED_CLIENT_ID="$(az identity show --resource-group "${RESOURCE_GROUP}" --name "${USER_ASSIGNED_IDENTITY_NAME}" --query 'clientId' -otsv)"`

3. Get credentials to access the cluster using the [az aks get-credentials](https://learn.microsoft.com/en-us/cli/azure/aks#az_aks_get_credentials) command. <br>
`az aks get-credentials --resource-group "${RESOURCE_GROUP}" --name "${CLUSTER_NAME}"`

4. To update your existing AKS cluster that's using a service principal to use a system-assigned managed identity, run the [az aks update](https://learn.microsoft.com/en-us/cli/azure/aks#az_aks_update) command <br>
`az aks update -g myResourceGroup -n myManagedCluster --enable-managed-identity`
