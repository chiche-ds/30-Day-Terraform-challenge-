# Day 12: Zero-Downtime Deployment with Terraform

## Participant Details

- **Name:** Ejibode Ibraheem A
- **Task Completed:** Implement zero-downtime infra deployment with terraform using the blue/green strategy. Also wrote a blog post on the blue/green deployment strategy.
- **Date and Time:** 14/12/2024 1:00 PM

This lifecycle rule ensures there is 
## Terraform Code 
```hcl

resource "aws_launch_configuration" "example" {
    image_id = var.ami
    instance_type = var.instance_type
    security_groups = [aws_security_group.instance.id]
    user_data = templatefile("${path.module}/user-data.sh", {
        server_port = var.server_port
        db_address = data.terraform_remote_state.db.outputs.address
        db_port = data.terraform_remote_state.db.outputs.port
        server_text = var.server_text
    })

    # Required when using a launch configuration with an auto scaling group.
    lifecycle {
        
    }
}

resource "aws_autoscaling_group" "example" {
    # Explicitly depend on the launch configuration's name so each time it's replaced, this ASG is also replaced
    name                 = "${var.cluster_name}-${aws_launch_configuration.example.name}"
    launch_configuration = aws_launch_configuration.example.name
    vpc_zone_identifier  = data.aws_subnets.default.ids

    target_group_arns    = [aws_lb_target_group.asg.arn]
    health_check_type    = "ELB"
    min_size             = var.min_size
    max_size             = var.max_size

    # Wait for at least this many instances to pass health checks before considering the ASG deployment complete
    min_elb_capacity     = var.min_size


    # When replacing this ASG, create the replacement first, and only delete the original after
    lifecycle {
        create_before_destroy = true
    }
}
```