# Day 8: Reusing Infrastructure with Modules

## Participant Details
- **Name:** Dwayne Chima
- **Task Completed:** Reusing Infrastructure with Modules
- **Date and Time:** 9th Dec 2024 5:30pm

## modules/vpc/main.tf
```
# Create a Virtual Private Cloud (VPC)
resource "aws_vpc" "vpc" {
  cidr_block           = var.cidr_block
  instance_tenancy     = "default"
  enable_dns_hostnames = var.dns_hostnames
  tags                 = var.tags
}

# Fetch available AZs in the chosen region
data "aws_availability_zones" "available_azs" {
  state = "available"
}

# Calculate effective AZs and limit based on the region's available AZs
locals {
  effective_azs = min(var.desired_azs, length(data.aws_availability_zones.available_azs.names)) 
  # Slice the list of AZs to match the desired count
  az_list       = slice(data.aws_availability_zones.available_azs.names, 0, local.effective_azs)
}

# Create public subnets, distributing them across available AZs
resource "aws_subnet" "public_subnets" {
  count                   = var.public_subnets_no
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = cidrsubnet(var.cidr_block, 8, count.index) 
  # Ensure subnets are distributed across AZs in a round-robin manner
  availability_zone       = local.az_list[count.index % length(local.az_list)] 
  map_public_ip_on_launch = var.map_public_ip
  tags                    = var.tags
}

# Create an Internet Gateway for external connectivity
resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
  tags   = var.tags
}

# Create a public route table and route internet traffic through the gateway
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
  }

  tags = var.tags
}

# Associate public subnets with the route table
resource "aws_route_table_association" "public_route_table_association" {
  # Loop through subnets to associate each with the route table
  for_each       = { for idx, subnet in aws_subnet.public_subnets : idx => subnet }
  route_table_id = aws_route_table.public_route_table.id
  subnet_id      = each.value.id
}
```

## modules/vpc/vars.tf
```
variable "cidr_block" {
    description = "cidr block for the vpc"
    default = "10.0.0.0/16"
}

variable "dns_hostnames" {
  description = "Enable DNS Hostnames"
  type = string
}

variable "desired_azs" {
    description = "Number of desired Availability Zones"
    type = number
}

variable "public_subnets_no" {
  description = "Number of private subnets needed"
  type = number
}

variable "map_public_ip" {
  description = "To Map Public IP on lauch"
  type = bool
}

variable "inbound_ports" {
  description = "List of ports to allow inbound access."
  type        = list(number)
  default     = [22, 80, 443] # default ports
}


variable "tags" {
  type = map(string)
}
```

## modules/vpc/ouputs.tf
```
# Output the ID of the created VPC
output "vpc_id" {
  value = aws_vpc.vpc.id
}

# Output a list of IDs for the created public subnets
output "subnet_ids" {
  value = [for subnet in aws_subnet.public_subnets : subnet.id]
}
```
## Example of VPC Module Usage
```
module "vpc" {
  source             = "./modules/vpc"
  cidr_block         = "10.0.0.0/16"
  dns_hostnames      = "true"
  desired_azs        = 3
  public_subnets_no  = 3
  map_public_ip      = true
  tags               = {
    Name        = "my-vpc"
    Environment = "dev"
  }
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "subnet_ids" {
  value = module.vpc.subnet_ids
}
```
Explanation of
- **Module Source:** The source attribute points to the path where your module is located ("./modules/vpc").
- **Inputs:** The inputs for the VPC module, such as cidr_block, dns_hostnames, desired_azs, public_subnets_no, and map_public_ip, are passed based on your requirements for the environment.
- **Outputs:** The outputs vpc_id and subnet_ids are captured from the module and can be referenced in the root configuration.

### Additional Notes
- `cidr_block:` Defines the network range for your VPC (e.g., 10.0.0.0/16).
- `dns_hostnames:` Whether to enable DNS hostnames for instances within the VPC.
- `desired_azs:` The number of Availability Zones you want to use for distributing the subnets.
- `public_subnets_no:` The number of public subnets to create.
- `map_public_ip:` Whether to automatically assign public IPs to instances launched in the public subnets.
- `tags:` Tags to apply to resources for identification, which could be customized for your use case.
This configuration will create a VPC with the specified CIDR block, public subnets spread across three Availability Zones, and an Internet Gateway to provide external access.


## Challenges Faced
One of the issues I faced was ensuring that the module could be utilized in a variety of contexts and setups. 
I kept the module adaptable by specifying input variables for the CIDR block, subnet, and availability zone, 
making it simple to adapt to diverse use cases.
