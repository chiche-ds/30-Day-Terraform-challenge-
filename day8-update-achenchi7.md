### Creating reusable infrastructure with Terraform Modules

#### Module vpc
```hcl
provider "aws" {
    region = "us-east-1"
}

resource "aws_db_instance" "db-example" {
    identifier_prefix = "terraform-up-and-running"
    engine = "mysql"
    allocated_storage = 10
    instance_class = "db.t2.micro"
    skip_final_snapshot = true
    db_name = var.db_name
    username = var.db_username
    password = var.db_password 
}

```
#### EC2 module
```hcl
provider "aws" {
    region = "us-east-1"
}
module "webserver_cluster" {
    source = "../../../../Project3-modules/modules/services/webserver_cluster"

    cluster_name = var.cluster_name
    db_remote_state_bucket = var.db_remote_state_bucket
    db_remote_state_key = var.db_remote_state_key

    instance_type = "t2.micro"
    min_size = 2
    max_size = 2
}


resource "aws_security_group_rule" "allow_testing_inbound" {
    type = "ingress"
    security_group_id = module.webserver_cluster.alb_security_group_id
    from_port = 12345
    to_port = 12345
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  
}
```