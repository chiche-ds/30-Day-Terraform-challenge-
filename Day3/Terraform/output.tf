# print the url of the webserver
output "ec2_web_url" {
  value     = join ("", ["http://", aws_instance.ec2_instance.public_dns, ":", "80"])
}

# print the url of the webserver
output "ssh_connection_command" {
  value     = join ("", ["ssh -i my_ec2_key.pem ec2-user@", aws_instance.ec2_instance.public_dns])
}