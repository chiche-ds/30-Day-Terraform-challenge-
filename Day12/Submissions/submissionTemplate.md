# Day 12:Zero downtime deplyment using terraform

## Participant Details

- **Name:**
- **Task Completed:**
- **Date and Time:** 

## Terraform Code 
```hcl
Zero-downtime deployment refers to updating a system or application without taking it offline. This is essential for modern applications that require high availability and minimal disruption to users.
Blue/Green Deployment

In blue/green deployment, you have two identical environments: one (blue) that is live, and another (green) where updates are applied. Once the updates are tested and verified on the green environment, traffic is switched from blue to green, ensuring that users never experience downtime.
resource "aws_instance" "blue" {
  ami           = "ami-blue"
  instance_type = "t2.micro"
}

resource "aws_instance" "green" {
  ami           = "ami-green"
  instance_type = "t2.micro"
}
resource "aws_lb" "app_lb" {
  name               = "app-lb"
  load_balancer_type = "application"
  subnets            = ["subnet-12345678", "subnet-87654321"]

  security_groups = ["sg-01234567"]
}

resource "aws_lb_target_group" "blue" {
  name     = "blue-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = "vpc-12345678"
}

resource "aws_lb_target_group" "green" {
  name     = "green-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = "vpc-12345678"
}

Canary Releases

In a canary release, updates are rolled out to a small subset of users before full deployment. If the new version works without issues, the release is gradually expanded to the rest of the users

```
## Architecture 

[Name](link to image in S3 bucket)
