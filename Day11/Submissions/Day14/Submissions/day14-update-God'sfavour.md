### Name: God'sfavour Braimah
### Task: Day 14: Working with Multiple Providers
### Date: 12/19/24
### Time: 12:20am
 ### Activity
# Day 14: Working with Multiple Providers - Deploying EC2 Instances

Welcome to Day 14 of the Terraform 30-Day Challenge! In this activity, we explore how to work with multiple providers in Terraform by deploying EC2 instances across multiple AWS regions. This demonstrates Terraform's capability to manage infrastructure in a multi-region setup using provider aliases.

---

## **Project Overview**

This project creates:
- An EC2 instance in the `us-east-1` region.
- An EC2 instance in the `us-west-2` region using a provider alias.

The setup ensures efficient scaling and deployment of infrastructure resources across multiple regions, showcasing Terraform's flexibility and power.

---

## **Terraform Configuration**

### **Code**

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# Default AWS Provider Configuration
provider "aws" {
  region = "us-east-1"
}

# AWS Provider with Alias for a Different Region
provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

# EC2 Instance in Default Region
resource "aws_instance" "default_region_instance" {
  ami           = "ami-0c02fb55956c7d316" # Amazon Linux 2 AMI (Replace with a valid AMI ID for us-east-1)
  instance_type = "t2.micro"

  tags = {
    Name = "DefaultRegionInstance"
  }
}

# EC2 Instance in West Region
resource "aws_instance" "west_region_instance" {
  provider      = aws.west
  ami           = "ami-0323c3dd2da7fb37d" # Amazon Linux 2 AMI (Replace with a valid AMI ID for us-west-2)
  instance_type = "t2.micro"

  tags = {
    Name = "WestRegionInstance"
  }
}
```

---

## **Steps to Deploy**

1. **Initialize Terraform:**
   ```bash
   terraform init
   ```

2. **Validate the Configuration:**
   ```bash
   terraform validate
   ```
   - This checks the code for syntax errors and ensures proper configuration.

3. **Plan the Deployment:**
   ```bash
   terraform plan
   ```
   - Review the execution plan to confirm the resources to be created.

4. **Apply the Configuration:**
   ```bash
   terraform apply
   ```
   - Type `yes` when prompted to confirm the deployment.

5. **Verify the Deployment:**
   - Log in to the AWS Management Console and check the EC2 Dashboard.
   - Ensure one EC2 instance is running in `us-east-1` and another in `us-west-2`.

---

## **Explanation**

### **Providers:**
- **Default Provider:** Used to deploy resources in the `us-east-1` region.
- **Alias Provider:** Used to deploy resources in the `us-west-2` region.

### **Resource Blocks:**
- Two `aws_instance` resources are defined:
  - `default_region_instance` for `us-east-1`.
  - `west_region_instance` for `us-west-2`, using the alias provider.

### **Key Details:**
- Replace the AMI IDs with valid IDs for the respective regions.
- Use `terraform destroy` to clean up resources after testing.

---

## **Benefits of Multi-Provider Configuration**
- Manage infrastructure in multiple regions or accounts seamlessly.
- Scale applications to meet regional demands.
- Enhance fault tolerance and redundancy by distributing resources across regions.

---

## **Conclusion**

This project demonstrates how Terraform's provider aliases enable multi-region deployments with ease. By mastering these concepts, you can efficiently manage complex, multi-cloud infrastructures.

---
