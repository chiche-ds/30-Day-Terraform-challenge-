# Day 17: Automated Testing of Terraform Code

## Participant Details

- **Name:** Otu Michael Udo
- **Task Completed:** Implemented unit tests, integration tests, and end-to-end tests for a Terraform project.
- **Date and Time:** Tue 29th Decemberr, 2024 | 11:38 am

I really faced some challenges with automated testing . I was glad to get the basics of automated testing which involces:

- Unit tests
- Automated tests
- End-to-end tests

Terratest is an extern library buildt with Go is usually used to test terraform code to ensure it works as expected. 

## Terraform Code 
```hcl
# Create VPC
resource "aws_vpc" "main" {
  cidr_block           = var.cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "${var.name}-vpc"
  }
}

# Create public subnets
resource "aws_subnet" "public" {
  count             = length(var.public_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnets[count.index]
  availability_zone = var.azs[count.index]
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.name}-public-${count.index + 1}"
  }
}

# Create private subnets
resource "aws_subnet" "private" {
  count             = length(var.private_subnets)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnets[count.index]
  availability_zone = var.azs[count.index]
  tags = {
    Name = "${var.name}-private-${count.index + 1}"
  }
}


```

I did run an automated on mu vpc module using _test.go file


package test

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestVpcModule(t *testing.T) {
	t.Parallel()

	// Specify the Terraform module directory
	terraformOptions := &terraform.Options{
		TerraformDir: "C://Users//madus//Desktop//30 Days of Terraform//30-Day-Terraform-challenge-//Day18//module//vpc-module", // Adjust based on the location of your Terraform configuration.

		// Pass variables to Terraform
		Vars: map[string]interface{}{
			"cidr":            "10.0.0.0/16",
			"public_subnets":  []string{"10.0.1.0/24", "10.0.2.0/24"},
			"private_subnets": []string{"10.0.3.0/24", "10.0.4.0/24"},
			"azs":             []string{"us-east-1a", "us-east-1b"},
			"name":            "test-vpc",
		},
	}

	// Clean up resources after test
	defer terraform.Destroy(t, terraformOptions)

	// Run Terraform Init and Apply
	terraform.InitAndApply(t, terraformOptions)

	// Get outputs
	vpcID := terraform.Output(t, terraformOptions, "vpc_id")
	publicSubnetIDs := terraform.OutputList(t, terraformOptions, "public_subnet_ids")
	privateSubnetIDs := terraform.OutputList(t, terraformOptions, "private_subnet_ids")

	// Validate outputs
	assert.NotEmpty(t, vpcID, "VPC ID should not be empty")
	assert.Equal(t, 2, len(publicSubnetIDs), "There should be 2 public subnets")
	assert.Equal(t, 2, len(privateSubnetIDs), "There should be 2 private subnets")
}
