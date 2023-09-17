![AKS Scaling](assets/Azure-Kubernetes-Service.jpg)

<span style="font-family:Papyrus; font-size:3em;">Azure AKS Scaler</span>
## Setting Azure Kubernetes Service (AKS) Workload Identity
> Azure Kubernetes Service (AKS) Workload Identity is a feature that allows Kubernetes pods to authenticate with Azure services using their own identities, instead of using a service principal. This provides a more secure and streamlined way to access Azure resources from within a Kubernetes cluster.  
>
> **Based On**:
> [Tutorial: Use a workload identity with an application on Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/learn/tutorial-kubernetes-workload-identity)
 
### Agenda
&nbsp;&nbsp;&nbsp;&nbsp;[A. Export environmental variables](#first)  
&nbsp;&nbsp;&nbsp;&nbsp;[B. Create an OpenID Connect provider on Azure Kubernetes Service (AKS)](#second)  
&nbsp;&nbsp;&nbsp;&nbsp;[C. Create a managed identity and grant permissions to access AKS control plane](#third)  


---
#### <a name="first"></a>A. Prepare the environment  
> Export environmental variables  

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
> **Further Reading**: [Create an OpenID Connect provider on Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/use-oidc-issuer)

1. Update an AKS cluster with OIDC Issuer:
`az aks update -g myResourceGroup -n myAKSCluster --enable-oidc-issuer`

2. Show the OIDC Issuer URL:
`az aks show -n myAKScluster -g myResourceGroup --query "oidcIssuerProfile.issuerUrl" -otsv`

3. Get the OIDC Issuer URL and save it to an environmental variable:
`export AKS_OIDC_ISSUER="$(az aks show -n myAKSCluster -g "${RESOURCE_GROUP}" --query "oidcIssuerProfile.issuerUrl" -otsv)"`

#### <a name="third"></a>C. Create a managed identity and grant permissions to access AKS control plane
> Azure Kubernetes Service (AKS) needs an identity for accessing Azure resources like load balancers and disks, which can be a [managed identity](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview) or service principal. A system-assigned managed identity is auto-generated and managed by Azure, while a [service principal](https://learn.microsoft.com/en-us/azure/aks/kubernetes-service-principal) must be created manually. Service principals expire and require renewal, making managed identities a simpler choice. Both have the same permission requirements and use certificate-based authentication. Managed identities have 90-day credentials that roll every 45 days. AKS supports both system-assigned and user-assigned managed identities, which are immutable.
> **Further Reading**:
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
 
`az role assignment create --assignee <control-plane-identity-principal-id>  --role "Azure Kubernetes Service Cluster Admin Role" --scope "/subscriptions/"${SUBSCRIPTION}"/resourceGroups/"${RESOURCE_GROUP}"/providers/Microsoft.ContainerService/managedClusters/"${CLUSTER_NAME}"`



---

## Further Reading:
[Use Azure AD workload identity with Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview?tabs=python)  
<span style="font-size:10px;display:inline-block; line-height:1;">Workloads deployed on an Azure Kubernetes Services (AKS) cluster require Azure Active Directory (Azure AD) application credentials or managed identities to access Azure AD protected resources, such as Azure Key Vault and Microsoft Graph. Azure AD workload identity integrates with the capabilities native to Kubernetes to federate with external identity providers.</span>

[What are workload identities?](https://learn.microsoft.com/en-us/azure/active-directory/workload-identities/workload-identities-overview)  
<span style="font-size:10px;display:inline-block; line-height:1;">A workload identity is an identity you assign to a software workload (such as an application, service, script, or container) to authenticate and access other services and resources. The terminology is inconsistent across the industry, but generally a workload identity is something you need for your software entity to authenticate with some system. For example, in order for GitHub Actions to access Azure subscriptions the action needs a workload identity which has access to those subscriptions. A workload identity could also be an AWS service role attached to an EC2 instance with read-only access to an Amazon S3 bucket.
In Microsoft Entra, workload identities are applications, service principals, and managed identities.</span>

[ServiceAccount token volume projection](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#serviceaccount-token-volume-projection)  
<span style="font-size:10px;display:inline-block; line-height:1;">The kubelet can also project a ServiceAccount token into a Pod. You can specify desired properties of the token, such as the audience and the validity duration. These properties are not configurable on the default ServiceAccount token. The token will also become invalid against the API when either the Pod or the ServiceAccount is deleted.</span>

[Tutorial: Use a workload identity with an application on Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/learn/tutorial-kubernetes-workload-identity#create-a-managed-identity-and-grant-permissions-to-access-the-secret)  
<span style="font-size:10px;display:inline-block; line-height:1;">Azure Kubernetes Service (AKS) is a managed Kubernetes service that lets you quickly deploy and manage Kubernetes clusters. In this tutorial, you:
Deploy an AKS cluster using the Azure CLI with OpenID Connect (OIDC) Issuer and managed identity.
Create an Azure Key Vault and secret.
Create an Azure Active Directory (Azure AD) workload identity and Kubernetes service account.
Configure the managed identity for token federation.
Deploy the workload and verify authentication with the workload identity.</span>

[Assign a managed identity access to a resource using Azure CLI](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/howto-assign-access-cli#next-steps)  
<span style="font-size:10px;display:inline-block; line-height:1;">Managed identities for Azure resources is a feature of Azure Active Directory. Each of the [Azure services that support managed identities for Azure resources](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/services-support-managed-identities) are subject to their own timeline. Make sure you review the [availability](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/services-support-managed-identities) status of managed identities for your resource and [known issues](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/known-issues) before you begin.</span>

[Use a managed identity in Azure Kubernetes Service (AKS)](https://learn.microsoft.com/en-us/azure/aks/use-managed-identity)  
<span style="font-size:10px;display:inline-block; line-height:1;">Azure Kubernetes Service (AKS) clusters require an identity to access Azure resources like load balancers and managed disks. This identity can be a managed identity or service principal. A system-assigned managed identity is automatically created when you create an AKS cluster. This identity is managed by the Azure platform and doesn't require you to provision or rotate any secrets. For more information about managed identities in Azure AD, see [Managed identities for Azure resources](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview).</span>