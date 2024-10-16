## Day 6 Task : Understanding Terraform State
_Utibe Okon | Sat, October 12 2024 | 6:52 AM - GMT+1_

__State with Terraform | Points I learnt:__ 
- State is a way for terraform to remember and keep track of resources that it has created. When terraform plan is run, terraform compares the current configuration to the current state in the statefile (.tfstate) and if they are not the same, it plans changes to ensure they are the same.

- By default, the statefile is created in the default directory on local system. But this is not an efficient way to manage state especially when you are collaborating with other persons (which is always usually the case). 

- Cloud platforms and terraform cloud provide ways to maange state file remotely. I learnt about S3 and DynamoDB for the state management. 

- I also took another step to do further research and learnt about using azure blob storage for state management. It works similar as S3 bucket, but does not need an extra service for the state locking.

- Speaking of locking, state locking is a way for terraform to tie down a satte file when it is in use, to ensure two perosns do not try to make changes to the file simultaneously, as this would cause errors.

`code samples`

```hcl

# remote backend sample configuration wirh azure blob storage
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>4"
    }
  }

  backend "azurerm" {
    resource_group_name  = "terraformstatesRG"
    storage_account_name = "terraformstate737"
    container_name       = "tfstateblob"
    key                  = "aws/3tier/terraform.tfstate"
  }
}

# terraform sample state file when a basic ec2 instance is created
{
    "version": 4,
    "terraform_version": "1.2.3",
    "serial": 1,
    "lineage": "86545604-7463-4aa5-e9e8-a2a221de98d2",
    "outputs": {},
    "resources": [
    {
    "mode": "managed",
    "type": "aws_instance",
    "name": "example",
    "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
    "instances": [
    {
    "schema_version": 1,
    "attributes": {
    "ami": "ami-0fb653ca2d3203ac1",
    "availability_zone": "us-east-2b",
    "id": "i-0bc4bbe5b84387543",
    "instance_state": "running",
    "instance_type": "t2.micro",
    "(...)": "(truncated)"
    }
    }
    ]
    }
    ]
}
```