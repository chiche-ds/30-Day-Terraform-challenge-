## Day 5 Task
_Utibe Okon | Wed, August 21 2024 | 11:57 PM_

---

__Scaling a webserver with Terraform__
Scaling is important when the traffic to our server cannot be predicted. To ensure server does not go down due to high traffic, Auto Scalling Groups (ASG) are used to deploy our infrastructure. They manage spining up new servers and conducting healthchecks.

To create an asg, a _launch configuration_ is needed,it carries rules for each server in the scale group.
```
    resource "aws_launch_configuration" "example" { 
        image_id = "ami-0fb653ca2d3203ac1" 
        instance_type = "t2.micro"
    }
```
Create the auto scale group...
```
    resource "aws_autoscaling_group" "example" {
        launch_configuration = aws_launch_configuration.example.name
        min_size = 2
        max_size = 10
        tag {
            key = "Name"
            value = "terraform-asg-example" propagate_at_launch = true
        }            
    }
```

The code above deploys an autoscaling group that can create up to 10 instances depending on user request and always have at least 2 instances running, this brings a problem, each instance will have a different ip address, but we want to ultimately give just one ip address to users or dns service. To accomplish this, load baalncers help in routing traffic to the different servers. So we should create a LB and a listener group.
```
    resource "aws_lb" "example" {
        name = "terraform-asg-example" 
        load_balancer_type = "application"
        subnets = data.aws_subnets.default.ids
        security_groups = [aws_security_group.alb.id]
    }

    resource "aws_lb_listener" "http" { 
        load_balancer_arn = aws_lb.example.arn 
        port = 80
        protocol = "HTTP"

        # By default, return a simple 404 page
        default_action {
            type = "fixed-response"
            fixed_response {
            content_type = "text/plain"
            message_body = "404: page not found"
            status_code  = 404
        }}
    }
```
By default, LBs do not allow traffic, so we will need some networking rules to allow necessary traffic to it.
```
    resource "aws_security_group" "alb" { 
        name = "terraform-example-alb"

        ingress {
            from_port = 80
            to_port = 80
            protocol = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        }

        egress {
            from_port = 0
            to_port = 0
            protocol = "tcp"
            cidr_blocks = ["0.0.0.0/0"]
        } 
    }
```

__Terraform State File__
Terraform needs a way to remember the resources it creates and their values, for htis it uses the _state file_, when terraform apply is ran for the first time, it creates a file _terraform.tfstate_, with this file, it stores the resources current state in json format. Upon further changes to the terrraform configurations and running terraform plan, it pulls the state file data and compares it against the new configurations, and then terraform plan outputs the changes to be made for approval. 

It is rare that one would have reason to edit the terraform state file as it is a provate api that is meant to be used internally by terraform. Making manual changes to the state file can lead to data loss, and state file corruption.


__Comparing Terraform blocks__
- _Data_
Retrieve data from external sources or existing infrastructure.
    Code Sample:
    ```
        data "<provider_type>" "<name>" {
            [settings...]
        }
    ```
    Use Case:
    - Fetching information about available AMIs or instance types
    - Incorporating external data into your infrastructure decisions

- _Module_
Organize configurations into reusable modules
    Code Sample:
    ```
        module "<name_of_module>" {
            source = <file_path_to_nodule>
        }
    ```
    Use Case:
    - Breaking down code and promoting code reuse and maintainability

- _Output_
Define output values to display information about your infrastructure
    Code Sample:
    ```
        output "<name>" {
            value = <what_should_be_outputed>
        }
    ```
    Use Case:
    - Exposing information about created resources for use in other scripts or tools