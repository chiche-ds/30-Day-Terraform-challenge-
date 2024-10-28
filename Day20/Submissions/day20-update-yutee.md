# Day 20: Workflow for Deploying Application Code

## Participant Details

- **Name:** Utibe Okon (yutee)
- **Task Completed:**
    - Secure sensitive variables in Terraform Cloud and integrate your version control system (e.g., GitHub) for automated deployments.
     - Explore Terraform Cloud's private registry feature to store and share modules.
- **Date and Time:** Wed 16th October, 2024 | 8:37 AM GMT+1

__Using terrafrom cloud:__
  - Setup terraform configuration files
  - Perform local/manual testing
  - Push your terraform code to github (encrypt secrest and ensure to use remote backend)
  - Create a vcs workspace on terraform cloud
  - Add the terraform repository
  - Terraform starts running

## Terraform Code 
```hcl
terraform { 
  cloud { 
    
    organization = "Contoso" 

    workspaces { 
      name = "Development" 
    } 
  } 
}
```