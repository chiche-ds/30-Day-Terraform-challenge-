## Day 8 Task : Reusing Infrastructure with Modules
_Utibe Okon | Sat, October 12 2024 | 1:02 PM - GMT+1_

__Terraform Modules:__
Completed all relevant readings and videos. Got enlightened in ways to reuse terraform configuration using modules. 
- Creating Modules
- Referencing Modules
- Using external modules
- Passing data between modules and properly referencing them using inputs (varibales), and outputs.

`main.tf`

```hcl
# calling a module in the root main.tf
module "ec2" {
  source = "./modules/ec2"

  instance_type = "t2.micro"
  ami      = "ami-0e86e20dae9224db8"
  subnet_id = "subnet-03cb68d25e5198c95"
  depends_on = [module.vpc]
}
```

