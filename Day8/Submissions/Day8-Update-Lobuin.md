```hcl
/project-root
  │
  ├──  main.tf
  │
  ├──  modules
  │   ├── vpc
  │   │   ├──  variables.tf
  │   │   ├──  outputs.tf
  │   │   └──  main.tf
  │   │
  │   ├──  ec2
  │   │   ├──  variables.tf
  │   │   ├──  outputs.tf
  │   │   ├──  main.tf
  │   │   ├──  install_nginx.sh
  │   │   └──  do_stuff.sh
  │   │
  │   └──  sg
  │       ├──  variables.tf
  │       ├──  outputs.tf
  │       └──  main.tf
  │
  ├──  outputs.tf
  └──  variables.tf
```
