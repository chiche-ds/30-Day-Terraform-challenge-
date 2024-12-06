# Day 15: Working with Multiple Providers - Part 2

## Participant Details

- **Name:** Omekwu Victor Ebube  
- **Task Completed:** Working with Multiple Providers using Terraform.
- **Date and Time:** 17-November-2024 at 11:40 AM WAT
---
## providers.tf
```bash
# providers.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.70"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

provider "azurerm" {
  features {}
}
```
---
## main.tf AWS modules
```bash
# modules/azure/main.tf
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_virtual_network" "vnet" {
  name                = "basic-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
}

# modules/azure/variables.tf
variable "resource_group_name" {}
variable "location" {}

# modules/azure/outputs.tf
output "resource_group_id" {
  value = azurerm_resource_group.main.id
}
```
---
## main.tf Azure modules
```bash
# modules/azure/main.tf
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_virtual_network" "vnet" {
  name                = "basic-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name
}

# modules/azure/variables.tf
variable "resource_group_name" {}
variable "location" {}

# modules/azure/outputs.tf
output "resource_group_id" {
  value = azurerm_resource_group.main.id
}
``