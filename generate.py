import re
import os
import argparse

TEMP_DIR = './temp'

#######################################################################
# Command Line Arguments ##############################################
#######################################################################
parser = argparse.ArgumentParser()

parser.add_argument('--customer', type=str, help='Customer Name', required=True)
parser.add_argument('--account', type=str, help='AppDynamics Account', required=True)
parser.add_argument('--controllerUrl', type=str, help='AppDynamics Controller URL', required=True)
args = parser.parse_known_args()[0]
print(args.account)
#######################################################################


#######################################################################
# Create Temp Directory ###############################################
#######################################################################
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
#######################################################################

#######################################################################
# Define Global Variables #############################################
#######################################################################
CUSTOMER_NAME = args.customer.lower()
APPD_ACCOUNT = args.account
APPD_CONTROLLER = args.controllerUrl
#######################################################################


#######################################################################
# Generate Cluster Agent Depoyment ####################################
#######################################################################
print('INFO: Generate Cluster Agent Deployment YAML')
cluster_agent = open('./deployments/cluster-agent.yml', 'r').read()

app_name = f'TeaStore-{CUSTOMER_NAME}'
app_name = re.sub('[^a-zA-Z]+', '_', app_name)

cluster_agent = cluster_agent.replace('APP_NAME', app_name)
cluster_agent = cluster_agent.replace('ACCOUNT', APPD_ACCOUNT)
cluster_agent = cluster_agent.replace('CONTROLLER', APPD_CONTROLLER)

file = open('./temp/cluster-agent.yml', 'w')
file.write(cluster_agent)
file.close()
#######################################################################