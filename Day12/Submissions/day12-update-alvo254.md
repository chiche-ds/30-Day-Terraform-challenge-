# Day 12: Understanding Terraform State

## Participant Details

- **Name:** Alvin Ndungu
- **Task Completed:** Zero-Downtime Deployment Techniques
- **Date and Time:** 2024-08-20 15:18pm


Implementing zero downtime using blue/green development and terraform

# Blue section

```
resource "aws_instance" "blue" {
  count         = 2
  ami           = "ami-0c55b159cbfafe1f0"  
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.main.id
  tags = {
    Name = "blue-environment"
  }
}

resource "aws_lb_target_group" "blue_tg" {
  name     = "blue-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}

resource "aws_lb_target_group_attachment" "blue_tg_attachment" {
  target_group_arn = aws_lb_target_group.blue_tg.arn
  target_id        = aws_instance.blue.*.id[0]
  port             = 80
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.blue_tg.arn
  }
}
```



# Green section 

```
resource "aws_instance" "green" {
  count         = 2
  ami           = "ami-0c55b159cbfafe1f0" 
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.main.id
  tags = {
    Name = "green-environment"
  }
}

resource "aws_lb_target_group" "green_tg" {
  name     = "green-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}

resource "aws_lb_target_group_attachment" "green_tg_attachment" {
  target_group_arn = aws_lb_target_group.green_tg.arn
  target_id        = aws_instance.green.*.id[0]
  port             = 80
}

```

### Traffic change
```
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.green_tg.arn
  }
}
  
```


**resource lifecycle management** is a way to control how resources are created, updated, and destroyed. Lifecycle settings allow you to influence the default behavior of Terraform during resource management. You can use lifecycle rules to delay destruction, control resource dependencies, or even prevent the destruction of critical resources.

### Common Lifecycle Meta-Arguments

The `lifecycle` block has several key meta-arguments that can be applied to resources to control their behavior:

1. **`create_before_destroy`**: Ensures that Terraform creates a new resource before destroying the old one.
2. **`prevent_destroy`**: Prevents the destruction of a resource. Useful for critical resources, like databases or important infrastructure.
3. **`ignore_changes`**: Instructs Terraform to ignore changes to specific attributes, even if they are modified outside of Terraform (e.g., through the cloud provider console).
4. **`replace_triggered_by`**: Replaces a resource when certain attributes change (such as changes in related resources).


- **Zero-Downtime Updates:**
    
    - Use `create_before_destroy` to ensure that resources like EC2 instances or RDS databases are created before the old ones are destroyed, allowing you to perform updates without service interruptions.
- **Critical Resource Protection:**
    
    - Use `prevent_destroy` for production databases, critical storage (like S3 buckets), or any resources that should never be destroyed without explicit intervention.
- **Avoiding External Changes Overwrites:**
    
    - Use `ignore_changes` when certain attributes are frequently modified outside Terraform and you don't want Terraform to reset those changes (e.g., manually added tags or instance types).
- **Coordinating Resource Updates:**
    
    - Use `replace_triggered_by` when resource A needs to be replaced when resource B changes, ensuring infrastructure consistency when resources are tightly coupled.