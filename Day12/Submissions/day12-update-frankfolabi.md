# Day 12: Zero-Downtime Deployment with Terraform 

## Participant Details

- **Name:** Franklin Afolabi
- **Task Completed:** Worked on zero downtime deployment. This is useful to avoid service interruptions when update a prodution server live.
- **Date and Time:** September 20 2200hrs

## Terraform Code 
```hcl

# Using the lifecycle rule to create before destroy
resource "aws_autoscaling_group" "example" {
  name = "${var.cluster_name}-${aws_launch_configuration.webserver.name}"

  launch_configuration = aws_launch_configuration.webserver.name
  vpc_zone_identifier = data.aws_subnets.default.ids

  target_group_arns = [aws_lb_target_group.webserver.arn]
  health_check_type = "ELB"

  min_size = var.min_size
  max_size = var.max_size

  # Wait for this number of instances to pass health checks
  min_elb_capacity = var.min_size

  # Create replacement ASG first before deleting the original
  lifecycle {
    create_before_destroy = true
  }

  tag {
    key = "Name"
    value = var.cluster_name
    propagate_at_launch = true
  }

  dynamic "tag" {
    for_each = var.custom_tags

    content {
      key = tag.key
      value = tag.value
      propagate_at_launch = true
    }
  }
}

# Native deployment method in which AWS takes care of the instance refresh. This may take longer.
resource "aws_autoscaling_group" "example" {
  name = var.cluster_name

  launch_configuration = aws_launch_configuration.webserver.name
  vpc_zone_identifier = data.aws_subnets.default.ids

  target_group_arns = [aws_lb_target_group.webserver.arn]
  health_check_type = "ELB"

  min_size = var.min_size
  max_size = var.max_size

  instance_refresh {
    strategy = "Rolling"

    preferences {
      min_healthy_percentage = 50
    }
  }
}


# Output when the replacement was going on as there is an interchange between old and new

<h1>New server text</h1>

<h1>New server text</h1>

<h1>Hello, Terraform</h1>

<h1>Hello, Terraform</h1>

<h1>New server text</h1>

<h1>Hello, Terraform</h1>

<h1>New server text</h1>

<h1>Hello, Terraform</h1>

```
## Architecture 

[Name](link to image in S3 bucket)
