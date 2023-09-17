from azure_connector import _AzureConnector

# Press the green button in the gutter to run the script.
# Press ⌘F8 to toggle the breakpoint.
if __name__ == "__main__":
    connection = _AzureConnector._connect_to_cluster()
    azure_connector: _AzureConnector = _AzureConnector()
    print("scaling up")
    azure_connector.scale_node_pool_up()
    # azure_connector.scale_node_pool_to_zero()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
