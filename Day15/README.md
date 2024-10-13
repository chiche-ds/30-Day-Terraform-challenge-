# Day 15: Working with Multiple Providers - Part 2

## Overview

Welcome to Day 15 of the Terraform 30-Day Challenge! Today, we continue working with multiple providers, focusing on more complex scenarios such as multi-cloud deployments and integrating Docker and Kubernetes with Terraform. By the end of today, you will have experience deploying resources across multiple cloud providers and using Docker containers and Kubernetes clusters managed by Terraform.

## Tasks for Today

### 1. **Reading**
   - **Chapter**: Complete Chapter 7 of "Terraform: Up & Running"
     - Sections: "Working with Multiple AWS Regions", "Working with Multiple AWS Accounts", "Creating Modules That Can Work with Multiple Providers", "Working with Multiple Different Providers", "A Crash Course on Docker", "A Crash Course on Kubernetes", "Deploying Docker Containers in AWS Using Elastic Kubernetes Service", "Conclusion".
   - **Goal**: Understand how to manage infrastructure across multiple AWS regions and accounts, create modules that work with multiple providers, and deploy Docker containers and Kubernetes clusters using Terraform.

### 2. **Videos**
   - **Udemy**: Rewatch the videos on Terraform modules:
     - Rewatch video of Day14
     - **Video 77**: "AWS multiRegion alais"
     - Focus on how modules can be adapted to work with multiple providers.
       
   - **Goal**: Prepare for creating multi-provider modules and deploying multi-cloud resources.

### 3. **Activity**
   - **Multi-Provider Modules**: Create Terraform modules that can work with multiple providers. For example, create a module that deploys infrastructure on both AWS and GCP.
   - **Docker and Kubernetes**: Deploy Docker containers in AWS using Elastic Kubernetes Service (EKS) managed by Terraform.
   - **Goal**: Successfully deploy resources across multiple cloud providers and integrate Docker and Kubernetes into your Terraform configurations.

### 4. **Blog Post**
   - **Title**: "Deploying Multi-Cloud Infrastructure with Terraform Modules"

### 5. **Social Media Post**
   - **Text**: "🌐 Deployed multi-cloud infrastructure using Terraform today, including Docker and Kubernetes—taking my Terraform skills to the next level! #30daytfchallenge #HUG #hashicorp #HUGYDE @Chi Che. #IaC #terraform"

### 6. **Activity**
   - **Discussion Preparation**: Prepare questions and topics for tomorrow's live session on Terraform AWS Modules with Anton Babenko. Think about how these concepts apply to your current projects and what you’d like to learn more about.

## How to Submit Your Work

### 1. **Create the `day15-update-your-github-username.md` File**
   - Include your Terraform code and any architecture diagrams in the markdown file.
   - Document your experience with creating multi-provider modules and deploying Docker and Kubernetes resources with Terraform.
   - Save the file in your `day15-multi-cloud-modules` branch.

### 2. **Commit Your Changes**
   - Stage and commit your changes with a message like:
     ```bash
     git add day15-update-your-github-username.md
     git commit -m "Completed Day 15 task on multi-provider modules"
     ```

### 3. **Create a Pull Request**
   - Push your changes to your GitHub repository:
     ```bash
     git push origin day15-multi-cloud-modules
     ```
   - Create a pull request using the provided template and include any additional comments if necessary.

## Checklist

- [ ] I have completed Chapter 7 of "Terraform: Up & Running".
- [ ] I have rewatched the videos on Terraform modules.
- [ ] I have successfully created and deployed multi-provider Terraform modules.
- [ ] I have deployed Docker containers and Kubernetes clusters using Terraform.
- [ ] I have written and published a blog post about today's task.
- [ ] I have made a social media post about today's task.
- [ ] I have created a `day15-update-your-github-username.md` file with my Terraform code and architecture diagrams.
- [ ] I have prepared questions for tomorrow's live session.
- [ ] I have created a pull request with all the required details.

## Additional Resources

- [Terraform: Up & Running on Amazon](https://www.amazon.com/Terraform-Running-Infrastructure-Configuration-Management/dp/1492046906)
- [Udemy Course on Terraform](https://www.udemy.com/course/terraform/)
- [Terraform Documentation on Multiple Providers](https://www.terraform.io/docs/language/providers/index.html)
- [Terraform Documentation on Docker Provider](https://registry.terraform.io/providers/kreuzwerker/docker/latest/docs)
- [Terraform Documentation on Kubernetes Provider](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs)
