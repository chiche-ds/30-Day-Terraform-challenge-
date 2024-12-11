# Day 10: Terraform Loops and Conditionals

## Participant Details

- **Name:** Dwayne Chima
- **Task Completed:** Use conditionals to deploy resources only when certain conditions are met
- **Date and Time:** 10th Dec 2024 3:30 am


### vars.tf example code
```
variable "instance_count" {
  description = "number of instances"
  type = number
  default = 1
}

variable "create_instance" {
  description = "Flag to determine whether to create the instance"
  type        = bool
  default     = true 
}

variable "subnet_id" {
  description = "List of subnet IDs to distribute instances"
  type = list(string)
  default = ["subnet-12345", "subnet-67890", "subnet-abcde"]
}

variable "inbound_ports" {
  description = "List of ports to allow inbound access."
  type        = list(number)
  default     = [22, 80, 443] # default ports
}

```

### main.tf example code
```
resource "aws_instance" "app" {
  # Conditionally create instances based on create_instance flag, using instance_count for the number of instances
  count = var.create_instance ? var.instance_count : 0

  instance_type          = var.instance_type
  iam_instance_profile = var.instance_profile.id
  ami                   = data.aws_ami.ubuntu.id
  # ensures that Terraform cycles through the subnet IDs in a round-robin fashion.
  subnet_id             = var.subnet_id[count.index % length(var.subnet_id)]
  vpc_security_group_ids = [var.security_group_id]

  user_data = <<-EOT
    #!/bin/bash
    sudo apt update -y
  EOT
}


resource "aws_vpc_security_group_ingress_rule" "allow_tls_ipv4" {
  # Converts the list of inbound ports into a set and creates a rule for each unique port
  for_each          = { for idx, port in toset(var.inbound_ports) : idx => port } 
  security_group_id = aws_security_group.app_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = each.value
  to_port           = each.value
  ip_protocol       = "tcp"
}
```
