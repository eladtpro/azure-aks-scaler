from flask import Flask, request
import os
from azure_connector import AzureConnector
import json
import logging


app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
@app.route('/test', methods=['GET'])
def test():
    logger.info('test called')
    return 'Hello World!'

@app.route('/list', methods=['GET'])
def list():
    azure_connector: AzureConnector = AzureConnector()
    return azure_connector.list_node_pools()

@app.route('/scale', methods=['GET'])
def scale():
    print(f'scale called')
    config, managed, client_id = get_request_args()
    print(f'config: {config}, managed: {managed}, client_id: {client_id}')
    azure_connector: AzureConnector = AzureConnector(managed, client_id)
    print(f'execute scale_node_pools: {config}, agent_pools: {azure_connector.list_node_pools()}')
    amount = azure_connector.scale_node_pools(config)
    
    return f'Scaled to: {amount}'

def get_request_args():
    config = None
    managed = True
    client_id = None

    req_config = request.args.get('config')
    req_managed = request.args.get('managed')
    req_client_id = request.args.get('client_id')

    if req_config is not None:
        config = json.loads(req_config)
    if req_managed is not None:
        managed = req_managed == 'true' or req_managed == '1'
    if req_client_id is not None:
        client_id = req_client_id

    return config, managed, client_id

if __name__ == '__main__': # file is run directly and not imported
    if "KUBERNETES_SERVICE_HOST" in os.environ:
        # Running in AKS container
        app.run(debug=False, host='0.0.0.0')
    else:
        app.run(debug=False, port=8080, host='0.0.0.0')
