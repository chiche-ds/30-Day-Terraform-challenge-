# Day 7: Understanding Terraform State Part 2

## Participant Details
- **Name:** Eddie Chem
- **Task Completed:** Completed all tasks for Day 7, except for the social media post, and focused on learning about various isolation techniques to improve manageability, security, and collaboration within infrastructure as code (IaC) practices.
- **Date and Time:** 8/25/2024 11:39 PM

## State File Isolation:
**Summary:**

Remote state files store and manage your infrastructure's state in a central location, rather than locally on your machine. 
This approach is essential for collaborative environments and maintaining your infrastructure's state across different environments or teams.
The example below depicts state file management with an object storage (S3) backend. Enabling Versioning in your backend (e.g., S3 bucket versioning) 
can equally help to recover from accidental deletions or changes.

![Remote State Files](https://drive.google.com/uc?export=view&id=1S-b-HHE7aJyaTPhNMOX40lFCB3jGjzJu)


## Workspace Isolation:
**Summary:**

Terraform workspaces are a technique to manage multiple instances of your infrastructure configuration with isolated state files. 
Each workspace has its state file, allowing you to work with multiple environments or versions of your infrastructure. In the example below,
I created an extra workspace using the command `terraform workspace new [new-workspace-name]` after initializing my working directory and deploying a web server.

![Workspace 1](https://drive.google.com/uc?export=view&id=1DYVNnxbp-2CVuk29wTodWPRfXRrwxMyz)

## Isolation of Files and Folders:
**Summary:**

The image demonstrates a well-organized Terraform file structure that isolates configurations by environment (e.g., global, stage) and service 
(e.g., datastores, webserver-cluster). Each environment and service has its own set of Terraform files, including state files (`terraform.tfstate`) 
and provider lock files (`.terraform.lock.hcl`), ensuring modularity, state management, and consistency. 

![VScode Working Directory - File Layout Isolation](https://drive.google.com/uc?export=view&id=1nhbAI-qk72OomNF1FZQVEUZ4sG8PDrqV)
