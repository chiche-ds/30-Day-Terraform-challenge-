# Day 18: Automated Testing of Terraform Code

## Participant Details

- **Name:** Omekwu Victor Ebube  
- **Task Completed:** Implemented automated tests (unit, integration, and end-to-end) for Terraform code and integrated them into a CI/CD pipeline.  
- **Date and Time:** 19-November-2024 at 06:30 PM WAT.

---
## Terraform Code
### `main.tf`

```bash
provider "azurerm" {
  features {}
  subscription_id = var.subscription
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}

terraform {
  required_version = ">= 0.12.26"
  required_providers {
    azurerm = {
      version = "~> 2.20"
      source  = "hashicorp/azurerm"
    }
  }
}

# DEPLOY A RESOURCE GROUP
resource "azurerm_resource_group" "resource_group" {
  name     = "terratest-storage-rg"
  location = var.location
}

# DEPLOY A STORAGE ACCOUNT
resource "azurerm_storage_account" "storage_account" {
  name                     = "storage${var.postfix}"
  resource_group_name      = azurerm_resource_group.resource_group.name
  location                 = azurerm_resource_group.resource_group.location
  account_kind             = var.storage_account_kind
  account_tier             = var.storage_account_tier
  account_replication_type = var.storage_replication_type
}

# ADD A CONTAINER TO THE STORAGE ACCOUNT
resource "azurerm_storage_container" "container" {
  name                  = "container1"
  storage_account_name  = azurerm_storage_account.storage_account.name
  container_access_type = var.container_access_type
}

# File Share
resource "azurerm_storage_share" "myfileshare" {
  name                 = "myfileshare"
  storage_account_name = azurerm_storage_account.storage_account.name
  quota                = 10 # Set the quota in GB
}
```
---
## Automated Tests

### `main_test.go`

The test code uses **Terratest** to ensure that the Terraform deployment works correctly. It checks the following:

1. **Storage Account Existence**: Verifies that the storage account is created successfully.
2. **Storage Container**: Checks that the storage container exists.
3. **File Share**: Ensures the file share is created.
4. **Public Access**: Confirms that the storage container is not publicly accessible.

```go
package test

import (
	"fmt"
	"os"
	"strings"
	"testing"

	"github.com/gruntwork-io/terratest/modules/azure"
	"github.com/gruntwork-io/terratest/modules/random"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestTerraformAzureStorage(t *testing.T) {
	t.Parallel()

	// subscriptionID is overridden by the environment variable "ARM_SUBSCRIPTION_ID"
	uniquePostfix := random.UniqueId()

	// Get the environment variables
	subscription := os.Getenv("subscription")
	clientID := os.Getenv("client_id")
	clientSecret := os.Getenv("client_secret")
	tenantID := os.Getenv("tenant_id")

	// Configure Terraform
	terraformOptions := &terraform.Options{
		TerraformDir: "../",
		Vars: map[string]interface{}{
			"subscription":  subscription,
			"client_id":     clientID,
			"client_secret": clientSecret,
			"tenant_id":     tenantID,
			"postfix":       strings.ToLower(uniquePostfix),
		},
	}

	// Cleanup after test
	defer terraform.Destroy(t, terraformOptions)

	// Run `terraform init` and `terraform apply`. Fail the test if there are any errors.
	terraform.InitAndApply(t, terraformOptions)

	// Run `terraform output` to get the values of output variables and sanitize them
	resourceGroupName := strings.TrimSpace(terraform.Output(t, terraformOptions, "resource_group_name"))
	storageAccountName := strings.TrimSpace(terraform.Output(t, terraformOptions, "storage_account_name"))
	storageAccountTier := strings.TrimSpace(terraform.Output(t, terraformOptions, "storage_account_account_tier"))
	storageAccountKind := strings.TrimSpace(terraform.Output(t, terraformOptions, "storage_account_account_kind"))
	storageBlobContainerName := strings.TrimSpace(terraform.Output(t, terraformOptions, "storage_container_name"))
	storageFileShareName := strings.TrimSpace(terraform.Output(t, terraformOptions, "storage_fileshare_name"))

	// Verify storage account properties and ensure it matches the output.
	storageAccountExists := azure.StorageAccountExists(t, storageAccountName, resourceGroupName, subscription)
	assert.True(t, storageAccountExists, "storage account does not exist")

	containerExists := azure.StorageBlobContainerExists(t, storageBlobContainerName, storageAccountName, resourceGroupName, subscription)
	assert.True(t, containerExists, "storage container does not exist")

	fileShareExists := azure.StorageFileShareExists(t, storageFileShareName, storageAccountName, resourceGroupName, "")
	assert.True(t, fileShareExists, "File share does not exist")

	publicAccess := azure.GetStorageBlobContainerPublicAccess(t, storageBlobContainerName, storageAccountName, resourceGroupName, subscription)
	assert.False(t, publicAccess, "storage container has public access")
}
```
---
## Variables
```bash
variable "subscription" {
  description = "Azure subscription ID"
  type        = string
}

variable "client_id" {
  description = "Azure client ID"
  type        = string
}

variable "client_secret" {
  description = "Azure client secret"
  type        = string
  sensitive   = true
}

variable "tenant_id" {
  description = "Azure tenant ID"
  type        = string
}

variable "location" {
  description = "The location to set for the storage account."
  type        = string
  default     = "East US"
}

variable "storage_account_kind" {
  description = "The kind of storage account to set"
  type        = string
  default     = "StorageV2"
}

variable "storage_account_tier" {
  description = "The tier of storage account to set"
  type        = string
  default     = "Standard"
}

variable "storage_replication_type" {
  description = "The replication type of storage account to set"
  type        = string
  default     = "GRS"
}

variable "container_access_type" {
  description = "The replication type of storage account to set"
  type        = string
  default     = "private"
}

variable "postfix" {
  description = "A postfix string to centrally mitigate resource name collisions"
  type        = string
  default     = "resource"
}
```
---
## Outputs
```bash
output "resource_group_name" {
  value = azurerm_resource_group.resource_group.name
}

output "storage_account_name" {
  value = azurerm_storage_account.storage_account.name
}

output "storage_account_account_tier" {
  value = azurerm_storage_account.storage_account.account_tier
}

output "storage_account_account_kind" {
  value = azurerm_storage_account.storage_account.account_kind
}

output "storage_container_name" {
  value = azurerm_storage_container.container.name
}

output "storage_fileshare_name" {
  value = azurerm_storage_share.myfileshare.name
}
```