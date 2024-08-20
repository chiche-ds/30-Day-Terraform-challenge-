```terraform
# Your Terraform code here
provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
}

 - Stage and commit your changes in the `daily-update.md` file with a message like:
     ```bash
     git add Day4/daily-update.md
     git commit -m "Completed Day 4 task and updated daily-update.md"
     ```
