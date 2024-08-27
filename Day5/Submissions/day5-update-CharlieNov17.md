# Day5: Scaling Infrastructure

## Participant Details
- **Name:** Chibuzo Nwobia
- **Task Completed:**  Scaled A web server using terraform using auto scaling groups
- made a social media post, drew a table comparing the vairous terraform blocks with sample codes
- looked at the princple of terraform state files its importance and and how to manage it 
-  
- **Date and Time:** 8/27/2024 02:34 AM

### This is the `main.tf` with all the configurations  
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_launch_configuration" "web_launch_config" {
  name          = "web-launch-config"
  image_id      = "ami-023508951a94f0c71"  # Replace with your desired AMI ID
  instance_type = "t2.micro"

  user_data = <<-EOF
              #!/bin/bash
              echo "Hello, World! Chibuzo Terraform Test page join me!! " > index.html
              nohup python -m SimpleHTTPServer 80 &
              EOF

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "web_asg" {
  desired_capacity     = 2
  max_size             = 8
  min_size             = 1
  launch_configuration = aws_launch_configuration.web_launch_config.id
  vpc_zone_identifier  = ["subnet-097f4151f3d2350a4", "subnet-0f60b5b162197cce9"]  # Replace with your subnet ID

  tag {
    key                 = "Name"
    value               = "web-server"
    propagate_at_launch = true
  }

  target_group_arns = [aws_lb_target_group.web_tg.arn]
}

resource "aws_lb" "web_lb" {
  name               = "web-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = ["sg-0797e0cb989439026"]  # Replace with your security group ID
  subnets            = ["subnet-097f4151f3d2350a4", "subnet-0f60b5b162197cce9"]  # Replace with your subnet ID
}

resource "aws_lb_target_group" "web_tg" {
  name     = "web-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = "vpc-05d9133f631b4ec97"  # Replace with your VPC ID
}

resource "aws_lb_listener" "web_listener" {
  load_balancer_arn = aws_lb.web_lb.arn
  port              = "80"
  protocol          = "HTTP"

# Return a 404 page if the target is not healthy
  default_action {
    type             = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "404: Resource Not Found"
      status_code  = "404"
    }
  }
}

output "load_balancer_dns" {
  value = aws_lb.web_lb.dns_name
}
```


### 
### 3. **Comparison Table of Terraform Blocks**

| Block Type             | Description                                                                                           | Use Case                                     | Code Sample                                               |
|------------------------|-------------------------------------------------------------------------------------------------------|---------------------------------------------|------------------------------------------------------------|
| `provider`             | Configures the provider (e.g., AWS, GCP) for your infrastructure.                                      | Set up the cloud provider configuration.    | `provider "aws" { region = "us-west-2" }`                  |
| `resource`             | Defines a specific infrastructure component (e.g., EC2 instance, S3 bucket).                           | Create and manage infrastructure resources. | `resource "aws_instance" "web" { ami = "ami-1234" }`       |
| `output`               | Exports information about your resources (e.g., instance IPs).                                         | Retrieve useful values after deployment.    | `output "instance_ip" { value = aws_instance.web.public_ip }` |
| `variable`             | Allows you to define input variables for your configuration.                                           | Parameterize your configuration.            | `variable "instance_type" { default = "t2.micro" }`        |
| `module`               | Encapsulates a set of resources and configurations into reusable units.                                | Reuse configurations across projects.       | `module "vpc" { source = "./modules/vpc" }`                |
| `data`                 | Fetches data from external sources (e.g., AMI IDs, existing resources).                               | Query data from other resources.            | `data "aws_ami" "ubuntu" { most_recent = true }`           |
| `locals`               | Defines local variables for your Terraform configuration.                                              | Simplify complex expressions.               | `locals { instance_count = 3 }`                            |
| `terraform`            | Specifies backend and other Terraform-related settings.                                                | Configure Terraform's settings.             | `terraform { backend "s3" { bucket = "mybucket" } }`       |
| `output`               | Exports information for other resources, scripts, or external tools to consume.                        | Provide useful data for other systems.      | `output "elb_dns" { value = aws_elb.web.dns_name }`        |
| `provisioner`          | Executes scripts or commands on resources after creation or destruction.                               | Configure resources post-deployment.        | `provisioner "local-exec" { command = "echo Hello" }`      |
| `backend`              | Configures where the Terraform state file is stored (e.g., local, S3).                                 | Manage state files across environments.     | `terraform { backend "s3" { bucket = "state-bucket" } }`   |
