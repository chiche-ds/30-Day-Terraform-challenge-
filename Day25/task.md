# Day 25: Deploy a Static Website on AWS S3 with Terraform

## Task Description

1. **Follow Best Practices**: 
   - Use **Terraform modules** for reusable code.
   - Manage your **state remotely** with S3 and DynamoDB for state locking.
   - Ensure all changes are tracked using **version control** (Git).
   - Ensure not to repeat yourself 

2. **Infrastructure Setup**:
   - Create an **S3 bucket** for hosting the static website.
   - Set up a **CloudFront distribution** to serve content from the S3 bucket over HTTPS.
   - Optionally, configure **Route53** to point your custom domain to the CloudFront distribution.

### Bonus Challenge:
- **Custom Domain Setup with Route53**: If you have a custom domain, set it up with Route53 to point to your CloudFront distribution for secure access.

### Blog Post Ideas:
- **Title**: "Deploying a Static Website on AWS S3 with Terraform: A Beginner's Guide"
- **Bonus**: Add details on how following best practices helped structure your project better.

### Social Media Post:
- "🚀 Deployed my first static website on AWS S3 with Terraform today! Learning best practices is key to success. #30daytfchallenge #HUG #hashicorp #HUGYDE @Chi Che. #IaC #terraform"


