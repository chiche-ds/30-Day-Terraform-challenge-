# Day 6: Understanding Terraform State

## Participant Details

- **Name:** Omekwu Victor Ebube  
- **Task Completed:** On Day 6, I focused on managing Terraform state, utilizing both remote state storage and backend configurations for both Azure Remote Backend and Terraform Cloud Backend. I explored how to configure the backend for storing the Terraform state file securely, ensuring team collaboration. Additionally, I implemented a cloud workspace.  
- **Date and Time:** 27-08-2024 at 21:30 PM IST  
---
### azure-remote-backend.tf: This Configures Azure backend for secure Terraform state.
```bash
terraform {
  backend "azurerm" {
    resource_group_name  = "production"
    storage_account_name = "ebubevickterraformstate"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
    sas_token             = "YOUR_SAS_TOKEN" 
    # SAS token can also be set via environment variable.
  }
}
```
---
### terraform-cloud-backend.tf: This Sets up Terraform Cloud backend for centralized state.
```bash
terraform { 
  cloud { 
    
    organization = "ebubevick" 

    workspaces { 
      name = "my-azure-app" 
    } 
  } 
}
```
---
### main.tf
```bash
provider "azurerm" {
  features {}

  subscription_id = var.subscription
}

resource "azurerm_resource_group" "rg" {
  name     = var.rg
  location = var.location
}

resource "random_id" "randomness" {
  byte_length = 9
}

resource "azurerm_virtual_network" "vnet" {
  name                = "${var.vnet}-${random_id.randomness.hex}"
  address_space       = var.address_space
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_subnet" "public_subnet_1" {
  name                 = "${azurerm_virtual_network.vnet.name}-public-subnet-1"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = var.address_prefixes
}
```
---
### variables.tf
```bash
variable "subscription" {
  description = "Subscription ID to use"
  type        = string
  default     = "subscription" # Replace with your subscription
}

variable "rg" {
  description = "Resource Group Name"
  type        = string
  default     = "production-rg"
}

variable "location" {
  description = "Resource Location"
  type        = string
  default     = "uksouth"
}

variable "vnet" {
  description = "VNet Name"
  type        = string
  default     = "production-vnet"
}

variable "address_space" {
  description = "Address Space for VNet"
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "address_prefixes" {
  description = "Address Prefixes for Subnet"
  type        = list(string)
  default     = ["10.0.52.0/24"]
}
```