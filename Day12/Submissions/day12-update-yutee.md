# Day 12: Zero-Downtime Deployment with Terraform

## Participant Details

- **Name:** Utibe Okon (yutee)
- **Task Completed:** Implement zero-downtime infra deployment with terraform using the blue/green strategy. Also wrote a blog post on the blue/green deployment strategy.
- **Date and Time:** Sun 13th October, 2024 | 3:15 PM GMT+1

Blue-green deployment is a strategy that reduces downtime and risks during application updates by running two identical environments: blue (active) and green (new version). The idea is to shift traffic between these environments to ensure seamless updates without impacting users.

With Terraform, you can provision these environments using Launch Configurations and Auto Scaling Groups (ASGs). The blue ASG manages the current version, while the green ASG hosts the new version. Both ASGs are registered with an Elastic Load Balancer (ELB), which initially directs traffic to the blue environment.

To ensure smooth updates, the create_before_destroy lifecycle hook can be added to the ASG configuration. This guarantees that the green ASG is fully created and healthy before the blue ASG is decommissioned. Once the green environment is tested, the ELB shifts traffic to it. If the new version performs well, the blue ASG is destroyed; if not, traffic can quickly switch back to the blue environment. Terraform’s modular approach and lifecycle rules make it easy to automate this process, ensuring reliable rollbacks and seamless updates.

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
## Architecture 

![architecture diagram](https://i.imgur.com/N18YDR3.png)