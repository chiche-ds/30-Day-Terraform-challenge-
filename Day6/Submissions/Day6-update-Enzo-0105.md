# Day 6: Understanding Terraform State

## Participant Details

- **Name:** Salako Lateef
- **Task Completed:** Terraform Backend state with remote enhanced backend
- **Date and Time:** 2024-10-02 20:54 PM

terraform.tf
```
terraform {
  backend "remote" {
    hostname = "app.terraform.io"
    organization = "enzo-0105"
    workspaces {
      name = "enzo"
    }
  }
}


```
