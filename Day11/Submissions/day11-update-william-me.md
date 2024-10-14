# Day 11: Terraform conditionals

## Participant Details

- **Name:** William Maina
- **Task Completed:** Terraform Conditionals
- **Date and Time:** 14-10-2024 20:45

## Terraform Code 
main.tf
```hcl
resource "aws_instance" "ubuntu" {
  //If var.high_availability is set to truethen Create three aws_instance resources	else	Create one aws_instance resource
  count = (var.high_availability == true ? 3 : 1)
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  associate_public_ip_address = (count.index == 0 ? true : false)
  subnet_id                   = aws_subnet.subnet_public.id
}
```

variables.tf
```hcl
variable "high_availability" {
  type        = bool
  description = "If this is a multiple instance deployment, choose `true` to deploy 3 instances"
  default     = true
}

```
