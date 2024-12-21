##Day 22: Putting It All Together - Congratulations on Making It This Far! 🎉
 terraform {
      source = "github.com/<OWNER>/modules//services/hello-world-app?ref=v0.0.7"
}
    include {
      path = find_in_parent_folders()
}
    dependency "mysql" {
      config_path = "../../data-stores/mysql"
}
    inputs = {
      environment = "stage"
      ami         = "ami-0fb653ca2d3203ac1"
      min_size = 2
      max_size = 2 
      enable_autoscaling = false mysql_config = dependency.mysql.outputs
       }

      dependency "mysql" {
      config_path = "../../data-stores/mysql"
      }

