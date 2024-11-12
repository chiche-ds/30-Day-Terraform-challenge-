# Day 9: Continuing Reuse of Infrastructure with Modules

## Participant Details

- **Name:** Omekwu Victor Ebube  
- **Task Completed:** On Day 9, I deepened my understanding of Terraform modules by implementing versioning, adding support for multiple environments (dev, staging, production), and deploying infrastructure using these advanced features. I learned how to structure and manage reusable modules for more complex and scalable infrastructure setups.  
- **Date and Time:** 12-Nov-2024 at 15:30 PM WAT
---
# main.tf
```bash
## Public Module Registry

# Virtual Network Module
module "vnet-public-module" {
  source  = "Azure/vnet/azurerm"
  version = "4.1.0"

  vnet_name           = "public-${var.vnet_name}"
  resource_group_name = var.resource_group_name
  use_for_each        = true
  vnet_location       = var.location
  address_space       = var.address_space
}

## Terraform Azure Storage Public Registry

# Azure Storage Module
module "avm-res-storage-storageaccount" {
  source  = "Azure/avm-res-storage-storageaccount/azurerm"
  version = "0.2.7"
  # insert the 3 required variables here
  resource_group_name       = var.resource_group_name
  location                  = module.vnet-public-module.vnet_location # Nested reference to output from vnet module
  name                      = "ebubevickstorage47"
  account_replication_type  = "LRS"
  account_kind              = "StorageV2"
  shared_access_key_enabled = true

  # Blob Container
  containers = {
    "mycontainer" = {
      name               = "mycontainer"
      public_access      = "Blob"
      versioning_enabled = true
      public_access      = "None"
    }
  }

  # File Share
  shares = {
    "myfileshare" = {
      name  = "myfileshare"
      quota = 10 # Set the quota in GB
      # Optionally, set metadata or other parameters here
    }
  }
}
```
## output.tf
```bash
# This outputs the name of the resource group created using the azurerm_resource_group resource.
output "resource_group_name" {
  value = azurerm_resource_group.resource_group_name.name
}

# Outputs for the Virtual Network Module
# These are nested outputs from the vnet-public-module, which creates the Virtual Network in Azure.
output "vnet_name" {
  value = module.vnet-public-module.vnet_name
}

output "vnet_location" {
  value = module.vnet-public-module.vnet_location
}

# Output for the Storage Account Module
# These are outputs from the avm-res-storage-storageaccount module, which creates the Storage Account in Azure.
output "name" {
  value     = module.avm-res-storage-storageaccount.name
  sensitive = true
}

output "container_info" {
  value = module.avm-res-storage-storageaccount.containers
}
```