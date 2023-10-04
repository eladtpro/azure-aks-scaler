from flask import Flask, request
from azure.mgmt.containerservice import ContainerServiceClient
from azure_connector import _AzureConnector
import json

app = Flask(__name__)

# @app.route('/', methods=['GET'])
@app.route('/scale', methods=['GET'])
def scale():
    scale_config = None
    args = request.args.get('config')
    if args is not None:
        scale_config = json.loads(args)
    azure_connector: _AzureConnector = _AzureConnector()
    print(f'scaling to config: {scale_config}, agent_pools: {azure_connector.list_node_pools()}')
    amount = azure_connector.scale_node_pools(scale_config)
    
    return f'Scaled to: {amount}'

if __name__ == '__main__': # file is run directly and not imported
    app.run(debug=False, host='0.0.0.0')

# app = create_app()
# app = Flask(__name__)
# app.run(debug=True)