# Day 9: Continue reUse of infrastructure with terraform modules

## Participant Details

- **Name: Dwayne Chima 
- **Task Completed: Continue with Chapter 4 (Pages 115-139)
- **Date and Time: 10th Dec 2024 7:00pm

## 
```
module "eks-module" {
  source         = "git::https://github.com/Darkk-kami/eks-modules?ref=v1.0.0"
  region         = "eu-north-1"
  vpc_cidr       = "10.0.0.0/16"
  dns_hostnames  = true
  dns_support    = true
  pub_one_cidr   = "10.0.1.0/24"
  pub_two_cidr   = "10.0.2.0/24"
  priv_one_cidr  = "10.0.3.0/24"
  priv_two_cidr  = "10.0.4.0/24"
  az_one         = ""
  az_two         = ""
  vpc_id         = "aws_vpc.eks_vpc.id"
  eks_version    = "1.26"
  ami_type       = "AL2_x86_64"
  instance_types = ["t3.small", "t3.medium", "t3.large"]
  capacity_type  = "ON_DEMAND"
}
```
