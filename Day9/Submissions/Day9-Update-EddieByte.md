# Day 9: Continuing Reuse of Infrastructure with Modules

## Participant Details

- **Name:** Eddie Chem
- **Task Completed:** All tasks for day 9, including videos and labs from Bryan's Udemy course
- **Date and Time:** 9/02/2024 10:39 PM

## File and Folder Isolation Layout (Modules in First Folder)

This Terraform directory structure includes several modules and provider files, organized into `.terraform/modules` and `.terraform/providers` directories. The `modules` directory contains subdirectories for different modules: `autoscaling`, `s3-bucket`, and `vpc`. Each module has its own structure, including `.github` workflows, `examples`, and various nested submodules.This setup indicates a well-organized Terraform workspace that supports various infrastructure components, such as autoscaling groups, S3 buckets, and VPCs, along with provider binaries needed for deployment.

```hcl
└───.terraform
    ├───modules
    │   ├───autoscaling
    │   │   ├───.github
    │   │   │   └───workflows
    │   │   └───examples
    │   │       └───complete
    │   ├───s3-bucket
    │   │   ├───.github
    │   │   │   └───workflows
    │   │   ├───examples
    │   │   │   ├───complete
    │   │   │   ├───notification
    │   │   │   ├───object
    │   │   │   └───s3-replication
    │   │   ├───modules
    │   │   │   ├───notification
    │   │   │   └───object
    │   │   └───wrappers
    │   │       ├───notification
    │   │       └───object
    │   └───vpc
    │       ├───.chglog
    │       ├───.github
    │       │   └───workflows
    │       ├───examples
    │       │   ├───complete-vpc
    │       │   ├───ipv6
    │       │   ├───issues
    │       │   ├───manage-default-vpc
    │       │   ├───network-acls
    │       │   ├───outpost
    │       │   ├───secondary-cidr-blocks
    │       │   ├───simple-vpc
    │       │   ├───vpc-flow-logs
    │       │   └───vpc-separate-private-route-tables
    │       └───modules
    │           └───vpc-endpoints
    └───providers
        └───registry.terraform.io
            └───hashicorp
                ├───aws
                │   ├───3.76.1
                │   │   └───windows_amd64
                │   └───5.65.0
                │       └───windows_amd64
                ├───http
                │   └───2.1.0
                │       └───windows_amd64
                ├───local
                │   └───2.1.0
                │       └───windows_amd64
                ├───random
                │   └───3.1.0
                │       └───windows_amd64
                └───tls
                    └───3.1.0
                        └───windows_amd64
```

