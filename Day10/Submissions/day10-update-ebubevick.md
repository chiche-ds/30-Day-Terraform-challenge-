# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** Omekwu Victor Ebube  
- **Task Completed:** On Day 10, I explored advanced Terraform techniques, including loops (`count` and `for_each`) and conditional expressions. By integrating these features, I refactored my Terraform code for dynamic infrastructure deployments, improving flexibility and reusability.  
- **Date and Time:** 13-Nov-2024 at 1:15 AM WAT
---

## main.tf: for_each and dynamic block for Azure NSG resource
```bash
# Define a network security group for public-facing resources
resource "azurerm_network_security_group" "public_nsg" {
  name                = "public-nsg"
  location            = var.location
  resource_group_name = var.resource_group_name

  # Apply each security rule using for_each
  dynamic "security_rule" {
    for_each = var.public_nsg_rules
    content {
      name                       = security_rule.key
      priority                   = security_rule.value.priority
      direction                  = security_rule.value.direction
      access                     = security_rule.value.access
      protocol                   = security_rule.value.protocol
      source_port_range          = security_rule.value.source_port_range
      destination_port_range     = security_rule.value.destination_port_range
      source_address_prefix      = security_rule.value.source_address_prefix
      destination_address_prefix = security_rule.value.destination_address_prefix
    }
  }
}

# Define a network security group for private-facing resources
resource "azurerm_network_security_group" "private_nsg" {
  name                = "private-nsg"
  location            = var.location
  resource_group_name = var.resource_group_name

  # Apply each security rule using for_each
  dynamic "security_rule" {
    for_each = var.private_nsg_rules
    content {
      name                       = security_rule.key
      priority                   = security_rule.value.priority
      direction                  = security_rule.value.direction
      access                     = security_rule.value.access
      protocol                   = security_rule.value.protocol
      source_port_range          = security_rule.value.source_port_range
      destination_port_range     = security_rule.value.destination_port_range
      source_address_prefix      = security_rule.value.source_address_prefix
      destination_address_prefix = security_rule.value.destination_address_prefix
    }
  }
}
```
## variables.tf: for_each and dynamic block for Azure NSG resource
```bash
# Public NSG Rules
variable "public_nsg_rules" {
  type = map(object({
    priority                   = number
    direction                  = string
    access                     = string
    protocol                   = string
    source_port_range          = string
    destination_port_range     = string
    source_address_prefix      = string
    destination_address_prefix = string
  }))
  default = {
    "allow-http" = {
      priority                   = 1001
      direction                  = "Inbound"
      access                     = "Allow"
      protocol                   = "Tcp"
      source_port_range          = "*"
      destination_port_range     = "80"
      source_address_prefix      = "*"
      destination_address_prefix = "*"
    },
    "allow-https" = {
      priority                   = 1002
      direction                  = "Inbound"
      access                     = "Allow"
      protocol                   = "Tcp"
      source_port_range          = "*"
      destination_port_range     = "443"
      source_address_prefix      = "*"
      destination_address_prefix = "*"
    },
    "allow-outbound" = {
      priority                   = 1003
      direction                  = "Outbound"
      access                     = "Allow"
      protocol                   = "*"
      source_port_range          = "*"
      destination_port_range     = "*"
      source_address_prefix      = "*"
      destination_address_prefix = "*"
    }
  }
}

# Private NSG Rules
variable "private_nsg_rules" {
  type = map(object({
    priority                   = number
    direction                  = string
    access                     = string
    protocol                   = string
    source_port_range          = string
    destination_port_range     = string
    source_address_prefix      = string
    destination_address_prefix = string
  }))
  default = {
    "allow-outbound-internet" = {
      priority                   = 2001
      direction                  = "Outbound"
      access                     = "Allow"
      protocol                   = "Tcp"
      source_port_range          = "*"
      destination_port_range     = "80"
      source_address_prefix      = "*"
      destination_address_prefix = "*"
    }
  }
}
```
---
## main.tf: count loop for Azure VNet Subnet and NSG association
```bash
# Define a Virtual Network (VNet)
resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  address_space       = var.address_space
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# This resource creates multiple subnets within the VNet, defined by a count of 3.
# Each subnet is given a unique address range based on the count index.
resource "azurerm_subnet" "public_subnet" {
  count                = 3
  name                 = "public-subnet-${count.index + 1}"
  address_prefixes     = ["10.0.${count.index}.0/24"]
  resource_group_name  = var.resource_group_name
  virtual_network_name = var.vnet_name
}

# Associate each subnet with the Network Security Group (NSG)
resource "azurerm_subnet_network_security_group_association" "public_nsg_association" {
  count                     = length(azurerm_subnet.public_subnet) # Number of NSG assoc. matches number of subnets.
  subnet_id                 = azurerm_subnet.public_subnet[count.index].id
  network_security_group_id = azurerm_network_security_group.public_nsg.id
}
```
---
## outputs.tf: 
```bash
# Outputs a list of the IDs of the created subnets.
output "public_subnet_ids" {
  value = azurerm_subnet.public_subnet[*].id  # Collects IDs of all created subnets.
}
```
