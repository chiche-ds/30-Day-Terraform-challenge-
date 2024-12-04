# Day4: Mastering Basic Infrastructure with Terraform

### Name: Omekwu Victor Ebube
### Task Completed: Day 4: Mastering Basic Infrastructure with Terraform
### Date: 2nd November, 2024
### Time: 10:20pm

### Deployment of Virtual Network and Subnet

I configured the virtual network and subnet using variables for flexibility, with `var.address_space` for the virtual network and `var.address_prefixes` for the subnet. I also used the `random_id` provider to generate unique IDs for resource names.


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
### variables.tf
```bash
variable "subscription" {
  description = "Subscription ID to use"
  type        = string
  default     = "abcdefghijklmnopqrstuvwxyz" # Replace with your subscription
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