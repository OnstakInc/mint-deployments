#!/bin/bash

EKS_CLUSTER=$1
EKS_ENDPOINT=$2
EKS_CERTIFICATE=$3
EKS_WORKER_ROLE=$4

token=$(/usr/local/bin/aws eks get-token --cluster-name $EKS_CLUSTER | jq -r '.status.token')

cat <<EOT > ./kubeconfig
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: $EKS_CERTIFICATE
    server: $EKS_ENDPOINT
  name: eks-cluster
contexts:
- context:
    cluster: eks-cluster
    user: eks-user
  name: eks-context
current-context: eks-context
kind: Config
preferences: {}
users:
- name: eks-user
  user:
    token: $token
EOT


cat <<EOT > ./aws-auth.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: $EKS_WORKER_ROLE
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes

EOT


# kubectl create namespace mint-admin --kubeconfig=./kubeconfig
kubectl create serviceaccount mint-admin --namespace=kube-system --kubeconfig=./kubeconfig
kubectl create clusterrolebinding mint-admin-role-binding --clusterrole=cluster-admin --serviceaccount=mint-admin:mint-admin --namespace=kube-system --kubeconfig=./kubeconfig

kubectl describe secrets --namespace=kube-system --kubeconfig=./kubeconfig | grep 'token:' | tail -n 1 | sed -En "s/token:      //p" > ./eks-credentials

kubectl apply -f ./aws-auth.yml --kubeconfig=./kubeconfig

echo "EKS Kube Config:"
cat ./kubeconfig

echo "AWS EKS Token:"
cat ./eks-credentials