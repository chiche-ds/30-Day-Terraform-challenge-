# Day 8: Reusing Infrastructure with Modules

## Participant Details

- **Name:** Omekwu Victor Ebube  
- **Task Completed:** On Day 8, I focused on creating reusable Terraform modules, learning about input and output variables, and deploying infrastructure using these modules. This task helped me understand how to structure Terraform code for better scalability and reusability.  
- **Date and Time:** 11-Nov-2024 at 12:45 PM IST
---
## Public Module Registry
```bash
# root/main.tf

# Virtual Network Module
module "vnet-public-module" {
  source  = "Azure/vnet/azurerm"
  version = "4.1.0"

  vnet_name           = "public-${var.vnet_name}"
  resource_group_name = var.resource_group_name
  use_for_each        = true
  vnet_location       = var.location
  address_space       = var.address_space
  subnet_names        = var.subnet_names
  subnet_prefixes     = var.subnet_prefixes
}
```
---
## Local Modules Directory

```bash
# root/main.tf

# Virtual Network Module
module "vnet-local-module" {
  source              = "./modules/vnet"
  vnet_name           = "local-${var.vnet_name}"
  address_space       = var.address_space
  location            = var.location
  resource_group_name = var.resource_group_name

  public_subnet_name            = var.public_subnet_name
  public_subnet_address_prefix  = var.public_subnet_address_prefix
  private_subnet_name           = var.private_subnet_name
  private_subnet_address_prefix = var.private_subnet_address_prefix
}

## modules/virtual-network/main.tf
# Define a virtual network
resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  address_space       = var.address_space
  location            = var.location
  resource_group_name = var.resource_group_name
}

# Define the public subnets within the virtual network
resource "azurerm_subnet" "public_subnet_1" {
  name                 = var.public_subnet_name
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = var.public_subnet_address_prefix
}

# Define the private subnets within the virtual network
resource "azurerm_subnet" "private_subnet_1" {
  name                 = var.private_subnet_name
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = var.private_subnet_address_prefix
}

# modules/virtual-network/output.tf
output "vnet_id" {
  description = "The ID of the virtual network"
  value       = azurerm_virtual_network.vnet.id
}

output "public_subnet_1_id" {
  description = "The ID of the first public subnet"
  value       = azurerm_subnet.public_subnet_1.id
}

output "private_subnet_1_id" {
  description = "The ID of the first private subnet"
  value       = azurerm_subnet.private_subnet_1.id
}

# modules/virtual-network/variables.tf

variable "vnet_name" {
  description = "The name of the virtual network"
  type        = string
}

variable "address_space" {
  description = "The address space of the virtual network"
  type        = list(string)
}

variable "location" {
  description = "The Azure region where the resources will be created"
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
}

variable "public_subnet_name" {
  description = "The name of the first public subnet"
  type        = string
}

variable "public_subnet_address_prefix" {
  description = "The address prefix of the first public subnet"
  type        = list(string)
}

variable "private_subnet_name" {
  description = "The name of the first private subnet"
  type        = string
}

variable "private_subnet_address_prefix" {
  description = "The address prefix of the first private subnet"
  type        = list(string)
}
```
---
```bash
## root/variables.tf
variable "subscription" {
  default = "subscription_id" /// Add your own subscription_id
}
variable "resource_group_name" {
  description = "resource group name"
  type        = string
  default     = "production-dev"

}

variable "location" {
  description = "This is the resource group location"
  type        = string
  default     = "uksouth"
}

variable "address_space" {
  type    = list(string)
  default = ["10.0.0.0/16"]
}

variable "vnet_name" {
  type    = string
  default = "prodcution-vnet"
}

variable "subnet_names" {
  type    = list(string)
  default = ["subnet1"]
}

variable "subnet_prefixes" {
  type    = list(string)
  default = ["10.0.1.0/24"]
}

variable "public_subnet_name" {
  description = "The name of the public subnet"
  type        = string
  default     = "public-subnet-1"
}

variable "public_subnet_address_prefix" {
  description = "The address prefix of the public subnet"
  type        = list(string)
  default     = ["10.0.1.0/24"]
}

variable "private_subnet_name" {
  description = "The name of the private subnet"
  type        = string
  default     = "private-subnet-1"
}

variable "private_subnet_address_prefix" {
  description = "The address prefix of the private subnet"
  type        = list(string)
  default     = ["10.0.101.0/24"]
}

## root/outputs.tf
# Output for the Azure Resource Group
output "resource_group_name" {
  value = azurerm_resource_group.resource_group_name.name
}

# Outputs for the Public Virtual Network Module
output "vnet_public_name" {
  value = module.vnet-public-module.vnet_name
}

output "vnet_public_subnet_names" {
  value = module.vnet-public-module.subnet_names
}

# Outputs for the Local Virtual Network Module
output "vnet_local_name" {
  value = module.vnet-local-module.vnet_name
}

output "vnet_local_public_subnet_name" {
  value = module.vnet-local-module.public_subnet_name
}
```

