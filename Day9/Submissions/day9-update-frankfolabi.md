# Day 9: Continuing Reuse of Infrastructure with Modules

## Participant Details
- **Name:** Franklin Afolabi
- **Task Completed:** Learnt about advanced concepts of working with modules such as Module Gotchas, Module versioning using git, nested modules, and reusable modules in different environments.
- **Date and Time:** September 8 0510hrs


### Terraform code for live stage
```
# This is the provider block showing the region to be used

provider "aws" {
    region = "us-east-2"
}

# Terraform backend for storing statefile

terraform {
  backend "s3" {
    bucket = "tf-frankfolabi"
    key = "stage/services/webserver-cluster/terraform.tfstate"
    region = "us-east-2"

    dynamodb_table = "tf-locks"
    encrypt = true
  }
}


module "webserver_cluster" {
    source = "github.com/frankfolabi/terraform-up-and-running//challenge/modules/services/webserver-cluster?ref=v0.0.2"
    
    cluster_name = "webservers-stage"
    db_remote_state_bucket = "tf-frankfolabi"
    db_remote_state_key = "stage/data-stores/mysql/terraform.tfstate"

    instance_type = "t2.micro"
    min_size = 2
    max_size = 10
}


resource "aws_security_group_rule" "allow_testing_inbound" {
  type = "ingress"
  security_group_id = module.webserver_cluster.alb_security_group_id

  from_port = 12345
  to_port = 12345
  protocol = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}
