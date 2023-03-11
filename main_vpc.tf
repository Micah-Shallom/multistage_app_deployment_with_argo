provider "aws" {
  region = "us-east-1"
}

module "dev_vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name = "dev_vpc"
  cidr = "10.0.0.0/16"
  azs = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}

module "staging_vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name = "staging_vpc"
  cidr = "10.1.0.0/16"
  azs = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.1.1.0/24", "10.1.2.0/24", "10.1.3.0/24"]
  public_subnets = ["10.1.4.0/24", "10.1.5.0/24", "10.1.6.0/24"]
 
  tags = {
    Terraform   = "true"
    Environment = "staging"
  }
}

module "prod_vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name = "prod_vpc"
  cidr = "10.2.0.0/16"
  azs = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.2.1.0/24", "10.2.2.0/24", "10.2.3.0/24"]
  public_subnets = ["10.2.4.0/24", "10.2.5.0/24", "10.2.6.0/24"]
  tags = {
    Terraform   = "true"
    Environment = "prod"
  }
}


output "dev_vpc_id" {
  value = module.dev_vpc.vpc_id
}

output "staging_vpc_id" {
  value = module.staging_vpc.vpc_id
}

output "prod_vpc_id" {
  value = module.prod_vpc.vpc_id
}
