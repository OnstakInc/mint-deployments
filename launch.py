import os
import yaml
import time
import boto3

OUTPUT_FILE = './output.vars'
EKS_CLUSTER_TEMPLATE = './cloudformation/eks-cluster.yml'

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.environ.get('AWS_REGION')

VPC_ID = os.environ.get('VPC_ID')
SUBNET01_ID = os.environ.get('SUBNET01_ID')
SUBNET02_ID = os.environ.get('SUBNET02_ID')
CUSTOMER_NAME = os.environ.get('CUSTOMER_NAME')
EKS_WORKER_IMAGE = os.environ.get('EKS_WORKER_IMAGE')

STACK_NAME = f'{CUSTOMER_NAME}-EKS-STACK'.upper()

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

STACKS_LIST = []
#######################################################################


#######################################################################
# Validate VPC ########################################################
#######################################################################
try:
    print(f'INFO: Validating VPC: {VPC_ID}')
    ec2 = session.resource('ec2')
    vpc = ec2.Vpc(VPC_ID)
    print(f'INFO: VPC Validated: {vpc.vpc_id}')
except:
    print(f'ERROR: VPC Validation Failed! Please provide a valid VPC Id.')
    exit(1)
#######################################################################


#######################################################################
# Validate Subnets ####################################################
#######################################################################
print(f'INFO: Validating Subnets')
print(f'INFO: Subnet 01: {SUBNET01_ID}')
print(f'INFO: Subnet 02: {SUBNET02_ID}')

filters = [
    {'Name':'vpcId', 'Values':[VPC_ID]}
]

ec2 = session.resource('ec2')
subnets = list(ec2.subnets.filter(Filters=filters))
subnets = list(filter(lambda e: e.id == SUBNET01_ID or e.id == SUBNET02_ID, subnets))

if len(subnets) != 2:
    print(f'ERROR: Subnet Validation Failed!')
    print(f'ERROR: Please provide two valid subnets ids in different availability zones.')
    exit(1)

print(f'INFO: Validated Subnet 01: {SUBNET01_ID}')
print(f'INFO: Validated Subnet 02: {SUBNET02_ID}')
#######################################################################


#######################################################################
# Create CloudFormation Stack #########################################
#######################################################################
try:

    cloudformation = session.client('cloudformation')
    cloudformation_template = open(EKS_CLUSTER_TEMPLATE, 'r').read()

    try:
        stack_status = cloudformation.describe_stacks(StackName=STACK_NAME)['Stacks'][0]['StackStatus']
    except:
        stack_status = None

    if not stack_status:

        aws_parameters = [
            {'ParameterKey': 'VpcID', 'ParameterValue': VPC_ID},
            {'ParameterKey': 'SubnetId01', 'ParameterValue': SUBNET01_ID},
            {'ParameterKey': 'SubnetId02', 'ParameterValue': SUBNET02_ID},
            {'ParameterKey': 'CustomerName', 'ParameterValue': CUSTOMER_NAME.lower()},
            {'ParameterKey': 'EKSWorkerImageID', 'ParameterValue': EKS_WORKER_IMAGE},
        ]

        print('INFO:', aws_parameters)

        result = cloudformation.create_stack(
            StackName=STACK_NAME,
            TemplateBody=cloudformation_template,
            Parameters=aws_parameters,
            Capabilities=[
                'CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM',
            ]
        )

        STACKS_LIST.append(STACK_NAME)

    else:
        print(f'INFO: Stack {STACK_NAME} already exists. Skipping stack deployment.')
        STACKS_LIST.append(STACK_NAME)

except Exception as e:
    print(e)
    exit(1)
#######################################################################

#######################################################################
# Wait For Stack Creation #############################################
#######################################################################
completed_stacks = []
while True:

    try:

        for stack_name in STACKS_LIST:

            if stack_name in completed_stacks:
                continue

            cloudformation = session.client('cloudformation')

            status = cloudformation.describe_stacks(
                StackName=stack_name
            )

            if status['Stacks'][0]['StackStatus'] == 'CREATE_COMPLETE':
                completed_stacks.append(stack_name)

            if status['Stacks'][0]['StackStatus'] == 'ROLLBACK_IN_PROGRESS' or  status['Stacks'][0]['StackStatus'] == 'ROLLBACK_COMPLETE':
                print(f"ERROR: Stack Failed: {stack_name}")
                print('ERROR: Unable To Complete CloudFormation Deployment.')
                exit(1)

            print(f"INFO: StackName: {stack_name}, Status: {status['Stacks'][0]['StackStatus']}")

        if len(STACKS_LIST) == len(completed_stacks):
            print('INFO: CloudFormation Completed Successfully.')
            break

        time.sleep(10)

    except Exception as e:
        print(e)
        exit(1)
#######################################################################


#######################################################################
# Print Stack Information #############################################
#######################################################################

try:

    cloudformation = session.client('cloudformation')

    stack = cloudformation.describe_stacks(
        StackName=STACK_NAME
    )

    outputs = stack['Stacks'][0].get('Outputs', [])

    output_file = open(OUTPUT_FILE, 'w')

    print('INFO: Stack Information')
    print('-----------------------------------------------')
    for o in outputs:
        output_file.write(f"env.{o['OutputKey']}='{o['OutputValue']}'\n")
        print(f"{o['OutputKey']}: {o['OutputValue']}")
    print('-----------------------------------------------')

    output_file.close()

except Exception as e:
    print(e)
    exit(1)

#######################################################################


print('Exiting! All The Tasks Are Completed Successfully.')
exit(0)