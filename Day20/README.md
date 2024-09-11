# Day 20: Workflow for Deploying Application Code

## Overview

Welcome to Day 20 of the Terraform 30-Day Challenge! Today, we will focus on the typical **workflow for deploying application code**. This workflow is well-established in the DevOps industry and involves steps like using version control, testing, and deploying code. Understanding this workflow is crucial as we compare it later to the **workflow for deploying infrastructure code**.

By the end of today, you should have a solid understanding of how to deploy application code from development to production, and how to secure your variables, integrate version control, and use a private registry in Terraform.

## Tasks for Today

### 1. **Reading**
   - **Chapter**: Continue reading Chapter 10 of "Terraform: Up & Running"
     - Section: "A Workflow for Deploying Application Code"
   - **Goal**: Understand the seven steps of a typical workflow for taking application code from development to production:
     1. Use version control.
     2. Run the code locally.
     3. Make code changes.
     4. Submit changes for review.
     5. Run automated tests.
     6. Merge and release.
     7. Deploy.

### 2. **Videos**
   - **Udemy**: Watch the following videos from Section 12:
     - "HCP Terraform (Terraform Cloud) - Secure Variables" (Video 70)
     - "HCP Terraform (Terraform Cloud) - Version Control Integration" (Video 71)
     - "HCP Terraform (Terraform Cloud) - Private Registry" (Video 72)
   - **Goal**: Learn how to secure sensitive variables, integrate version control, and use Terraform Cloud's private registry.

### 3. **Activity**
   - **Deploying Application Code**:
     - Follow the steps outlined in the reading to simulate a typical workflow for deploying application code.
     - Secure sensitive variables in Terraform Cloud and integrate your version control system (e.g., GitHub) for automated deployments.
     - Explore Terraform Cloud's private registry feature to store and share modules.

### 4. **Blog Post**
   - **Title**: "A Workflow for Deploying Application Code with Terraform"

### 5. **Social Media Post**
   - **Text**: "🚀 Learning how to deploy application code step-by-step with version control and secure variables using Terraform Cloud! #30daytfchallenge #HUG #hashicorp #HUGYDE @Chi Che. #IaC #terraform"

## How to Submit Your Work

### 1. **Create the `day20-update-your-github-username.md` File**
   - Include details of your deployment workflow, securing variables, and using the private registry in Terraform Cloud.
   - Save the file in your `day20-deploying-app-code` branch.

### 2. **Commit Your Changes**
   - Stage and commit your changes with a message like:
     ```bash
     git add day20-update-your-github-username.md
     git commit -m "Completed Day 20 task on deploying application code with Terraform"
     ```

### 3. **Create a Pull Request**
   - Push your changes to your GitHub repository:
     ```bash
     git push origin day20-deploying-app-code
     ```
   - Create a pull request using the provided template and include any additional comments if necessary.

## Checklist

- [ ] I have read the section "A Workflow for Deploying Application Code" in Chapter 10 of "Terraform: Up & Running".
- [ ] I have watched the Udemy videos on secure variables, version control integration, and the private registry.
- [ ] I have simulated a workflow for deploying application code and secured sensitive variables in Terraform Cloud.
- [ ] I have written and published a blog post about today's task.
- [ ] I have made a social media post about today's task.
- [ ] I have created a `day20-update-your-github-username.md` file with details on deploying application code and Terraform Cloud features.
- [ ] I have created a pull request with all the required details.
