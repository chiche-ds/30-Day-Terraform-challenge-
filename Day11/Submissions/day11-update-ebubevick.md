# Day 11: Terraform Conditionals

## Participant Details

- **Name:** Omekwu Victor Ebube  
- **Task Completed:** On Day 11, I focused on mastering loops and conditional logic in Terraform. I refactored my Terraform configurations to include conditional logic, which allowed me to dynamically configure environment-specific settings like IP addresses and outbound access based on the env variable. This added flexibility to my infrastructure code and made it adaptable to different environments such as prod and dev.  
- **Date and Time:** 14-November-2024 at 10:30 AM WAT
---
## main.tf
```bash
# Virtual Network creation
resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name           
  resource_group_name = var.resource_group_name 
  location            = var.location            
  address_space       = var.address_space       

  depends_on = [azurerm_resource_group.resource_group_name] # VNet depends on the resource group
}

# Subnet creation for different environments (prod, dev)
resource "azurerm_subnet" "vnet_subnet" {
  for_each                        = var.env               # Loop through the environments
  
  name                            = lower(each.key)      # Convert environment name to lowercase for subnet name
  resource_group_name             = upper(var.resource_group_name) # Uppercase for consistency
  virtual_network_name            = upper(var.vnet_name)          # Uppercase for consistency
  address_prefixes                = each.value.ip         # Set the subnet's IP range
  default_outbound_access_enabled = each.value.outbound_access # Enable or disable outbound access

  depends_on = [azurerm_virtual_network.vnet] 
}

locals {
  start_time     = timestamp()  # Current timestamp
  end_time       = timeadd(local.start_time, "${var.expiry_days * 24}h")  # Calculate end time
  formatted_date = formatdate("YYYY-MM-DD hh:mm:ss AA", local.end_time)  # Format the end time
}
```
## variables.tf
```bash
# Defines the location for resources
variable "location" {
  default = "uksouth" 
}

# Specifies the address space for the virtual network
variable "address_space" {
  type    = list(string)           # Type is a list of strings (CIDR blocks)
  default = ["10.0.0.0/16"]        # Default address space is 10.0.0.0/16
}

# Name of the virtual network
variable "vnet_name" {
  type    = string           
  default = "production-vnet"
}

# Defines environment-specific configurations (prod, dev)
variable "env" {
  type = map(any)  # Type is a map where the key is a string (env name), and the value is a map with 'ip' and 'outbound_access'
  default = {
    prod = {
      ip              = ["10.0.150.0/24"] 
      outbound_access = false             # No outbound access in prod
    }
    
    dev = {
      ip              = ["10.0.250.0/24"] 
      outbound_access = true              # Outbound access enabled in dev
    }
  }
}

# Expiry time configuration
variable "expiry_days" {
  type    = number
  default = 7  # Default expiry is set to 7 days
}
```
## output.tf
```bash
# Use join to create a more readable string with labels for each part
output "readable_dates" {
  description = "A readable format for start and end times"
  value       = join(" | ", [
    "Start Time: ${local.start_time}",
    "Formatted End Date: ${local.formatted_date}"
  ])
}
```