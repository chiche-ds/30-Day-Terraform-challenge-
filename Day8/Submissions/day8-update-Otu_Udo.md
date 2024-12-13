Name: Otu Michael Udo
Task Completed: Day 8: Reusing Infrastructure with Modules
Date:11/12/24
Time: 8:03pm
Module Basics", "Inputs", and "Outputs
I was able to understand how to create reusable modules. Terraform modules are the building blocks of scalable and reusable infrastructure. By effectively managing inputs and outputs, you can enhance your team's productivity and simplify complex configurations by using modules.

Inputs: These are like parameters you pass into a module. Use them to make your modules flexible and reusable across environments. For example, specify instance types or regions.
for example ,
variable "instance_type" {
  default = "t2.micro"
}

Outputs: Outputs help you extract information from a module for use in other parts of your configuration.

By combining inputs and outputs effectively, you can:
Reuse configurations across projects and share values between modules easily