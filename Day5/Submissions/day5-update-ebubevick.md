# Day 5: Scaling Infrastructure

## Participant Details

- **Name:** Omekwu Victor Ebube  
- **Task Completed:** On Day 5, I delved into scaling infrastructure using Terraform, focusing on state management, understanding various Terraform blocks, and learning when to apply them for efficient infrastructure scaling.  
- **Date and Time:** 06-11-2024 at 21:30 PM IST  

---
### `provider.tf` - Configures the Azure provider and fetches the existing resource group
```bash
# Azure provider configuration
provider "azurerm" {
  features {}

  # Your Azure subscription ID
  subscription_id = "4bf3e463-ed9f-4148-8906-3eed094e0794" /// Add your own subscription
}

# Fetch an existing resource group instead of creating a new one
data "azurerm_resource_group" "production" {
  name = "production" # Replace with your existing resource group name
}
```
---
### `main.tf` - Defines a virtual network, subnet, public IP, NIC, and virtual machine (VM) resources
```bash
# Define a virtual network
resource "azurerm_virtual_network" "vnet" {
  name                = "production-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = data.azurerm_resource_group.production.location
  resource_group_name = data.azurerm_resource_group.production.name
}

# Define the public subnet
resource "azurerm_subnet" "public_subnet_1" {
  name                 = "public-subnet-1"
  resource_group_name  = data.azurerm_resource_group.production.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Public IP for the VM
resource "azurerm_public_ip" "public_ip_1" {
  name                = "public-ip-1"
  location            = data.azurerm_resource_group.production.location
  resource_group_name = data.azurerm_resource_group.production.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# Network interface for the VM
resource "azurerm_network_interface" "public_nic_1" {
  name                = "public-nic-1"
  location            = data.azurerm_resource_group.production.location
  resource_group_name = data.azurerm_resource_group.production.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.public_subnet_1.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public_ip_1.id
  }
}

# Deploy the public VM
resource "azurerm_virtual_machine" "vm_1" {
  name                  = "public-vm-1"
  location              = data.azurerm_resource_group.production.location
  resource_group_name   = data.azurerm_resource_group.production.name
  network_interface_ids = [azurerm_network_interface.public_nic_1.id]
  vm_size               = "Standard_B1s"

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  storage_os_disk {
    name              = "public-os-disk-1"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = "publicvm1"
    admin_username = "azureuser"
    admin_password = "P@ssw0rd1234!"

    custom_data = <<-EOF
                      #cloud-config
                      package_update: true
                      package_upgrade: true
                      packages:
                        - nginx
                      runcmd:
                        - sudo systemctl start nginx
                        - sudo systemctl enable nginx
                      EOF
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }
}
```
---
### `nsg.tf` - Defines network security group (NSG) for controlling access to VM
```bash
# Network security group for public-facing resources
resource "azurerm_network_security_group" "public_nsg" {
  name                = "public-nsg"
  location            = data.azurerm_resource_group.production.location
  resource_group_name = data.azurerm_resource_group.production.name

  # Allow inbound HTTP traffic on port 80
  security_rule {
    name                       = "allow-http"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Allow inbound HTTPS traffic on port 443
  security_rule {
    name                       = "allow-https"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Allow all outbound traffic
  security_rule {
    name                       = "allow-outbound"
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

# Associate NSG with the public subnet
resource "azurerm_subnet_network_security_group_association" "public_subnet_1_nsg" {
  subnet_id                 = azurerm_subnet.public_subnet_1.id
  network_security_group_id = azurerm_network_security_group.public_nsg.id
}
```
---
### `load-balancer.tf` - Configures a public load balancer to distribute traffic to healthy VMs
```bash
# Public IP for the load balancer
resource "azurerm_public_ip" "public_lb_ip" {
  name                = "public-lb-ip"
  location            = data.azurerm_resource_group.production.location
  resource_group_name = data.azurerm_resource_group.production.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# Load balancer with frontend IP configuration
resource "azurerm_lb" "public_lb" {
  name                = "public-lb"
  location            = data.azurerm_resource_group.production.location
  resource_group_name = data.azurerm_resource_group.production.name
  sku                 = "Standard"

  frontend_ip_configuration {
    name                 = "public-lb-front"
    public_ip_address_id = azurerm_public_ip.public_lb_ip.id
  }
}

# Backend address pool for load balancer
resource "azurerm_lb_backend_address_pool" "public_backend_pool" {
  name            = "public-backend-pool"
  loadbalancer_id = azurerm_lb.public_lb.id
}

# HTTP health probe for load balancer
resource "azurerm_lb_probe" "http_probe" {
  name            = "http-health-probe"
  loadbalancer_id = azurerm_lb.public_lb.id
  protocol        = "Http"
  port            = 80
  request_path    = "/"
}

# Load balancing rule for HTTP traffic
resource "azurerm_lb_rule" "lb_rule" {
  name                           = "lb-rule"
  loadbalancer_id                = azurerm_lb.public_lb.id
  protocol                       = "Tcp"
  frontend_port                  = 80
  backend_port                   = 80
  frontend_ip_configuration_name = "public-lb-front"
  backend_address_pool_ids       = [azurerm_lb_backend_address_pool.public_backend_pool.id]
  probe_id                       = azurerm_lb_probe.http_probe.id
}

# Associate NIC with the backend pool
resource "azurerm_network_interface_backend_address_pool_association" "nic_assoc_1" {
  network_interface_id    = azurerm_network_interface.public_nic_1.id
  ip_configuration_name   = "internal"
  backend_address_pool_id = azurerm_lb_backend_address_pool.public_backend_pool.id
}
```
---
### `output.tf` - Outputs the URL of the load balancer frontend for access
```bash
output "load_balancer_url" {
  description = "The URL of the load balancer frontend."
  value       = "http://${azurerm_public_ip.public_lb_ip.ip_address}"
}
```
