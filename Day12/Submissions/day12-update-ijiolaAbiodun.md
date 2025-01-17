##Zero-Downtime Deployment with Terraform

##In the modules/services/webserver-cluster

//main.tf
resource "aws_launch_configuration" "work" {
  image_id        = var.ami
  instance_type   = var.instance_type
  security_groups = [aws_security_group.instance.id]

  user_data = templatefile("${path.module}/user-data.sh", {
    server_port = var.server_port
    db_address  = data.terraform_remote_state.db.outputs.address
    db_port     = data.terraform_remote_state.db.outputs.ports
    server_text = var.server_text
  })

  lifecycle {
    create_before_destroy = true
  }
}

//user-data.sh 
#!/bin/bash
cat > index.html <<-EOF
<h1>${server_text}</h1>
<p>DB address: ${db_address}</p>
<p>DB port: ${db_port}</p>
nohup busybox httpd -f -p ${server_port} &
EOF

//variable.tf
variable "ami" {
  description = "The AMI to run"
  type        = string
  default     = "ami-0fb653ca2d3203ac1"
}

variable "server_text" {
  description = "The text the web server should return"
  type        = string
  default     = "Welcome to the services webserver"
}

variable "instance_type" {
  description = "The instance type"
  type        = string
  default     = "t2.micro"
}

variable "server_port" {
  description = "The port of the server"
  type        = number
  default     = 8080
}


##In the live/stage/services/webserver
//main.tf
module "webserver_cluster" {
  source = "../../../../modules/services/webserver-cluster"

  ami         = "ami-0fb653ca2d3203ac1"
  server_text = "Welcome to the live webserver"

  cluster_name           = "webserver-live"
  db_remote_state_bucket = "my-bucket-r88r939395d"
  db_remote_state_key    = "stage/data-stores/mysql/terraform.tfstate"

  instance_type      = "t2.micro"
  min_size           = 2
  max_size           = 2
  enable_autoscaling = false
}

