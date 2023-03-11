import subprocess,time

env_list = [
    {
        "env_name": "dev",
        "domain_name": "elliottlamararnold-dev.com",
        "hosted_zone_id": "Z03476993IN1YTE6MVIVQ",
        "s3_bucket": "gpt-k8s-store-development",
        "vpc_id": "vpc-0df0e0a686549ddba"
    },
    {
        "env_name": "prod",
        "domain_name": "elliottlamararnold-prod.com",
        "hosted_zone_id": "Z01969251DOZMTZ3KY65I",
        "s3_bucket": "gpt-k8s-store-prod",
        "vpc_id": "vpc-0f788f7799b50d635"
    },
    {
        "env_name": "stg",
        "domain_name": "elliottlamararnold-stg.com",
        "hosted_zone_id": "Z01494153GTTP6C6ZQMNQ",
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
    
    # Create a new cluster configuration
    create_command = f"kops create cluster --node-count 2 --node-size t2.medium --master-size t2.medium --zones {region}a,{region}b --name {name} --dns-zone {hosted_zone_id} --yes --cloud aws"
    subprocess.run(f"{export_command} && {create_command}", shell=True)
    
    # Update the cluster configuration
    update_command = f"kops update cluster {name} --yes"
    subprocess.run(f"{export_command} && {update_command}", shell=True)
    
    # Wait for the cluster to be ready
    time.sleep(600)
    validate_command = "kops validate cluster --wait 10m"
    subprocess.run(f"{export_command} && {validate_command}", shell=True)
    
    
    # Export kubectl configuration
    export_command = f"kops export kubecfg --state s3://{s3_bucket}"
    subprocess.run(f"{export_command}", shell=True)
