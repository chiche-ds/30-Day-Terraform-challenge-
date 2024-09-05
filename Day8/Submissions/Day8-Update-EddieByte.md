# Day 8: Reusing Infrastructure With Modules

## Participant Details
- **Name:** Eddie Chem
- **Task Completed:** All day 8 tasks, including videos from Bryan's Udemy course
- **Date and Time:** 9/01/2024

## File and Folder Isolation Layout (Modules in First Folder)

```hcl
├───.terraform
│   ├───modules
│   │   └───autoscaling
│   │       ├───.github
│   │       │   └───workflows
│   │       └───examples
│   │           └───complete
│   └───providers
│       └───registry.terraform.io
│           └───hashicorp
│               ├───aws
│               │   ├───3.76.1
│               │   │   └───windows_amd64
│               │   ├───4.67.0
│               │   │   └───windows_amd64
│               │   └───5.65.0
│               │       └───windows_amd64
│               ├───http
│               │   └───2.1.0
│               │       └───windows_amd64
│               ├───local
│               │   ├───2.1.0
│               │   │   └───windows_amd64
│               │   └───2.5.1
│               │       └───windows_amd64
│               ├───random
│               │   ├───3.1.0
│               │   │   └───windows_amd64
│               │   └───3.6.2
│               │       └───windows_amd64
│               └───tls
│                   ├───3.1.0
│                   │   └───windows_amd64
│                   └───4.0.5
│                       └───windows_amd64
└───modules
    ├───server
    │   └───.terraform
    │       └───providers
    │           └───registry.terraform.io
    │               └───hashicorp
    │                   └───aws
    │                       └───5.65.0
    │                           └───windows_amd64
    └───web_server
```
## Image - Deployed and Destroyed a VPC with Underlying Components using Terraform Modules
![Deployed a VPC](https://drive.google.com/uc?export=view&id=1sfC_J_ZVa_F-VbtifFqEHOxm3IDldjdl)
