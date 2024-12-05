# Day 13: Managing Sensitive Data in Terraform

## Participant Details

- **Name:** Omekwu Victor Ebube  
- **Task Completed:** Secured sensitive data using Azure Key Vault, integrated it with Terraform, and implemented best practices for handling secrets in code.  
- **Date and Time:** 15-November-2024 at 7:30 PM WAT
---

## 
```bash
# Configure the Azure provider
provider "azurerm" {
  features {}
  subscription_id = var.subscription
}

resource "azurerm_resource_group" "resource_group_name" {
  name     = var.resource_group_name
  location = var.location
}

data "azurerm_client_config" "current" {}

# Key Vault with security best practices
resource "azurerm_key_vault" "keyvault" {
  name                       = "day13KeyVault"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  purge_protection_enabled   = true
  soft_delete_retention_days = 90

  # Access policy for Terraform user with key and secret management permissions
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    key_permissions = [
      "Create",
      "Import",
      "Delete",
      "Get",
      "List",
      "Update",
      "Restore",
      "Purge"
    ]

    secret_permissions = [
      "Get",
      "List",
      "Set",
      "Delete",
      "Recover",
      "Backup",
      "Restore",
      "Purge"
    ]
  }
}

# Creating a Key in Azure Key Vault
resource "azurerm_key_vault_key" "key" {
  name         = "my-key"
  key_vault_id = azurerm_key_vault.keyvault.id
  key_type     = "RSA" # Specify the type of the key (RSA, EC, etc.)
  key_size     = 2048  # The size of the key (only applicable to RSA keys)
  key_opts = ["decrypt", "encrypt", "sign", "verify"] # Key operations (options like decrypt, encrypt, etc.)
}

# Storing a secret in Key Vault
resource "azurerm_key_vault_secret" "secret" {
  name         = "my-secret"
  value        = var.secret_value
  key_vault_id = azurerm_key_vault.keyvault.id
}

# External data block to read the secret from a local file (secret.json)
data "external" "secret" {
  program = ["sh", "-c", "cat ./secret.json"]
}

# Create a secret in the Azure Key Vault from the fetched data
resource "azurerm_key_vault_secret" "my_secret" {
  name         = "mySecretAPIKey"
  value        = data.external.secret.result.my_secret_value
  key_vault_id = azurerm_key_vault.keyvault.id
}
```
---
### variables.tf (Sensitive Variable Definitions)
```bash
variable "subscription" {
  description = "The Azure subscription ID"
  type        = string
  default     = "add-ur-subscription-id"
}

variable "resource_group_name" {
  description = "The name of the resource group"
  default     = "production-rg"
}

variable "location" {
  description = "Azure location for resources"
  default     = "uksouth"
}

variable "secret_value" {
  description = "A sensitive secret value"
  type        = string
  sensitive   = true
}
```
---
## Output (sensitive output should not display secret values)
```bash
output "key_vault_name" {
  value       = azurerm_key_vault.keyvault.name
  description = "The name of the created Key Vault"
}

output "secret_id" {
  value       = azurerm_key_vault_secret.secret.id
  description = "The ID of the stored secret"
}

# Output the secret URI from the Key Vault for later use
output "secret_uri" {
  value = azurerm_key_vault_secret.my_secret.id
}

output "key_id" {
  value       = azurerm_key_vault_key.key.id
  description = "The ID of the created Key"
}
```
---
## terraform.tfvars: This file contains the values for variables defined in the Terraform configuration.
```bash
# Security Tip: Add terraform.tfvars to .gitignore to prevent it from being committed to version control.
secret_value = "this is our important secret here"  # Example secret value to be securely handled by Terraform

```
---
## secret.json: This file contains the sensitive data (e.g., API keys or passwords) 
```bash
## It is read by Terraform using an external data source.
{
    "my_secret_value": "my-super-special-secret-value"
}

```
