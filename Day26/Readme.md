# Day 26: Build a Scalable Web Application with Auto Scaling on AWS

## Overview

Welcome to Day 26 of the 30-Day Terraform Challenge! 🎉 Today’s project focuses on building an **intermediate-level** infrastructure by deploying a **scalable web application** using **AWS EC2 instances**, an **Elastic Load Balancer (ELB)**, and **Auto Scaling** to dynamically adjust the number of EC2 instances based on traffic.

As always, we will adhere to **Terraform best practices**:
- Use **modules** to keep your code modular and reusable.
- Manage **remote state** using S3 and DynamoDB for state locking.
- Use **version control** (Git) to track and manage your changes.
- Use **DRY** Principles.

By the end of today, you'll have deployed an AWS infrastructure that automatically scales based on demand, following best practices for scalability and maintainability.

---

## Project Structure

Here’s how to structure your Terraform project for today:

```
project-root/
├── modules/
│   ├── ec2/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── elb/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── asg/
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
## 📋 Steps for Today

### 1. Best Practices to Follow
- Use Terraform modules for EC2, ELB, and Auto Scaling resources.
- Store Terraform state remotely using S3, and enable state locking with DynamoDB.
- Ensure your work is committed regularly using version control.

### 2. Infrastructure Setup

#### EC2 Instances:
- Deploy EC2 instances to run your web application.
- Use security groups to allow HTTP/HTTPS traffic to your instances.

#### Elastic Load Balancer (ELB):
- Set up an ELB to distribute incoming traffic between your EC2 instances.
- Make sure the load balancer is publicly accessible.

#### Auto Scaling Group (ASG):
- Create an Auto Scaling group to manage EC2 instances dynamically.
- Define scaling policies based on metrics like CPU utilization or incoming traffic.

### 3. Bonus Challenge (Optional)
- Implement CloudWatch monitoring to track the performance of your EC2 instances and ELB.
- Set up CloudWatch alarms to trigger Auto Scaling actions based on performance metrics.

## ✍️ Blog Post Idea
**Title**: "Building a Scalable Web Application with Terraform, EC2, and Auto Scaling"  
**Bonus**: Include a section on how following Terraform best practices ensures scalability and maintainability.

## 🐦 Social Media Post Idea
**Text**:  
"🚀 Built a scalable web app on AWS with EC2, Auto Scaling, and ELB! Learning to design for scale with Terraform. #30daytfchallenge #HUG #hashicorp #HUGYDE @Chi Che. #IaC #terraform"

## ✅ How to Submit Your Work

### 1. Create the `day26-your-username.md` File
- Document your process for building the infrastructure, any challenges you faced, and how you applied Terraform best practices.
- Save this file in your `day26-scalable-web-app` branch.

### 2. Commit Your Changes
Stage and commit your changes with a message like:

```bash
git add .
git commit -m "Completed Day 26: Scalable Web App with Auto Scaling and ELB"
```
### 3. Create a Pull Request 
```bash
git push origin day26-scalable-web-app
```

### 📝 Checklist
- [ ] I used Terraform modules for EC2, ELB, and Auto Scaling components.
- [ ] I stored Terraform state remotely in S3 and locked it with DynamoDB.
- [ ] I committed my changes regularly using version control.
- [ ] I deployed a scalable web application using EC2, ELB, and Auto Scaling.
- [ ] I wrote and published a blog post about today's project.
- [ ] I created a pull request with all the required details.

### 📚 Additional Resources:
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2)
- [Terraform EC2 Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance)
- [Terraform Auto Scaling Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/autoscaling_group)

