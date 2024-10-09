# Day 25: Deploy a Static Website on AWS S3 with Terraform

## Overview

Welcome to Day 25 of the 30-Day Terraform Challenge! 🎉 Today, we’re focusing on a **beginner-level** project where you will deploy a simple static website using **AWS S3** and integrate it with a **CloudFront** distribution for content delivery. This project will give you practical experience with **Terraform best practices**, such as using modules, managing state remotely, and properly structuring your project.

The goal is to follow Terraform's best practices while setting up your infrastructure, including:
- Using **Terraform modules** for reusable code.
- Managing **remote state** using S3 and DynamoDB (for state locking).
- Applying **version control** to keep track of changes.
- Applying  **DRY** concepts 

By the end of this project, you'll have deployed a static website accessible via **CloudFront** over a secure HTTPS connection!

## Project Structure
Your project structure should follow this format:

```
project-root/
├── modules/
│   └── s3-static-website/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── envs/
│   └── dev/
│       ├── main.tf
│       ├── variables.tf
│       └── terraform.tfvars
├── backend.tf
├── provider.tf
└── variables.tf

```


## Tasks for Today

### 1. **Terraform Best Practices**
- **Use modules**: Create a reusable module for the S3 bucket that can be easily adapted for other projects.
- **Manage remote state**: Store your state file in an S3 bucket and use DynamoDB for state locking.
- **Version control**: Ensure you commit your changes regularly using Git.

### 2. **Infrastructure Setup**
   - **S3 Bucket**: 
     - Create an S3 bucket to store your website files.
     - Enable public access for the bucket to make the website accessible.
   - **CloudFront Distribution**:
     - Set up a CloudFront distribution to serve the website over HTTPS.
     - Configure the distribution to point to the S3 bucket as the origin.

### 3. **Bonus Challenge**
   - **Route53 Integration**:
     - Optionally, set up a Route53 hosted zone to point your custom domain to the CloudFront distribution.

## Key Concepts
- **S3 for static website hosting**: Learn how to configure S3 for serving static content.
- **CloudFront for CDN**: Ensure your website is delivered over a secure, fast network using CloudFront.
- **Remote state management**: Use S3 to store Terraform state and DynamoDB for state locking.

## Blog Post Idea
- **Title**: "Deploying a Static Website on AWS S3 with Terraform: A Beginner's Guide"

## Social Media Post
- **Text**: "🚀 Deployed my first static website on AWS S3 with Terraform today! Learning best practices is key to success. #30daytfchallenge #HUG #hashicorp #HUGYDE @Chi Che. #IaC #terraform"

---

## How to Submit Your Work

### 1. **Create the `day25-update-your-github-username.md` File**
   - Include details of your project, screenshots, and the key challenges you faced.
   - Save this file in your `day25-s3-static-website` branch.

### 2. **Commit Your Changes**
   - Stage and commit your changes with a message like:
     ```bash
     git add .
     git commit -m "Completed Day 25: S3 Static Website with Terraform"
     ```

### 3. **Create a Pull Request**
   - Push your changes to GitHub:
     ```bash
     git push origin day25-s3-static-website
     ```
   - Create a pull request and submit for review.

## Checklist
- [ ] I have used Terraform modules for my S3 and CloudFront resources.
- [ ] I have managed my Terraform state remotely using S3 and DynamoDB.
- [ ] I have committed my changes regularly in version control.
- [ ] I have deployed my static website using S3 and CloudFront.
- [ ] I have written and published a blog post about today's project.
- [ ] I have created a pull request with all the required details.
