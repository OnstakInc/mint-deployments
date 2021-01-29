import os
import yaml
import json
import boto3
import argparse

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.environ.get('AWS_REGION')

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)
#######################################################################
# Command Line Arguments ##############################################
#######################################################################
parser = argparse.ArgumentParser()

parser.add_argument('--customer', type=str, help='Customer Name', required=True)
args = parser.parse_known_args()[0]
#######################################################################


#######################################################################
# Get EKS Worker Details ##############################################
#######################################################################
ec2 = session.client('ec2')

filters = [
    {
        'Name': 'tag:Name', 
        'Values': [f'mint-{args.customer}-eks-worker-{AWS_REGION}'.lower()]
    }
]

result = ec2.describe_instances(Filters=filters)

for reservation in result['Reservations']:
    for instance in reservation['Instances']:
        if instance.get('PublicIpAddress'):
            print(f"TeaStore URL: http://{instance.get('PublicIpAddress')}:30080")
            print(f"K8 Dashboard URL: https://{instance.get('PublicIpAddress')}:32443")
#######################################################################

#######################################################################
# Print AWS EKS Token #################################################
#######################################################################
try:
    eks_token = open('./eks-credentials', 'r').read()
    print(f'K8 Auth Token: {eks_token}')
except:
    print('ERROR: Unable to get eks-credentials')
#######################################################################