## Deploying a Single EC2 Instance on AWS Using Terraform

This guide will walk you through deploying a single EC2 instance on AWS using Terraform. The instance will serve a simple web page using a minimal HTTP server.

### 1. Provider Configuration

Create a file named `main.tf` and add the following configuration to specify the AWS provider:

```hcl
provider "aws" {
  region = "us-east-2"
}
```

### 2. Security Group
a security group configuration to allow inbound traffic on port 8080:

```hcl
resource "aws_security_group" "instance" {
  name        = "terraform-example-instance"
  description = "Allow inbound traffic on port 8080"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### 3. EC2 Instance
Add the EC2 instance configuration with user data to run a minimal HTTP server:

```hcl
resource "aws_instance" "example" {
  ami                    = "ami-0fb653ca2d3203ac1"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.instance.id]

  user_data = <<-EOF
    #!/bin/bash
    echo "Hello, World" > index.html
    nohup busybox httpd -f -p 8080 &
    EOF

  user_data_replace_on_change = true
  tags = {
    Name = "terraform-example"
  }
}
```

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/p3nneg916u72sjdxjvuu.png)
![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/3imnw2wxotbfvsalhnam.png)
