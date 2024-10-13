# Day 27: 3-Tier Multi-Region High Availability Infrastructure with AWS and Terraform

## Overview

Welcome to Day 27 of the 30-Day Terraform Challenge! Today, you will build a production-ready **3-tier multi-region infrastructure** using AWS and Terraform. This architecture will ensure **high availability** and **fault tolerance** by distributing traffic across multiple AWS regions. You will deploy:

1. **Web Tier**: Elastic Load Balancer (ELB) to distribute traffic across application instances.
2. **Application Tier**: EC2 instances running your application.
3. **Database Tier**: Multi-region RDS database with read replicas for cross-region failover.

This project will test your knowledge of Terraform's best practices, modularity, and AWS high-availability strategies.

---

## Tasks for Today

### 1. **Reading**
   - **Documentation**: Review the following sections in the Terraform documentation:
     - VPC, EC2, Elastic Load Balancer (ELB), and Auto Scaling documentation
     - RDS Multi-AZ and Cross-Region Read Replicas


### 2. **Activity**
   - **Web Tier**: Deploy Elastic Load Balancer (ELB) in public subnets to handle incoming web traffic.
   - **Application Tier**: Deploy EC2 instances in private subnets to handle application logic, scaling them with an Auto Scaling Group (ASG).
   - **Database Tier**: Deploy a primary RDS instance with cross-region read replicas to ensure failover.
   - **DNS Failover**: Configure Route53 to manage DNS and failover routing between regions.

### 3. **Bonus Hands-On Project**
   - Implement **S3 Cross-Region Replication** to replicate static content (such as images, and assets) across AWS regions for even better redundancy.

---

## Blog Post Ideas
- **Title**: "Building a 3-Tier Multi-Region High Availability Architecture with Terraform"
- **Bonus**: Discuss how using Terraform modules simplified the creation of multi-region architectures and ensured scalability.

---

## Social Media Post
- "🚀 Built a 3-tier multi-region high-availability infrastructure using AWS and Terraform! #30daytfchallenge #HUG #hashicorp #HUGYDE @Chi Che. #IaC #terraform"

---

## How to Submit Your Work

### 1. **Create the `day27-your-username.md` File**
   - Document the steps you took to deploy the 3-tier infrastructure.
   - Include the challenges you faced, how you applied Terraform best practices, and the final architecture diagram.

### 2. **Commit and Push Your Changes**
   - Stage and commit your changes:
     ```bash
     git add .
     git commit -m "Completed Day 27: 3-Tier Multi-Region High Availability Infrastructure"
     ```

### 3. **Create a Pull Request**
   - Push your branch:
     ```bash
     git push origin day27-multi-region-ha
     ```
   - Open a pull request and submit it for review.

---

## Checklist
- [ ] I used **Terraform modules** for all infrastructure components (VPC, EC2, ELB, RDS).
- [ ] I stored Terraform state **remotely** in S3 and used DynamoDB for state locking.
- [ ] I committed my changes regularly using **version control**.
- [ ] I deployed a 3-tier multi-region, high-availability infrastructure using **EC2**, **ELB**, **RDS**, and **Route53**.
- [ ] I wrote and published a blog post about today's project.
- [ ] I created a pull request with all the required details.

