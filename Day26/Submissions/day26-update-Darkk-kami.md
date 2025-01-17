# Day 25: Build a Scalable Web Application with Auto Scaling on AWS
## Participant Details

- **Name:** Dwayne Chima 
- **Task Completed:** Deploy a scalable web application using AWS EC2 instances, an Elastic Load Balancer (ELB), and Auto Scaling policies
- **Date and Time:** 23rd Dec 2024 05:30 am

## Architecture
![asg](https://github.com/user-attachments/assets/dfda1297-a33d-4d5f-b0a0-62fe72aadbe1)

## GitHub repo link
https://github.com/Darkk-kami/terraform-asg


## Project Structure
```
├── env
│   └── dev
│       ├── main.tf
│       ├── outputs.tf
│       ├── terraform.tf
│       ├── terraform.tfvars
│       └── vars.tf
├── modules
│   ├── alb
│   │   ├── alb.tf
│   │   ├── outputs.tf
│   │   └── vars.tf
│   ├── asg
│   │   ├── asg.tf
│   │   ├── outputs.tf
│   │   └── vars.tf
│   ├── cloud_watch
│   │   ├── cw.tf
│   │   └── vars.tf
│   ├── launch_template
│   │   ├── LT.tf
│   │   ├── outputs.tf
│   │   └── vars.tf
│   ├── shared
│   │   └── security_groups
│   │       ├── outputs.tf
│   │       ├── sg.tf
│   │       └── vars.tf
│   └── vpc
│       ├── outputs.tf
│       ├── vars.tf
│       └── vpc.tf
└── templates
    └── user_data.sh
```

## Challenges Faced
- **Security Groups**: Ensuring the security groups were correctly configured to allow HTTP traffic from the ALB, but after reviewing the security group rules, everything worked as expected.

## Best Practices Applied

- **Terraform Modules**: Created reusable modules for the EC2 instances, ELB, and Auto Scaling group to maintain a modular and DRY code structure.
- **Remote State Management**: Configured S3 for storing the Terraform state and DynamoDB for state locking, ensuring that my Terraform runs are consistent across teams and machines.
- **Version Control**: Committed my changes regularly and tagged the commits to document the progress of the project.
  
