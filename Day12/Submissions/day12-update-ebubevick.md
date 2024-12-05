# Day 12: Zero-Downtime Deployment with Terraform

## Participant Details

- **Name:** Omekwu Victor Ebube  
- **Task Completed:** Focused on zero-downtime deployments with Terraform, utilizing blue/green deployment techniques to maintain continuous availability during updates.  
- **Date and Time:** 14-November-2024 at 2:40 PM WAT
---
## main.tf
```bash
# Blue Environment - Current Production
resource "azurerm_app_service" "blue" {
  name                = "myapp-blue"
  resource_group_name = var.resource_group
  location            = var.location
}

# Green Environment - Staging for Update
resource "azurerm_app_service" "green" {
  name                = "myapp-green"
  resource_group_name = var.resource_group
  location            = var.location
}

## configuration for setting up a blue/green deployment:

resource "azurerm_application_gateway" "app_gateway" {
  # Name of the Application Gateway
  name                = "my-app-gateway"
  resource_group_name = var.resource_group
  location            = var.location

  # Backend pool for the current stable production version (blue environment)
  backend_address_pool {
    name        = "blue-backend"
    ip_addresses = [azurerm_app_service.blue.default_site_hostname] # IP for the blue App Service
  }

  # Backend pool for the new version in staging (green environment)
  backend_address_pool {
    name        = "green-backend"
    ip_addresses = [azurerm_app_service.green.default_site_hostname] # IP for the green App Service
  }
}
```