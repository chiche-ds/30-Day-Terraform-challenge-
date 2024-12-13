# Day 14: Working with Multiple Providers in Terraform
## Participant Details

- **Name:** Dwayne Chima
- **Task Completed:** Configured and deployed resources across multiple AWS regions using Terraform provider aliases.
- **Date and Time:** 14th Dec 2024 12:00am

## Architecture Diagram
![multi](https://github.com/user-attachments/assets/604452fe-b496-423a-892a-0a48257429f4)

## Terraform Code 
**terraform.tf**
```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = ">= 5.80"
    }

    local = {
        source = "hashicorp/local"
        version = ">= 2.5.2"
    }

    tls = {
      source = "hashicorp/tls"
      version = ">= 4.0.6"
    }
  }

  required_version = ">= 1.10.0"
}

provider "aws" {
  region = "us-east-1"
  alias  = "east"
}

provider "aws" {
  region = "us-west-2"
  alias  = "west"
}

```
**main.tf**
```hcl
module "vpc" {
  source = "./modules/vpc"

  providers = {
    aws = aws.east
  }
}

module "security_groups" {
  source                        = "./modules/security_groups"
  vpc_id                        = module.vpc.vpc_id
  inbound_ports                 = ["80"]
  create_alb_ref_security_group = false
  # alb_sg                        = module.autoscaling.alb_sg

  providers = {
    aws = aws.east
  }
}


module "secrets" {
  source = "./modules/secrets"
  providers = {
    aws = aws.east
  }
}


module "instance" {
  source = "./modules/instance"
  web_sg = module.security_groups.web_sg
  public_subnets = module.vpc.public_subnets
  secret_data = module.secrets.secrets

  providers = {
    aws = aws.east
  }
}


module "vpc_west" {
  source = "./modules/vpc"

  providers = {
    aws = aws.west
  }
}


module "security_groups_west" {
  source                        = "./modules/security_groups"
  vpc_id                        = module.vpc_west.vpc_id
  inbound_ports                 = ["80"]
  create_alb_ref_security_group = false
  # alb_sg                        = module.autoscaling.alb_sg

  providers = {
    aws = aws.west
  }
}


module "instance_west" {
  source = "./modules/instance"
  web_sg = module.security_groups_west.web_sg
  public_subnets = module.vpc_west.public_subnets
  secret_data = module.secrets.secrets

  providers = {
    aws = aws.west
  }
}
```
