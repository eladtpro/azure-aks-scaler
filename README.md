![AKS Scaling](assets/Azure-Kubernetes-Service.jpg)

# Azure AKS Scaler

## Setting Azure Kubernetes Service (AKS) Workload Identity
> Azure Kubernetes Service (AKS) Workload Identity is a feature that allows Kubernetes pods to authenticate with Azure services using their own identities, instead of using a service principal. This provides a more secure and streamlined way to access Azure resources from within a Kubernetes cluster.
> Further Reading:
> [Tutorial: Use a workload identity with an application on Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/learn/tutorial-kubernetes-workload-identity)

### Agenda
&nbsp;&nbsp;&nbsp;&nbsp;[A. Export environmental variables](#first)
&nbsp;&nbsp;&nbsp;&nbsp;[B. Create an OpenID Connect provider on Azure Kubernetes Service (AKS)](#second)
&nbsp;&nbsp;&nbsp;&nbsp;[C. Create a managed identity and grant permissions to access AKS control plane](#third)
#### <a name="first"></a>A. Export environmental variables

`export RESOURCE_GROUP="myResourceGroup" \`
`export LOCATION="westcentralus" \`
`export CLUSTER_NAME="myManagedCluster" \`
`export SERVICE_ACCOUNT_NAMESPACE="default" \`
`export SERVICE_ACCOUNT_NAME="workload-identity-sa" \`
`export SUBSCRIPTION="$(az account show --query id --output tsv)" \`
`export USER_ASSIGNED_IDENTITY_NAME="userIdentity" \`
`export FEDERATED_IDENTITY_CREDENTIAL_NAME="scalerFedIdentity"`

#### <a name="second"></a>B. Create an OpenID Connect provider on Azure Kubernetes Service (AKS)
> [OpenID Connect (OIDC)](https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/auth-oidc) extends OAuth 2.0 for authentication via Azure AD. It enables SSO on Azure Kubernetes Service (AKS) using an ID token. AKS can automatically rotate keys or do it manually. Token lifetime is one day.
> This section teaches you how to create, update, and manage the OIDC Issuer for your cluster.
>
> **Warning**: Enabling OIDC Issuer on an existing cluster may cause downtime and API server restarts. If app pods fail, manually restart them.
> 
> **Important**: Once enabled, OIDC cannot be disabled.
> Further Reading: [Create an OpenID Connect provider on Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/use-oidc-issuer)

1. Update an AKS cluster with OIDC Issuer:
`az aks update -g myResourceGroup -n myAKSCluster --enable-oidc-issuer`

2. Show the OIDC Issuer URL:
`az aks show -n myAKScluster -g myResourceGroup --query "oidcIssuerProfile.issuerUrl" -otsv`

3. Get the OIDC Issuer URL and save it to an environmental variable:
`export AKS_OIDC_ISSUER="$(az aks show -n myAKSCluster -g "${RESOURCE_GROUP}" --query "oidcIssuerProfile.issuerUrl" -otsv)"`

#### <a name="third"></a>C. Create a managed identity and grant permissions to access AKS control plane
> Further Reading:
> [Assign a managed identity access to a resource using Azure CLI](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/howto-assign-access-cli)
> [Use a managed identity in Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/use-managed-identity)

1. Create a managed identity using the [az identity create](https://learn.microsoft.com/en-us/cli/azure/identity#az-identity-create) command:
`az identity create --name "${USER_ASSIGNED_IDENTITY_NAME}" --resource-group "${RESOURCE_GROUP}" --location "${LOCATION}" --subscription "${SUBSCRIPTION}"`

2. Set the CLIENT_ID environment variable:
`export USER_ASSIGNED_CLIENT_ID="$(az identity show --resource-group "${RESOURCE_GROUP}" --name "${USER_ASSIGNED_IDENTITY_NAME}" --query 'clientId' -otsv)"`

3. Get credentials to access the cluster using the [az aks get-credentials](https://learn.microsoft.com/en-us/cli/azure/aks#az_aks_get_credentials) command:
`az aks get-credentials --resource-group "${RESOURCE_GROUP}" --name "${CLUSTER_NAME}"`

4. Enable managed identities on an existing AKS cluster 
> To update your existing AKS cluster that's using a service principal to use a system-assigned managed identity, run the [az aks update](https://learn.microsoft.com/en-us/cli/azure/aks#az_aks_update) command

`az aks update -g "${RESOURCE_GROUP}" -n "${CLUSTER_NAME}" --enable-managed-identity`

5. Get the principal ID of managed identity
> Get the existing identity's principal ID using the [az identity show](https://learn.microsoft.com/en-us/cli/azure/identity#az_identity_show) command.

`az identity show --ids /subscriptions/"${SUBSCRIPTION}"/resourceGroups/"${RESOURCE_GROUP}"/providers/Microsoft.ManagedIdentity/userAssignedIdentities/"${USER_ASSIGNED_IDENTITY_NAME}"`


6. Add role assignment
> Assign the Managed Identity Operator role on the kubelet identity using the [az role assignment create](https://learn.microsoft.com/en-us/cli/azure/role/assignment#az_role_assignment_create) command.
> Following the principle of lease priviliges we will try to give less permissions by using custom roles, in this case we will use the builtin roles.
>  
`az role assignment create --assignee <control-plane-identity-principal-id> --role "Azure Kubernetes Service Cluster Admin Role" --scope "<custom-resource-group-resource-id>"`