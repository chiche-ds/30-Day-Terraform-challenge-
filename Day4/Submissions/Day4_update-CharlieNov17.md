### Name:Chibuzo Nwobia
### Task: Day 4: Mastering Basic Infrastructure with Terraform
### Date: 8/26/24
### Time: 12:34AM

### Deployment of  Configurable Web Server

I configured the webserver to deploy a webserver using a confiuration which referenced the the variable file where it was stated. Below is the resource block with the referenced configuration `var.server_port`

```
resource "aws_instance" "web_server" {
  ami           = "ami-066784287e358dad1"  
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
```
variable "server_port" {
description = "The port the server will use for HTTP requests"
type = number
default = 80
}

```


