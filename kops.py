import subprocess,time

env_list = [
    {
        "env_name": "dev",
        "domain_name": "elliottlamararnold.com",
        "hosted_zone_id": "Z02041259ULZR04XYMKA",
        "s3_bucket": "gpt-k8s-store-development",
        "vpc_id": "vpc-0df0e0a686549ddba"
    },
    {
        "env_name": "prod",
        "domain_name": "lamararnold.com",
        "hosted_zone_id": "Z0313571W53DLDVW41Y0",
        "s3_bucket": "gpt-k8s-store-prod",
        "vpc_id": "vpc-0f788f7799b50d635"
    },
    {
        "env_name": "stg",
        "domain_name": "elliottarnold.com",
        "hosted_zone_id": "Z017710613GRK87AKD5E6",
        "s3_bucket": "gpt-k8s-store-staging",
        "vpc_id": "vpc-0c1bfc0a7ccfed14c"
    }
]



for env in env_list:
    name = env["domain_name"]
    region = "us-east-1"
    s3_bucket = env["s3_bucket"]
    vpc_id = env["vpc_id"]
    hosted_zone_id = env["hosted_zone_id"]
    export_command = f"export KOPS_STATE_STORE=s3://{s3_bucket}"
    
    #Create a new cluster configuration
    create_command = f"kops create cluster --node-count 2 --vpc {vpc_id} --node-size t2.medium --master-size t2.medium --zones {region}a,{region}b --name {name} --dns-zone {hosted_zone_id} --yes --cloud aws"
    subprocess.run(f"{export_command} && {create_command}", shell=True)
    
    # Update the cluster configuration
    update_command = f"kops update cluster {name} --yes"
    subprocess.run(f"{export_command} && {update_command}", shell=True)
    
    # Wait for the cluster to be ready
    # time.sleep(600)
    validate_command = f"kops validate cluster {name} --wait 10m"
    subprocess.run(f"{export_command} && {validate_command}", shell=True)
        # Wait for the cluster to be ready
    # time.sleep(600)
    
    
    
    # # Export kubectl configuration
    export_command = f"kops export kubecfg --state s3://{s3_bucket}"
    subprocess.run(f"{export_command}", shell=True)


#toDo purchase 3 domains from AWS
# study how to use customize 
#understand how to promote deployments into higher environments with argocd