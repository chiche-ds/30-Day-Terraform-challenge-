
# Day4: Mastering Basic Infrastructure with Terraform

### Name: Adaeze Nnamdi-Udekwe
### Task Completed: Day 4: Mastering Basic Infrastructure with Terraform
### Date: 8/20/24
### Time: 8:30pm

### Deployment of  Configurable Web Server

I configured the webserver to deploy a webserver using a confiuration which referenced the the variable file where it was stated. Below is the resource block with the referenced configuration `var.server_port`

```hcl
resource "aws_launch_configuration" "example" {
image_id = "ami-04a81a99f5ec58529"
instance_type = "t2.micro"
security_groups = [aws_security_group.instance.id]
user_data = <<-EOF
#!/bin/bash
echo "Hello, World" > index.html
nohup busybox httpd -f -p ${var.server_port} &
EOF
}
```

`variable.tf` where the webserver referenced.
```hcl
variable "server_port" {
description = "The port the server will use for HTTP requests"
type = number
default = 8080
}


