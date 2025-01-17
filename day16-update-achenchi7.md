# Day 16:  Building Production-Grade Infrastructure
## Participant Details

- **Name:** Jully Achenchi
- **Task Completed:**"production grade infrastructure

- **Date and Time:** 30/12/2024 




##main.tf
```hcl
provider "aws" {
  region = "us-east-1"
}

module "vpc" {
  source = "./modules/vpc"
}

module "ec2_webserver" {
  source                = "./modules/ec2_webserver"
  elb_security_group_id = module.public_elb.elb_security_group_id
  vpc_id                = module.vpc.vpc_id
}

module "asg_webserver" {
  source = "./modules/asg_webserver"
  subnet_ids = [
    module.vpc.cloudforce_privateA_id,
    module.vpc.cloudforce_privateB_id
  ]
  target_group_arn   = module.public_elb.frontendTG
  launch_template_id = module.ec2_webserver.launch_template_id
}

module "public_elb" {
  source = "./modules/public_elb"
  vpc_id = module.vpc.vpc_id
  subnet_ids = [
    module.vpc.cloudforce_publicA_id,
    module.vpc.cloudforce_publicB_id
  ]
  webserver_sg = module.ec2_webserver.webserver_sg
}

module "appserver_elb" {
  source = "./modules/appserver_elb"
  vpc_id = module.vpc.vpc_id
  subnet_ids = [
    module.vpc.cloudforce_privateA_id,
    module.vpc.cloudforce_privateB_id
  ]
  webserver_sg_id = module.ec2_webserver.webserver_sg
  appserver_sg_id = module.ec2_appserver.appserver_sg
}


module "ec2_appserver" {
  source                = "./modules/ec2_appserver"
  appserver_elb_sg_id   = module.appserver_elb.appserver_elb_sg_id
  vpc_id                = module.vpc.vpc_id
  elb_security_group_id = module.public_elb.elb_security_group_id
}

module "asg_appserver" {
  source = "./modules/asg_appserver"
  subnet_ids = [
    module.vpc.cloudforce_privateC_id,
    module.vpc.cloudforce_privateD_id
  ]
  target_group_arn   = module.appserver_elb.appserverTG
  launch_template_id = module.ec2_appserver.launch_template_id
}

module "cloudfront" {
  source      = "./modules/cloudfront"
  domain_name = module.public_elb.frontend_lb_dns_name
  frontend_lb = module.public_elb.frontend_lb
}

module "cloudtrails" {
  source = "./modules/cloudtrails"
}
```
