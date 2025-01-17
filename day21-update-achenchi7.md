## Day 21: Workflow for Deploying Application Code

- **Name:** Jully Achenchi
- **Date:** 03/01/2025
- **Task:** Terraform Cloud workflow

  ## The process
  - Write your configuration file
  - Test locally using `terraform init`, `terraform plan`, and `terraform apply`
  - Push your terraform code to your version control system using the following commands:
        - `git init` to initialize an empty repo
        - `git add .` to add your files for tracking
        - `git commit -m <commit message>` - to commit your files to git.
        - `git push -u origin main` - to push your files to a remote repo on the main branch.
  - Create a vcs workspace on terrafform cloud
  - Add the terraform repository
  - Terraform starts running
