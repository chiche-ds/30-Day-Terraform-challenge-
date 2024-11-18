# Day 16: Building Production-Grade Infrastructure

## Participant Details

- **Name:** Omekwu Victor Ebube  
- **Task Completed:** Refactored a Terraform project to meet production-grade standards, with a focus on modular design and CI/CD integration.  
- **Date and Time:** 18-November-2024 at 12:30 PM WAT.
---
```markdown
# Production-Grade Infrastructure with Terraform on Azure

This repository contains Terraform configurations for building production-grade infrastructure on Azure. The project follows best practices for modularity, version control, security, and CI/CD integration to manage resources effectively in a production environment.

## Directory Structure

```plaintext
.
├── modules
│   ├── vnet/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   ├── compute/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   ├── storage/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
└── .github/
    └── workflows/
        └── terraform.yml
```

## Terraform Code

### Vnet Module (`modules/vnet/main.tf`)

```bash
resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  location            = var.location
  address_space       = var.address_space
  resource_group_name = var.resource_group_name
}

resource "azurerm_subnet" "prod_subnet" {
  name                 = var.subnet_name
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vent.name
  address_prefixes     = var.subnet_address_prefix
}
```

### Compute Module (`modules/compute/main.tf`)

```bash
resource "azurerm_linux_virtual_machine" "vm" {
  name                = var.vm_name
  resource_group_name = var.resource_group_name
  location            = var.location
  size                = var.vm_size
  admin_username      = var.admin_username
  admin_password      = var.admin_password
  network_interface_ids = [
    azurerm_network_interface.example.id,
  ]
}

resource "azurerm_network_interface" "nic" {
  name                = var.nic_name
  location            = var.location
  resource_group_name = var.resource_group_name
  ip_configuration {
    name                          = "internal"
    subnet_id                     = var.subnet_id
    private_ip_address_allocation = "Dynamic"
  }
}
```

### Main Terraform Configuration (`main.tf`)

```bash
provider "azurerm" {
  features {}
}

module "vpc" {
  source          = "./modules/vnet"
  vnet_name        = "production-vnet"
  location        = "East US"
  address_space   = ["10.0.0.0/16"]
  subnet_name     = "subnet"
  subnet_address_prefix = ["10.0.1.0/24"]
  resource_group_name = "my-resource-group"
}

module "compute" {
  source          = "./modules/compute"
  vm_name         = "production-vm"
  location        = "East US"
  vm_size         = "Standard_DS1_v2"
  resource_group_name = "my-resource-group"
  admin_username  = "adminuser"
  admin_password  = "password"
  subnet_id       = module.vpc.azurerm_subnet.prod_subnet.id
}
```

### Backend Configuration (`terraform.tfvars`)

```bash
resource_group_name = "my-terraform-state-rg"
storage_account_name = "mytfstatestorage"
container_name = "terraform-state"
key = "prod/terraform.tfstate"
```

### GitHub Actions CI/CD Workflow (`.github/workflows/terraform.yml`)

```yaml
name: Terraform Azure CI/CD

on:
  push:
    branches:
      - main

jobs:
  terraform:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Repository
      uses: actions/checkout@v3

    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: "1.5.0"

    - name: Terraform Init
      run: terraform init
      working-directory: ./terraform

    - name: Terraform Plan
      run: terraform plan -out=tfplan
      working-directory: ./terraform

    - name: Terraform Apply
      if: github.ref == 'refs/heads/main' && github.event_name == 'push'
      run: terraform apply -auto-approve tfplan
      working-directory: ./terraform
```

## Getting Started


1. Initialize Terraform:
   ```bash
   terraform init
   ```

2. Plan Terraform:
   ```bash
   terraform plan
   ```

3. Apply the configuration:
   ```bash
   terraform apply
   ```

4. For CI/CD, ensure the GitHub Actions workflow is triggered by pushing to the `main` branch.
