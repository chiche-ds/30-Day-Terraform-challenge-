# Day 3: Deploying Basic Infrastructure with Terraform

## Participant Details
  - **Name:** Patrick Odhiambo
## Tasks Completed

- **Watched the required video**
  - Gained foundational knowledge on setting up and managing AWS infrastructure using Terraform IaC.
  
- **Designed the architecture for the web server**
  - Utilized **draw.io** to create a clear and structured diagram of the web server architecture.

- **Set up a basic web server on AWS using Terraform IaC**
  - Spun up a free-tier **Ubuntu instance** on AWS.

- **Configured the infrastructure in the `Main.tf` script file using VSCode**
  - Created and managed the Terraform script to define and provision the necessary resources for the web server.

- **Blog and Social Media**

-Wrote an article titled "" and hosted it on my blog at Dev.to
- Updated my progress on social media by tweeting on X

- **Terraform Code**


provider  "aws" {
    region = "us-east-1"
}

resource "aws_instance" "My-Ec2instance" {
 ami = "ami-0e86e20dae9224db8" #Ubuntu 20.04 LTS
 instance_type = "t2.micro"
 vpc_security_group_ids = [aws_security_group.instance.id]


 user_data = <<-EOF
             #!/bin/bash
             echo "Hello, World" > index.html
             nohup busybox httpd -f -p 8080 &
                 

                  EOF
             user_data_replace_on_change = true
 tags = {
    Name = "Terraform-Instance"
 }
}

resource "aws_security_group" "instance" {
 name = "terraform-SG-instance"
 ingress {
 from_port = 8080
 to_port = 8080
 protocol = "tcp"
 cidr_blocks = ["0.0.0.0/0"]
 }
}
 #### **Date and Time:** 3/09/2024 4:10 PM