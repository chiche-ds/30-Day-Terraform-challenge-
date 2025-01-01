# Day 22: Putting It All Together - Wrapping Up the Book and Celebrating Success! 
## Participant Details

- **Name:** Otu Michael Udo
- **Task Completed:** Putting It All Together - Wrapping Up the Book and Celebrating Success! 
- **Date and Time:** Jan 1ST 2025 2:21 AM



### terraform/modules/terraform-aws-EC2/main.tf
```
# ./modules/ec2-instance/main.tf

resource "aws_instance" "app" {
  ami           = var.ami_id
  instance_type = var.instance_type
  tags = {
    Name = "Terraform-Managed-Instance"
  }
}
### main.tf
```
variable "ami_id" {
  description = "The Amazon Machine Image ID"
  type        = string
}

variable "instance_type" {
  description = "The type of instance to use"
  type        = string
  default     = "t3.micro"
}

provider "aws" {
  region  = "us-east-1"  # Change to your desired region 
}
module "ec2_instance" {
  source       = "app.terraform.io/massive-dynamic3/EC2/aws"
  version      = "1.0.1"
  ami_id       = "ami-0e2c8caa4b6378d8c"
  instance_type = "t2.micro"
}
```
terraform {
  backend "remote" {
    organization = "terraform-cloud"

    workspaces {
      name = "massive-dynamic5"
    }
  }
}



### Sentinel policy
Created a policy that only allows instance of a particular type to be provisioned on AWS CLOUD. Instance types different from the one I specified in the policy will stop the CI workflow each time I commit to the repo intergrated to my terraform workspace.

```
import "tfplan/v2" as tfplan

# Define the allowed EC2 instance types
allowed_instance_types = ["t2.micro", "t3.micro"]

# Main rule to validate instance types
main = rule {
    all tfplan.resource_changes as _, resource {
        # Check if the resource is an AWS EC2 instance
        resource.type is "aws_instance" and
        resource.mode is "managed" and
        # Ensure the action involves creation or updating of the resource
        resource.change.actions contains "create" and
        # Ensure the instance_type attribute exists
        "instance_type" in resource.applied and
        # Validate that the instance_type is in the allowed list
        resource.applied.instance_type in allowed_instance_types
    }
}

# Explanation:
# - The policy enforces that only `t2.micro` and `t3.micro` are allowed.
# - It validates that the `instance_type` attribute exists before accessing it to prevent `undefined` errors.
# - It ensures the policy applies only to resources being created or updated (`create` action).
