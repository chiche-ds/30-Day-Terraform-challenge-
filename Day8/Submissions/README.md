## Submit all day8 .md files in this folder 
Undaretsanding Terraform modules by reading chap.4
Deployed infractructures using Terraform modules and understanding how to reference the folders
Also undrestood variables, inputs and out puts
Examplesof a folder structure: terraform-ec2-module/
 ├── main.tf
 ├── variables.tf
 ├── outputs.tf
 └── README.md
module "ec2_instance" {
  source        = "../terraform-ec2-module" 
  region        = "us-west-2"
  ami_id        = "ami-0c55b159cbfafe1f0"    
  instance_type = "t2.micro"
  instance_name = "my-ec2-instance"
}

output "instance_id" {
  value = module.ec2_instance.instance_id
}

output "public_ip" {
  value = module.ec2_instance.public_ip
}

Block post:
How to Build and Deploy a Reusable Terraform Module for an EC2 Instance on AWS

Terraform is a powerful infrastructure-as-code (IaC) tool that allows you to define, deploy, and manage infrastructure across multiple cloud platforms. A key benefit of using Terraform is its modularity, which enables you to create reusable components that can be applied to different projects or environments.

In this blog post, we’ll walk through the process of building a reusable Terraform module to deploy an EC2 instance on AWS and demonstrate how to use this module to deploy infrastructure in a real-world scenario.
What is a Terraform Module?

A Terraform module is a self-contained package of Terraform configurations that define a specific piece of infrastructure. By packaging infrastructure as a module, you can reuse it across different environments, projects, or teams, which makes your infrastructure code more manageable and scalable.
Step 1: Create a Basic Terraform Module

We will create a simple Terraform module that deploys an EC2 instance on AWS. Follow the steps below to set up the module.
Directory Structure

The module will consist of three primary files: main.tf, variables.tf, and outputs.tf. Here is how the directory structure should look:

terraform-ec2-module/
 ├── main.tf
 ├── variables.tf
 ├── outputs.tf
 └── README.md

Defining the Resources in main.tf

This file contains the Terraform code to create an EC2 instance. We use the aws_instance resource to define the EC2 instance, specifying the AMI ID, instance type, and tags.


provider "aws" {
  region = var.region
}

resource "aws_instance" "ec2_instance" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = var.instance_name
  }
}

Defining Inputs with variables.tf

Next, we define the input variables needed for the module. These inputs include the AWS region, AMI ID, instance type, and instance name. This file makes the module flexible and reusable across different environments.


variable "region" {
  description = "AWS region where the instance will be deployed"
  type        = string
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "Instance type for the EC2 instance"
  type        = string
  default     = "t2.micro"
}

variable "instance_name" {
  description = "Name for the EC2 instance"
  type        = string
}

Defining Outputs in outputs.tf

The outputs.tf file captures the key information from the deployed infrastructure, such as the EC2 instance ID and its public IP. These outputs are useful when you want to reference the instance in other parts of your Terraform configuration.


output "instance_id" {
  description = "The ID of the EC2 instance"
  value       = aws_instance.ec2_instance.id
}

output "public_ip" {
  description = "The public IP of the EC2 instance"
  value       = aws_instance.ec2_instance.public_ip
}

README.md

It's a good practice to document your module. The README.md should contain an explanation of what the module does, instructions on how to use it, and details of the input variables and outputs.
Step 2: Deploy Infrastructure Using the Terraform Module

Now that we’ve created the Terraform module, we can use it in a new Terraform project to deploy an EC2 instance on AWS.
Directory Structure for the Project Using the Module


my-terraform-project/
 ├── main.tf
 ├── terraform.tfvars
 └── outputs.tf

Using the Module in main.tf

In this file, we will call the module we created earlier and pass the necessary input variables like the region, AMI ID, and instance type.


module "ec2_instance" {
  source        = "../terraform-ec2-module"  # Path to your module
  region        = "us-west-2"
  ami_id        = "ami-0c55b159cbfafe1f0"    # Replace with a valid AMI ID
  instance_type = "t2.micro"
  instance_name = "my-ec2-instance"
}

output "instance_id" {
  value = module.ec2_instance.instance_id
}

output "public_ip" {
  value = module.ec2_instance.public_ip
}

Optional: Store Values in terraform.tfvars

You can store variable values in a terraform.tfvars file to avoid hardcoding them directly into the configuration files.


region        = "us-west-2"
ami_id        = "ami-0c55b159cbfafe1f0"
instance_name = "my-ec2-instance"

Step 3: Apply the Terraform Configuration

To deploy the infrastructure, follow these steps:

    Initialize Terraform: Run the following command to initialize the project and download necessary providers:


terraform init

Apply the Configuration: Once initialized, apply the configuration to deploy the EC2 instance:

    terraform apply

    Review and Confirm: Terraform will display the actions it will take (e.g., create an EC2 instance). Type yes to confirm and proceed with the deployment.

Conclusion

In this tutorial, we created a reusable Terraform module that provisions an EC2 instance on AWS and demonstrated how to use it in a real-world Terraform project. By leveraging modules, you can write more maintainable, reusable, and scalable infrastructure code.

Using this approach, you can easily adapt the module to deploy other infrastructure components like VPCs, load balancers, and databases. Terraform’s modularity is an excellent way to promote code reuse and standardization across your organization.

Start building your own Terraform modules today, and enjoy the benefits of clean, reusable infrastructure code!

