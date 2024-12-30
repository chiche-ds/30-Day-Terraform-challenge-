# Day4: Mastering Basic Infrastructure with Terraform

### Name: God'sfavour Braimah
### Task Completed: Day 4: Mastering Basic Infrastructure with Terraform
### Date: 12/5/24
### Time: 11:40pm

# Day 4: Mastering Basic Infrastructure with Terraform  

## Overview  
On Day 4 of the Terraform 30-Day Challenge, I focused on creating reusable and efficient infrastructure code by leveraging Terraform variables. This approach simplifies updates, reduces redundancy, and adheres to the **"DRY"** principle.  

---

## Tasks for the Day  

### 1. Reading  
- **Chapter**: Chapter 2 of *Terraform: Up & Running* by Yevgeniy Brikman.  
- **Pages**: 60 - the first part of page 70.  
- **Goal**: Understand Terraform's **"DRY"** principle and learn how to write reusable infrastructure code.  

---

### 2. Videos  
#### **Udemy Videos Rewatched**:  
- Day 3 videos: Videos 11, 12, and 13  
- Video 17: **Input Variables**  
- Video 18: **Local Variables**  

#### **Goal**:  
- Learn how to use **input variables** and **local variables** in Terraform for flexibility and reusability.  

---

### 3. Activities  

#### **Configurable Web Server**  
Deployed a configurable web server using variables to customize:  
- AWS region  
- AMI ID  
- Instance type  

#### **Clustered Web Server**  
Deployed a clustered web server with multiple instances, using variables for:  
- Server count  
- Security group configuration  
- Networking rules  

#### **Explore Documentation**  
Dived into Terraform's documentation on:  
- Providers  
- Resource blocks  
- Input/Output variables  

---

## Terraform Code  

### **Variables Definition** (`variables.tf`)  

```hcl
variable "aws_region" {
  default = "us-east-1"
}

variable "security_group_name" {
  default = "web_server_sg"
}

variable "ingress_from_port" {
  default = 80
}

variable "ingress_to_port" {
  default = 80
}

variable "ingress_protocol" {
  default = "tcp"
}

variable "ingress_cidr_blocks" {
  default = ["0.0.0.0/0"]
}

variable "egress_from_port" {
  default = 0
}

variable "egress_to_port" {
  default = 0
}

variable "egress_protocol" {
  default = "-1"
}

variable "egress_cidr_blocks" {
  default = ["0.0.0.0/0"]
}

variable "server_count" {
  default = 3
}

variable "ami_id" {
  default = "ami-0453ec754f44f9a4a" # Amazon Linux 2
}

variable "instance_type" {
  default = "t2.micro"
}
```

## **Main Configuration** (`main.tf`)
```hcl
provider "aws" {
  region = var.aws_region
}

resource "aws_security_group" "web_server_sg" {
  name = var.security_group_name

  ingress {
    from_port   = var.ingress_from_port
    to_port     = var.ingress_to_port
    protocol    = var.ingress_protocol
    cidr_blocks = var.ingress_cidr_blocks
  }

  egress {
    from_port   = var.egress_from_port
    to_port     = var.egress_to_port
    protocol    = var.egress_protocol
    cidr_blocks = var.egress_cidr_blocks
  }
}

resource "aws_instance" "web_server" {
  count = var.server_count
  ami   = var.ami_id
  instance_type = var.instance_type
  vpc_security_group_ids = [aws_security_group.web_server_sg.id]

  user_data = <<-EOF
    #!/bin/bash
    sudo yum update -y
    sudo yum install -y httpd
    sudo systemctl start httpd
    sudo systemctl enable httpd
    echo "Hello from server instance ${count.index + 1}" > /var/www/html/index.html
  EOF

  tags = {
    Name = "Clustered_Web_Server_${count.index + 1}"
  }
}
```
## Highlights
DRY Principle
By defining variables, I eliminated redundancy and made the code reusable for different configurations.
Updates can be made by changing variable values without editing the main Terraform files.

## Key Learnings
Input variables enhance flexibility.
Infrastructure configurations can be parameterized for scalable deployment.
