## Day 4 Task : Mastering Basic Infrastructure with Terraform
_Utibe Okon | Wed, August 22 2024 | 2:29 AM - GMT+1_

__Deploying a cluster of webservers:__ Previously, I got to deploy a webserver using terraform. WHile it was a good starting point, it is rarely ever the case in real life as a single server is not ideal to ensure continous accessibility. So here, I will deploy a cluster of servers using AWS auto scalling groups. To acheive this, two resources are needed, the auto scaling groups and launch configuration where it uses to add servers. The following configuration allows aws to scale our servers up to 10 in times of high demand and ascale down to 2 when there is less request. Essentially, a load balancer is also deployed to route traffic to all the servers, but that is not included in the code sample for now.

```hcl
resource "aws_launch_configuration" "example" {
    image_id = "ami-0fb653ca2d3203ac1"
    instance_type = "t2.micro"
    security_groups = [aws_security_group.instance.id]
    user_data = <<-EOF
    #!/bin/bash
    echo "Hello, World" > index.html
    nohup busybox httpd -f -p ${var.server_port} &
    EOF
}

resource "aws_autoscaling_group" "example" {
    launch_configuration = aws_launch_configuration.example.name
    min_size = 2
    max_size = 10
    tag {
        key = "Name"
        value = "terraform-asg-example"
        propagate_at_launch = true
    }
}
```