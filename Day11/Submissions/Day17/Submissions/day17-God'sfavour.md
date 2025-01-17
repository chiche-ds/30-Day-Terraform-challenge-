### Name: God'sfavour Braimah
### Task: Day 17:Testing Documentation
### Date: 12/28/24
### Time: 7:20am
# Day 17: Manual Testing Documentation: EKS Infrastructure

## Test Environment
- **Region:** [Your AWS Region]
- **Environment:** Development
- **Terraform Version:** 1.x
- **Date:** December 26, 2024

## Pre-Test Checklist
- [ ] AWS credentials configured
- [ ] Terraform installed and initialized
- [ ] kubectl installed
- [ ] Required IAM permissions verified
- [ ] Test variables file prepared

## Test Cases
## Repository Link  
You can find the repository here: [Production Grade Deployment](https://github.com/GfavourBraimah/Production_grade_deployment).  

### 1. VPC and Networking Module
```bash
# Initialize and plan
cd environments/dev
terraform init
terraform plan -target=module.networking

# Verify outputs
terraform output
```
### 2. IAM Role Configuration
```
terraform plan -target=module.iam
```
### 3. EKS Cluster Deployment
```
terraform plan -target=module.eks
terraform apply -target=module.eks
```
### Cleanup Procedure
# Destroy resources in reverse order
```
terraform destroy -target=module.eks
terraform destroy -target=module.iam
terraform destroy -target=module.networking
```

# Verify cleanup
```
aws eks list-clusters
aws ec2 describe-vpcs
```