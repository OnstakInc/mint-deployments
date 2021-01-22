pipeline {
    agent any 
    
    parameters {
        string(
            name: "CustomerName",
            defaultValue: "MINT-POC",
            description: "Enter customer name for which stack is to be provisioned."
        )
        string(
            name: "AccessKey",
            defaultValue: "",
            description: "Provide AWS access key."
        )
        string(
            name: "SecretKey",
            defaultValue: "",
            description: "Provide AWS secret key."
        )
        choice(
            name: "Region",
            choices: ["us-east-1"],
            description: "Select an AWS region for stack provisioning."
        )
        string(
            name: "VPCId",
            defaultValue: "vpc-65817803",
            description: "Provide AWS VPC Id."
        )
        string(
            name: "Subnet01Id", 
            defaultValue: "subnet-641ba73f",
            description: "Provide AWS Subnet 01 Id."
        )
        string(
            name: "Subnet02Id",
            defaultValue: "subnet-4f43d82a",
            description: "Provide AWS Subnet 02 Id."
        )
        string(
            name: "EKSWorkerImageId",
            defaultValue: "ami-0dd0589ee7a07c236",
            description: "Provide EKS Worker Image Id."
        )
    }

    environment {
        AWS_ACCESS_KEY_ID = "${params.AccessKey}"
        AWS_SECRET_ACCESS_KEY = "${params.SecretKey}"
        AWS_REGION = "${params.Region}"
        VPC_ID = "${params.VPCId}"
        SUBNET01_ID = "${params.Subnet01Id}"
        SUBNET02_ID = "${params.Subnet02Id}"
        CUSTOMER_NAME = "${params.CustomerName}"
        EKS_WORKER_IMAGE = "${params.EKSWorkerImageId}"
    }

    stages {
        stage("Prepare") {
            steps {
                cleanWs()
            }
        }
        stage("Deploy EKS Cluster") {
            steps {
                sh "python3 -u launch.py"
            }
        }
        stage("Configure EKS Cluster") {
            steps {
                echo ""
            }
        }
        stage("Configure AppDynamics") {
            steps {
                echo ""
            }
        }
        stage("Deploy TeaStore") {
            steps {
                echo ""
            }
        }
        stage("Cleanup") {
            steps {
                cleanWs()
            }
        }
    }
}