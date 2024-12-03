# Day 3: Deploying Basic Infrastructure with Terraform

## Participant Details

- **Name:** Omekwu Victor Ebube
- **Task Completed:** Learnt - Understanding of Provider block, Resource block, and hands-on of Deployment of web-server using Terraform.
- **Date and Time:** 2nd November 2024 at 10:00 am

### provider.tf
```bash
# Azure provider configuration
provider "azurerm" {
  features {}

  # Your Azure subscription ID
  subscription_id = "subscription" /// Add you own subscription
}

# Define the resource group
resource "azurerm_resource_group" "rg" {
  name = "production-rg"

  # Location of the resource group
  location = "uksouth"
}
```

### Virtual Network 
```bash
# Define a virtual network
resource "azurerm_virtual_network" "vnet" {
  name                = "production-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# Define the first public subnet within the virtual network
resource "azurerm_subnet" "public_subnet_1" {
  name                 = "public-subnet-1"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Define the public IP for the virtual machine
resource "azurerm_public_ip" "public_ip_1" {
  name                = "public-ip-1"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  # Static allocation for the public IP
  allocation_method = "Static"
  sku               = "Standard"
}

# Define the network interface for the virtual machine
resource "azurerm_network_interface" "public_nic_1" {
  name                = "public-nic-1"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  # Network interface IP configuration
  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.public_subnet_1.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public_ip_1.id
  }
}
```

### Networ Security Group
```bash
# Define a network security group for public-facing resources
resource "azurerm_network_security_group" "public_nsg" {
  name                = "public-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

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

# Associate the public NSG with public subnets
resource "azurerm_subnet_network_security_group_association" "public_subnet_1_nsg" {
  subnet_id                 = azurerm_subnet.public_subnet_1.id
  network_security_group_id = azurerm_network_security_group.public_nsg.id
}
```


### main.tf
```bash
# Deploy Public VM
resource "azurerm_virtual_machine" "public_vm_1" {
  name                = "public-vm-1"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  # Associate the VM with the public NIC
  network_interface_ids = [azurerm_network_interface.public_nic_1.id]
  vm_size               = "Standard_B1s"

  # OS image details
  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  # OS disk configuration
  storage_os_disk {
    name              = "public-os-disk-1"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  # VM OS profile
  os_profile {
    computer_name  = "publicvm1"
    admin_username = "azureuser"
    admin_password = "P@ssw0rd1234!" #Not a recommended method for storing keys!!

    # Custom data for VM provisioning
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

  # Linux OS specific profile
  os_profile_linux_config {
    disable_password_authentication = false
  }

  # Tags for resource grouping
  tags = {
    environment = "production"
  }
}
```
