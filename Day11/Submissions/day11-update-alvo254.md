# Day 11: Understanding Terraform Conditionals

## Participant Details

- **Name:** Alvin Ndungu
- **Task Completed:** Conditionals with Terraform
- **Date and Time:** 2024-08-20 15:18pm


- Terraform conditionals allow you to execute specific configurations or return values based on a logical condition, similar to "if-else" statements in programming. They are typically used with `count`, `for_each`, and variable definitions to dynamically adjust your infrastructure based on input values or resource states.
- If the `condition` evaluates to `true`, Terraform returns `true_value`; otherwise, it returns `false_value`.

```
variable "environment" {
  type    = string
  default = "dev"
}

variable "instance_type" {
  default = var.environment == "production" ? "t3.large" : "t3.micro"
}

```

```
variable "use_https" {
  type    = bool
  default = true
}

resource "aws_security_group_rule" "allow_http" {
  count       = var.use_https ? 0 : 1
  type        = "ingress"
  from_port   = 80
  to_port     = 80
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "allow_https" {
  count       = var.use_https ? 1 : 0
  type        = "ingress"
  from_port   = 443
  to_port     = 443
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

```