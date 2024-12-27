# Day 27: 3-Tier Multi-Region High Availability Infrastructure with AWS and Terraform

## Participant Details
- **Name:** Dwayne Chima
- **Task Completed:** 3-tier multi-region infrastructure using AWS and Terraform.
- **Date and Time:** 25th Dec 2024 17:50 pm

## Terraform Code Repository
https://github.com/Darkk-kami/terraform-3tier-infra

## Architecture Diagram
![infra](https://github.com/user-attachments/assets/e9d685bc-eabf-4f3a-815e-c50853ee39ca)

## **Architecture Layout**
### **Frontend Layer**
- Deployed an Auto Scaling Group (ASG) for high availability.
- Integrated with an Elastic Load Balancer (ALB) to distribute traffic evenly.
- Configured the ALB with SSL using an ACM certificate and a custom domain.
![domain](https://github.com/user-attachments/assets/7a9aa8c5-0c07-40dc-9bd8-5531f0705a13)

### **Application Layer**
- Provisioned instances in private subnets to isolate them from public access.
- Configured a NAT Gateway in public subnets for secure outbound internet access.
- Set up routing to ensure proper communication between subnets.
- Deployed applications using a launch template with an instance profile, granting:
  - Access to specific secrets in AWS Secrets Manager for database credentials.
  - Permissions to write application logs to an S3 bucket.
    
### **Database Layer**
- Provisioned Amazon RDS in a private subnet for persistence.
- Ensured security by restricting access only to the application layer.

![rds_access](https://github.com/user-attachments/assets/a1b7f829-fc30-4dde-b590-c895909bea77)

- Configured a read replica in another region for redundancy and improved read performance.

![rds_replica](https://github.com/user-attachments/assets/973255ee-919d-41b4-8b63-7055785f4256)

## Networking and Security
### **VPC Setup**
- Created a custom VPC with public, private, and database subnets across multiple availability zones.
- Configured an S3 VPC endpoint to enable private communication between the application and the S3 bucket without internet exposure.

![s3_access](https://github.com/user-attachments/assets/8ab66741-0f5f-421c-9456-d2e6a7c56e62)

- Used security groups to enforce strict access controls:
  - ALB only communicates with application instances.
  - Application instances access the RDS database securely.
  - RDS is not publicly accessible.

### **S3 Bucket Configuration**
- Configured S3 for log storage with replication to another region for disaster recovery.
- Enabled lifecycle policies to archive data to reduce costs.

![s3_rep](https://github.com/user-attachments/assets/4073e797-1522-4b02-948b-add849b281f3)


## Monitoring and Failover
### **Database Monitoring**
- Created a Privaate Hosted Zone in both VPCs for DNS Resolution management
- Created CloudWatch alarms to monitor database connections for both primary and replica instances.
- Configured Route 53 health checks based on these alarms to enable automated DNS failover in case of database failure.

![health_check](https://github.com/user-attachments/assets/ef4eca4b-c6c7-4d2e-9104-ae037273b472)


### **Cross-Region Failover**:
- Established a VPC peering connection between the primary and secondary regions to ensure seamless replication and failover support.

![vpc_peering](https://github.com/user-attachments/assets/e58ff7e3-1931-4993-89d8-36c709c31aca)

- Configured Appropriate Route Tables for both VPC to be able to communinicate with each other
- EC2 instances are able to reach both Primary and Read Replica RDS instances for cases of failover, despite being in different regions and private subnets

![connectivity](https://github.com/user-attachments/assets/bc8108cf-fae4-429e-ba1a-071e2a1618ba)




## Deployment Process
### **Infrastructure Setup**
- Leveraged Terraform to define and provision all resources.
- Used remote state storage in S3
- Deployed resources sequentially, starting with foundational components (VPC, subnets, NAT Gateway), followed by ALB, application instances, and RDS.

## Application of Terraform Best Practices
### **Modular Design**
- Developed reusable modules for VPC, ALB, EC2, and RDS etc
- Emphasized self-contained and parameterized module design for flexibility.
  ```
      ├── env
  │   └── dev
  │       ├── main.tf
  │       ├── outputs.tf
  │       ├── terraform.tf
  │       ├── terraform.tfvars
  │       └── vars.tf
  ├── modules
  │   ├── alb/
  │   ├── asg/
  │   ├── instance_profile/
  │   │   ├── policy/
  │   ├── launch_template/
  │   ├── multi-region/
  │   │   ├── cloud_watch/
  │   │   ├── route53failover/
  │   │   └── vpc_peering/
  │   ├── rds/
  │   ├── route_53/
  │   │   ├── acm/
  │   │   ├── health_check/
  │   ├── shared/
  │   │   ├── s3/
  │   │   └── security_groups/
  │   └── vpc/
  └── templates
      └── user_data.sh
  ```
  
### **Secure Configurations**
- Restricted access using security groups and private subnets.
  
### **State Management**
- Configured remote backend storage with S3 for consistency.
