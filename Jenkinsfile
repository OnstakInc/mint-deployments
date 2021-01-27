pipeline {
    agent any 
    
    parameters {
        string(
            name: "CustomerName",
            defaultValue: "ONSTAK-POC",
            description: "Enter customer name for which stack is to be provisioned."
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
        AWS_ACCESS_KEY_ID = credentials('onstak-aws-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('onstak-aws-key-secret')
        AWS_REGION = "${params.Region}"
        VPC_ID = "${params.VPCId}"
        SUBNET01_ID = "${params.Subnet01Id}"
        SUBNET02_ID = "${params.Subnet02Id}"
        CUSTOMER_NAME = "${params.CustomerName}"
        EKS_WORKER_IMAGE = "${params.EKSWorkerImageId}"
        APPD_ACCOUNT = credentials('onstak-appd-account')
        APPD_API_KEY = credentials('onstak-appd-api-key')
        APPD_CONTROLLER = credentials('onstak-appd-controller')
    }

    stages {
        stage("Prepare") {
            steps {
                cleanWs()
                git branch: "main", url: "https://github.com/OnstakInc/mint-deployments.git"
            }
        }
        stage("Deploy EKS Cluster") {
            steps {
                sh "python3 -u ./launch.py"
            }
        }
        stage("Configure EKS Cluster") {
            steps {
                sh "cat ./output.vars"
                load "./output.vars"
                sh "chmod +x ./shell/bootstrap.sh"
                sh "./shell/bootstrap.sh ${env.EKSClusterName} ${env.EKSClusterEndpoint} ${env.EKSClusterCertificate} ${env.EKSWorkerIAMRoleArn}"
            }
        }
        stage("Deploy K8 Dashboard") {
            steps {
                sh "kubectl apply -f ./deployments/dashboard.yml --kubeconfig=./kubeconfig"
                sh "sleep 10"
            }
        }
        stage("Deploy K8 Metrics") {
            steps {
                sh "kubectl apply -f ./deployments/metrics-server.yml --kubeconfig=./kubeconfig"
                sh "sleep 10"
            }
        }
        stage("Configure AppD") {
            steps {
                echo "${APPD_API_KEY}"
                sh "kubectl create namespace appdynamics --kubeconfig=./kubeconfig || true"
                sh "kubectl delete secret cluster-agent-secret --namespace=appdynamics --kubeconfig=./kubeconfig || true"
                sh "kubectl create secret generic cluster-agent-secret --from-literal=controller-key='${APPD_API_KEY}' --namespace=appdynamics --kubeconfig=./kubeconfig || true"
                sh "kubectl apply -f ./deployments/cluster-operator.yml --namespace=appdynamics --kubeconfig=./kubeconfig"
                sh "kubectl get pods --namespace=appdynamics --kubeconfig=./kubeconfig"
                sh "python3 -u ./generate.py --customer=${CUSTOMER_NAME} --account=${APPD_ACCOUNT} --controllerUrl=${APPD_CONTROLLER}" 
                sh "sleep 10"
            }
        }
        stage("Deploy AppD Agents") {
            steps {
                sh "cat ./temp/cluster-agent.yml"
                sh "kubectl apply -f ./temp/cluster-agent.yml --namespace=appdynamics --kubeconfig=./kubeconfig"
                sh "sleep 10"
                sh "kubectl apply -f ./deployments/netviz-agent.yml --namespace=appdynamics --kubeconfig=./kubeconfig"
                sh "sleep 10"
                sh "kubectl apply -f ./deployments/db-log-config.yml --namespace=appdynamics --kubeconfig=./kubeconfig"
                sh "kubectl apply -f ./temp/db-agent.yml --namespace=appdynamics --kubeconfig=./kubeconfig"
                sh "sleep 10"
            }
        }
        stage("Deploy TeaStore") {
            steps {
                sh "kubectl create namespace tea-store --kubeconfig=./kubeconfig || true"
                sh "kubectl delete -f ./deployments/tea-store.yml --namespace=tea-store --kubeconfig=./kubeconfig || true"
                sh "sleep 10"
                sh "kubectl apply -f ./deployments/tea-store.yml --namespace=tea-store --kubeconfig=./kubeconfig"
                sh "sleep 10"
            }
        }
        stage("Deploy JMeter Load") {
            steps {
                sh "kubectl create namespace jmeter-load --kubeconfig=./kubeconfig || true"
                sh "kubectl delete -f ./deployments/jmeter-load.yml --namespace=jmeter-load --kubeconfig=./kubeconfig || true"
                sh "sleep 10"
                sh "kubectl apply -f ./deployments/jmeter-load.yml --namespace=jmeter-load --kubeconfig=./kubeconfig"
                sh "sleep 10"
            }
        }
        stage("Cleanup") {
            steps {
                cleanWs()
            }
        }
    }
}