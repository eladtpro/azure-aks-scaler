from dotenv import load_dotenv
import os
import json

class AzureConfig:
    def __new__(cls):
        # Load environment variables from .env file
        load_dotenv()
        # Print a message indicating that a new object is being created
        print(f'Creating a new {cls.__name__} object...')
        # Create a new object of the current class
        obj = object.__new__(cls)
        # Return the newly created object
        return obj

    @classmethod
    @property
    def SUBSCRIPTION_ID(cls):
        # Get the value of the SUBSCRIPTION_ID environment variable
        return os.getenv("SUBSCRIPTION_ID")

    @classmethod
    @property
    def NODE_POOLS_AMOUNT(cls):
        # Get the value of the NODE_POOLS_AMOUNT environment variable and parse it as JSON
        return json.loads(os.environ['NODE_POOLS_AMOUNT'])

    @classmethod
    @property
    def RESOURCE_GROUP(cls):
        # Get the value of the RESOURCE_GROUP environment variable
        return os.getenv("RESOURCE_GROUP")

    @classmethod
    @property
    def CLUSTER_NAME(cls):
        # Get the value of the CLUSTER_NAME environment variable
        return os.getenv("CLUSTER_NAME")
    
    @classmethod
    @property
    def AZURE_CLIENT_ID(cls):
        # Get the value of the CLIENT_ID environment variable
        return os.getenv("AZURE_CLIENT_ID")
    
    @classmethod
    @property
    def AZURE_MANAGED_CLIENT_ID(cls):
        # Get the value of the CLIENT_ID environment variable
        return os.getenv("AZURE_MANAGED_CLIENT_ID")