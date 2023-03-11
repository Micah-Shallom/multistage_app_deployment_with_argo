export KOPS_STATE_STORE=s3://gpt-k8s-store
export NAME=elliottlamararnold.com
export AWS_REGION=us-east-1
export VPC_IDS="vpc-0df0e0a686549ddba,vpc-0f788f7799b50d635,vpc-0c1bfc0a7ccfed14c"

# Create S3 buckets for the new cluster
# gpt-k8s-store-development
# gpt-k8s-store-staging
# gpt-k8s-store-prod
# Create Route 53 entries for the new cluster
aws route53 create-hosted-zone --name $NAME --caller-reference $(date +%s)
aws route53 create-hosted-zone --name api.$NAME --caller-reference $(date +%s)

# Create a new cluster configuration
kops create cluster \
  --node-count 2 \
  --node-size t2.medium \
  --master-size t2.medium \
  --zones "${AWS_REGION}a,${AWS_REGION}b" \
  --name $NAME \
  --dns-zone $(aws route53 list-hosted-zones-by-name --dns-name $NAME --query 'HostedZones[0].Id' --output text) \
  --vpc $VPC_IDS \
  --state $KOPS_STATE_STORE \
  --yes \
  --cloud aws

# Update the cluster configuration
kops update cluster $NAME --yes

# Wait for the cluster to be ready
kops validate cluster --wait 10m

# Export kubeconfig
kops export kubecfg --state $KOPS_STATE_STORE

# # Delete the old S3 buckets and Route 53 entries
# aws s3 rb s3://$NAME-kops-state-store --force
# aws s3 rb s3://$NAME-kops-logs-store --force
# aws route53 delete-hosted-zone --id $(aws route53 list-hosted-zones-by-name --dns-name $NAME --query 'HostedZones[0].Id' --output text)
# aws route53 delete-hosted-zone --id $(aws route53 list-hosted-zones-by-name --dns-name api.$NAME --query 'HostedZones[0].Id' --output text)

# # Delete the cluster
# kops delete cluster --name $NAME --yes
