# Day 9: Continuing Reuse of Infrastructure with Modules
## Participant Details

- **Name:** Ebenka christian 
- **Date and Time:** 10-09-2024 at 00:30 am
- **Task Completed:** 

1. **Reading**: Continue with Chapter 4 (Pages 115-139)
   - Sections: "Module Gotchas", "Module Versioning" .
2. **Udemy Videos**: 
   - Video 38: "Terraform Module - Scope "
   - Video 39: "Terraform Module - Public Registory "
   - Video 40: "Terraform Module - versioning "




# Terraform versionned EC2 Instance Module

```hcl
#This module deploys an EC2 instance on AWS.
##https://registry.terraform.io/modules/terraform-aws-modules/ec2-instance/aws/latest
module "ec2_instance" {
  source        = "git::https://github.com/chrisjoel/ec2_terraform_module.git?ref=v1.0.0"
  ami           = "ami-0182f373e66f89c85"
  instance_type = "t2.micro"
  name          = "30daysterraform"
}
```


## Changelog
### v1.0.0
git tag v1.0.0
git push origin v1.0.0

- Initial release of the EC2 instance module.

### v1.1.0
- Added support for additional instance types.
- Improved documentation and examples.