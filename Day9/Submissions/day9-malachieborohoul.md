# Day 9: Continuing Reuse of Infrastructure with Modules

## Participant Details

- **Name:** BOROHOUL Soguelni Malachie
- **Task Completed:** I updated my code by splitting it into 2 different filders in other to put in practice what i learned about module versioning. I push the modules to a Github repo and created a release.
- **Date and Time:** 8/29/2024 12:50 PM 

## Terraform Code 
```hcl
#live/stage/services/webserver-cluster

provider "aws" {
  region = "us-east-1"
}

module "webserver_cluster" {
  source                 = "github.com/malachieborohoul/day09-terraform-modules//services/webserver-cluster?ref=v0.0.1"
  cluster_name           = "webservers-stage"
  db_remote_state_bucket = "terraform-bsm-my-state"
  db_remote_state_key    = "stage/data-stores/mysql/terraform.tfstate"
  instance_type = "t2.micro"
  min_size = 2
  max_size = 2
}



```
## Architecture 
[Name](link to image in S3 bucket)

