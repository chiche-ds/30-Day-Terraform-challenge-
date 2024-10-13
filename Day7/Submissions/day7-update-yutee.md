## Day 6 Task : Understanding Terraform State - Part 2
_Utibe Okon | Sat, October 12 2024 | 8:35 AM - GMT+1_

__State file isolation:__

As infrastructure demands grow, and workload increases, it is crucial to divide up environments for easy management. This is where state file isolation comes in. Isolation can be acheived in two different ways.
- Using Workspaces
- Using File Layout

Today, I learnt how to leverage both methods to create different environments for managing our infrastructure with terraform.

I also practiced using file layout to manage statefile. 
File layout folfer structure:
```
stage
|__ datastore
        |__ mysql
            |__ variables.tf
            |__ outputs.tf
            |__ main.tf
    |__ services
        |__ webserver-cluster.tf
            |__ output.tf
            |__ variables.tf
            |__ main.tf
global
|__ s3
    |__ output.tf
    |__ main
```
