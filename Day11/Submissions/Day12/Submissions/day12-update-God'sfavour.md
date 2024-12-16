### Name: God'sfavour Braimah
### Task: Day 12 Zero-Downtime Deployment with Terraform
### Date: 12/16/24
### Time: 10:15pm
### Activity
# Zero-Downtime Deployment with Terraform

## Overview
This project demonstrates how to implement zero-downtime deployments using Terraform. By leveraging techniques like **blue/green deployments** and **load balancers**, we can update web application infrastructure without service interruptions. This is critical for applications requiring high availability and minimal downtime.

---

## Features
- **Blue/Green Deployment**: Deploy infrastructure updates in a separate environment (green) while keeping the current environment (blue) live.
- **AWS Elastic Load Balancer (ELB)**: Route traffic seamlessly between environments.
- **Auto Scaling Groups**: Ensure scalability and high availability.
- **Terraform Variables**: Dynamically manage environments and configurations.

---

## File Structure
```plaintext
.
├── main.tf       # Core configuration for resources (ELB, ASGs, Launch Configurations)
├── variables.tf  # Input variables for flexibility
├── provider.tf   # AWS provider configuration
├── outputs.tf    # Outputs for monitoring results
```

---

## Prerequisites
- **Terraform** installed on your machine.
- **AWS CLI** configured with valid credentials.
- Basic understanding of Terraform commands (`init`, `plan`, `apply`, `destroy`).

---

## Input Variables

### `variables.tf`
```hcl
variable "environment" {
  description = "Active environment (blue or green)"
  type        = string
  default     = "blue"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instances"
  type        = string
  default     = "ami-0abcdef1234567890" # Replace with your AMI ID
}

variable "instance_type" {
  description = "Type of EC2 instance"
  type        = string
  default     = "t2.micro"
}
```

---

## Core Configuration

### `main.tf`
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_elb" "app_elb" {
  name               = "web-app-lb"
  availability_zones = ["us-east-1a", "us-east-1b"]

  listener {
    instance_port     = 80
    instance_protocol = "HTTP"
    lb_port           = 80
    lb_protocol       = "HTTP"
  }

  health_check {
    target              = "HTTP:80/"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_autoscaling_group" "blue_asg" {
  count              = var.environment == "blue" ? 1 : 0
  launch_configuration = aws_launch_configuration.blue_lc.id
  desired_capacity    = 2
  min_size            = 1
  max_size            = 3
  load_balancers      = [aws_elb.app_elb.name]
}

resource "aws_launch_configuration" "blue_lc" {
  name          = "blue-lc"
  image_id      = var.ami_id
  instance_type = var.instance_type

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "green_asg" {
  count              = var.environment == "green" ? 1 : 0
  launch_configuration = aws_launch_configuration.green_lc.id
  desired_capacity    = 2
  min_size            = 1
  max_size            = 3
  load_balancers      = [aws_elb.app_elb.name]
}

resource "aws_launch_configuration" "green_lc" {
  name          = "green-lc"
  image_id      = var.ami_id
  instance_type = var.instance_type

  lifecycle {
    create_before_destroy = true
  }
}
```

---

## Outputs

### `outputs.tf`
```hcl
output "active_environment" {
  value       = var.environment
  description = "The currently active environment (blue or green)"
}

output "elb_dns" {
  value       = aws_elb.app_elb.dns_name
  description = "DNS of the Load Balancer"
}
```

---

## Deployment Steps

1. **Initialize Terraform**:
   ```bash
   terraform init
   ```

2. **Plan the Deployment**:
   ```bash
   terraform plan
   ```

3. **Deploy the Blue Environment**:
   ```bash
   terraform apply -var="environment=blue"
   ```

4. **Switch to the Green Environment**:
   - Update the `environment` variable to `green`.
   - Apply the changes:
     ```bash
     terraform apply -var="environment=green"
     ```

5. **Verify Deployment**:
   - Open the Load Balancer DNS in your browser (from the output).
   - Confirm traffic switches seamlessly between environments.

6. **Cleanup**:
   ```bash
   terraform destroy
   ```

---

## Key Notes
- **Blue/Green Deployment** ensures seamless updates by running two environments and switching traffic.
- **Load Balancer** manages traffic and ensures zero downtime during transitions.
- Terraform’s `count` feature dynamically controls which environment is active.

---

## Conclusion
This project showcases how to implement zero-downtime deployments with Terraform. It’s an essential skill for managing infrastructure updates in production environments. Let me know if you have questions or need further assistance!
