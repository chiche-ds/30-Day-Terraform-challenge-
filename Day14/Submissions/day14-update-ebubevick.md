#  Day 14: Working with Multiple Providers - Part 1

## Participant Details

- **Name:** Omekwu Victor Ebube  
- **Task Completed:** Worked on deploying resources using multiple providers with aliases in Terraform.  
- **Date and Time:** 17-November-2024 at 12:50 AM WAT
---

## main.tf : This is where the main resources and provider configurations are declared
```bash
# Declare required providers
terraform {
  required_providers {
    # Azure Resource Manager provider for managing Azure resources
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.70"
    }

    # TLS provider for generating and managing TLS certificates
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
  }
}

# Configure the Azure provider 
provider "azurerm" {
  features {}
  subscription_id = var.subscription

  # Alias for the East US region
  alias = "eastus"
}

# Resource Group in UK South
resource "azurerm_resource_group" "rg_uksouth" {
  provider = azurerm.eastus
  name     = var.rg_uksouth
  location = var.location
}

# Storage Account in East US
resource "azurerm_storage_account" "storage_uksouth" {
  provider                 = azurerm.eastus
  name                     = var.uksouth_storage_acct
  resource_group_name      = azurerm_resource_group.rg_uksouth.name
  location                 = azurerm_resource_group.rg_uksouth.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# TLS provider generates a self-signed certificate
resource "tls_private_key" "my_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "tls_self_signed_cert" "my_cert" {
  private_key_pem       = tls_private_key.my_key.private_key_pem
  allowed_uses          = ["key_encipherment", "digital_signature"]
  validity_period_hours = 760
  is_ca_certificate     = false
}

```
---
## outputs.tf : This file contains the outputs to verify and retrieve resource details
```bash
# Output the name of the Storage Account created in UK South
output "uksouth_storage_account_name" {
  value = azurerm_storage_account.storage_uksouth.name
}

# Output the certificate details
output "certificate_pem" {
  value = tls_self_signed_cert.my_cert.cert_pem
}

# Output the private key, marked as sensitive
output "private_key_pem" {
  sensitive = true
  value     = tls_private_key.my_key.private_key_pem
}

```