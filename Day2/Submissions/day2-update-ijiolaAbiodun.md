# Day 2: Setting Up Terraform

## Task Description

### **1. Reading**
- Chapter 2 of *Terraform: Up & Running* by Yevgeniy (Jim) Brikman:
  - "Setting Up Your AWS Account"
  - "Installing Terraform"
  - "Deploying the First Two Servers"

### **2. Udemy Videos**
Watch the following videos:
- **Video 7**: "Setting Up Your AWS Account"
- **Video 8**: "Installing Terraform"
- **Video 9**: "First Steps with Terraform"
- **Video 10**: "Understanding the Terraform Workflow"
- *(Ensure you have completed Video 6 if not already done)*

### **3. Activity**
- Set up your AWS account.
- Install Terraform locally.
- Install AWS CLI and configure it.
- Install Visual Studio Code (VSCode) and add the AWS plugin.
- Configure your VSCode to work with AWS.
- Deploy a single server and a web server as outlined in Chapter 2.

### **4. Blog Post**
Write a blog post: "Step-by-Step Guide to Setting Up Terraform, AWS CLI, and Your AWS Environment."

### **5. Social Media Post**
Share your progress on social media:
```
💻 Just installed Terraform, AWS CLI, and configured my AWS environment with VSCode. Ready to deploy some infrastructure! #TerraformSetup #AWS #DevOps
```

---

## Deliverables

- Update the `daily-update.md` file with:
  - Your name Ijiola Abiodun Usman
  - Tasks completed 
  - Date: 3rd of December, 2024
  - Time: 03:45 PM
- Write and publish a blog post detailing your setup process. 
- Share your progress on social media with the required hashtags.

---

## Terraform Configuration Example

### **Provider Configuration**
```hcl
provider "aws" {
    region = "us-east-1"
}
```

### **Single Server Resource**
```hcl
resource "aws_instance" "single_server" {
    ami           = "ami-0fb653ca2d3203ac1"
    instance_type = "t2.micro"
}
```

### **Web Server Resource**
```hcl
resource "aws_instance" "terraform-web_server-instance" {
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
        Name = "terraform-web-server-instance"
    }
}
```

### **Security Group Configuration**
```hcl
resource "aws_security_group" "terraform-web-server-instance" {
    name = "terraform-web-server-instance"

    ingress {
        from_port   = 8080
        to_port     = 8080
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}
```

