# Day 9: Continuing Reuse of Infrastructure with Modules


## Participant Details

- **Name:** Vijayaraghavan Vashudevan
- **Task Completed:** Learnt -Understanding of Terraform modules and learn how to manage modules across different versions and environments.
- **Date and Time:** 05-09-2024 at 21:41 pm IST

## Terraform Code 
```hcl
module "webserver_cluster" {
  source = "github.com/vjraghavanv/day09-advanced-modules//services/webserver-cluster?ref=v0.0.2"
  cluster_name = "webservers-stage"           
  db_remote_state_bucket = "vj-bucket"
  db_remote_state_key = "stage/data-stores/mysql/terraform.tfstate"    

  instance_type = "t2.micro"
  min_size = 2     
  max_size = 2      
 }

```
 

