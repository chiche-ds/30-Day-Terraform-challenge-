## Day 22: Putting It All Together - Congratulations on Making It This Far! 🎉

- **Name:** Jully Achenchi
- **Date:** 06/01/2025
- **Task Completed:** Practiced sentinel policy and intergated with my tf configuration

## Sentinel.hcl
```
import "tfplan"

# Main rule definition
main = rule {
    all tfplan.resource_changes as resource {
        resource.type == "aws_instance" && resource.change.after.instance_type == "t2.micro"
    }
}
```
