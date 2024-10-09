 # Terraform module for a common infrastructure component (e.g., an EC2 instance, a VPC, or a load balancer).



```hcl
/project-root
  │
  ├──  main.tf
  │
  ├──  modules
  │   ├── VPC
  │   │   ├──  variables.tf
  │   │   ├──  outputs.tf
  │   │   └──  main.tf
  │   │
  │   ├──  EC2
  │   │   ├──  variables.tf
  │   │   ├──  outputs.tf
  │   │   ├──  main.tf
  │   │   ├──  install_nginx.sh
  │   │   └──  do_stuff.sh
  │   │
  │   └──  ALB
  │       ├──  variables.tf
  │       ├──  outputs.tf
  │       └──  main.tf
  │
  ├──  outputs.tf
  └──  variables.tf
```
