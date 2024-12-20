# Day 20: Workflow for Deploying Application Code

## Participant Details
- **Name:** Dwayne Chima
- **Task Completed:** Simulated deployment process and integrated Terraform Cloud’s version control, secure variables, and private registry features.  
- **Date and Time:** 20th Dec 2024 4:05 pm

## 1. **Setup Terraform Configuration Files**  
- Define infrastructure resources using Terraform’s `.tf` files.  
- Configure the backend to use Terraform Cloud for secure state management.

  ### Terraform Cloud Configuration
  ```hcl
  terraform {
    cloud {
      organization = "Project-kami"
  
      workspaces {
        name = "kami-workspace"
      }
    }
  }
  ```

## 2. **Local Testing**  
- Ran `terraform init` to initialize the configuration.  
- Validated the code with `terraform validate`.  
- Previewed changes using `terraform plan`.  

## 3. **Push to GitHub**  
- Encrypted sensitive data (e.g., secrets, keys) using Terraform Cloud variable management.  
- Pushed the tested code to a GitHub repository 

## 4. **Create a VCS-Linked Workspace in Terraform Cloud**  
- Used Terraform Cloud to create a new workspace linked to the GitHub repository.  
- Ensured the workspace monitors the main branch for changes.

  
![Screenshot 2024-12-20 155830](https://github.com/user-attachments/assets/6fe16f37-3f94-4a95-993c-0336aa4a1200)



## 5. **Automated Plan and Apply**  
- Terraform Cloud automatically detects changes, generates a plan, and applies them after approval.  
- Monitor execution logs and validate the infrastructure deployment.  
