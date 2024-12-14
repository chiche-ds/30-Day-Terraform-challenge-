# Day 14: Working with Multiple Providers - Part 1

## Participant Details

- **Name:Yusuf Abdulganiyu 
- **Task Completed:
  Reading: 
	- Chapter: Begin Chapter 7 of "Terraform: Up & Running"
  - Sections: "Working with One Provider", "What Is a Provider?", "How Do You Install Providers?",
                "How Do You Use Providers?", "Working with Multiple Copies of the Same Provider".
  - Videos:
          - Udemy:
              - Video 15: "Provider block"
              - Video 24: "Provider installation and visioning"
              - Video 25: "using multiple providers "

  Activity
	- Set up Terraform configurations that use multiple copies of the same provider, such as deploying resources in multiple AWS regions or accounts.
    Experiment with using provider aliases and understanding the role of provider versions.

  
  Social Media Post
        - https://www.linkedin.com/posts/yusuf-abdulganiyu_day14-terraform-cloudcomputing-activity-7273819976644378625-4gpQ?utm_source=share&utm_medium=member_desktop
  
- **Date and Time: December 14 2024, 23:15🕥 GMT+1

- Additional Notes:
  - Understood the basics of Terraform providers, how to install and use them, and how to work with multiple copies of the same provider.
  - Learnt the concepts of working with multiple providers in Terraform and prepare for more complex, multi-provider setups.
  - Successfully deployed resources across multiple regions or accounts using multiple copies of the same provider.
 
```hcl
# AWS provider for two different regions
provider "aws" {
  alias  = "primary"
  region = "us-east-1"
}

provider "aws" {
  alias  = "secondary"
  region = "us-west-2"
}

# Azure provider
provider "azurerm" {
  alias    = "east_us"
  features {}
}

# Resource in AWS (US-East-1)
resource "aws_s3_bucket" "east_bucket" {
  provider = aws.primary
  bucket   = "example-east-bucket"
}

# Resource in AWS (US-West-2)
resource "aws_s3_bucket" "west_bucket" {
  provider = aws.secondary
  bucket   = "example-west-bucket"
}

# Resource in Azure (East US)
resource "azurerm_resource_group" "example" {
  provider = azurerm.east_us
  name     = "example-resources"
  location = "East US"
}

```

![image](https://github.com/user-attachments/assets/bbd288bf-bc24-4263-8598-ad71f4c4e7c5)


## Experience Working with Provider Aliases in Terraform

- Challenges Faced:

    - Provider Configuration: Managing multiple providers in a single file can get complex, especially with aliases.
    - Credential Handling: Ensuring each provider has the correct credentials (e.g., profiles or environment variables).
    - Terraform State: Avoiding state conflicts when using the same resource types across regions/accounts.


- Solutions and Best Practices:

    - Using Aliases: Helps segregate configurations logically, especially in multi-region deployments.
    - Remote State Management: Store Terraform state in S3 or Azure Blob Storage with locking enabled using DynamoDB or Azure Table Storage.
    - Workspaces for Segregation: Use workspaces for staging environments.
    - Clear Documentation: Commenting code blocks and using meaningful aliases like us_east or prod_account for better clarity.

- Benefits:
  
    - Achieved fault tolerance with multi-region setups by enabling Route 53 failover.
    - Leveraged multi-cloud capabilities for enhanced flexibility and cost optimization.
    - Simplified management of resources across multiple environments with aliases and remote state.

