# Day 25: Deploy a Static Website on AWS S3 with Terraform

## Participant Details
- **Name:** Dwayne Chima 
- **Task Completed:** Deploy a Static Website on AWS S3 with Terraform.
- **Date and Time:** 22nd Dec 2024 2:08am

## Architecture Diagram
![static_website](https://github.com/user-attachments/assets/faca5195-a89c-450c-b343-ba09cd2f0504)

## GitHub Repo Link
- https://github.com/Darkk-kami/terraform-s3-static

## File Structure
```
├── README.md
├── env
│   └── dev
│       ├── main.tf
│       ├── terraform.tfvars
│       └── vars.tf
├── modules
│   ├── acm
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   └── vars.tf
│   ├── cloudfront
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   └── vars.tf
│   ├── route53
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   └── vars.tf
│   └── s3-static-website
│       ├── main.tf
│       ├── outputs.tf
│       └── vars.tf
├── providers.tf
├── static
│   ├── images
│   │   └── dancing_cat.gif
│   ├── index.html
│   └── styles.css
├── terraform.tf
└── vars.tf
```
## Key Components
1. **Modules:**
   - **S3 Module:** Configures the S3 bucket for static website hosting.
   - **CloudFront Module:** Sets up the CloudFront distribution for secure HTTPS delivery.
   - **ACM Module:** Manages the SSL certificate for CloudFront.
   - **Route53 Module (Optional):** Configures DNS for custom domain integration.

2. **Static Website Content:**
   - Located in the `static/` directory, including an HTML page, CSS styles, and a fun image!

3. **Remote State Management:**
   - State files are stored in an S3 bucket with state locking enabled via DynamoDB.

4. **Providers:**
   - AWS as the cloud provider for all services.

## Key Challenges
1. **CloudFront Configuration:**
   - Ensuring the distribution pointed correctly to the S3 bucket origin and enabling HTTPS.
2. **ACM Certificate Validation:**
   - Successfully validating the domain for HTTPS required proper DNS setup using Route53.
