# Day 5: Scaling Infrastructure

## Participant Details
- **Name:** Dwayne Chima
- **Task Completed:**  Completed Day 5: Scalig infrastructure
- **Date and Time:** 7th Dec 2024 2:30pm

| **Block**              | **Purpose**                                                                 | **Example Usage**                                                                                                                                   |
|-------------------------|-----------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| **Provider**            | Defines which cloud provider Terraform interacts with.                    | `provider "aws" { region = "us-east-1" }`                                                                                                           |
| **Resource**            | Declares infrastructure to be created or managed.                         | `resource "aws_instance" "web" { instance_type = "t2.micro" }`                                                                                     |
| **Data**                | Fetches information about existing resources or settings.                 | `data "aws_ami" "latest" { most_recent = true }`                                                                                                   |
| **Variable**            | Makes configurations flexible and reusable.                               | `variable "instance_type" { default = "t2.micro" }`                                                                                                |
| **Output**              | Displays useful information after applying changes.                       | `output "instance_ip" { value = aws_instance.web.public_ip }`                                                                                      |
| **Module**              | Encapsulates reusable configurations for better organization.             | `module "vpc" { source = "./modules/vpc" cidr_block = "10.0.0.0/16" }`                                                                             |
| **Backend**             | Specifies where Terraform stores state files.                             | `terraform { backend "s3" { bucket = "my-state" key = "prod/terraform.tfstate" } }`                                                                |

