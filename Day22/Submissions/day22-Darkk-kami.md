# Day 22: Integrating Workflows for Application and Infrastructure Code

## Participant Details

- **Name:** Dwayne Chima
- **Task Completed:** Putting It All Together - Wrapping Up the Book and Celebrating Success!  
- **Date and Time:** 21st Dec 2024 8:32pm

**check-environment-tags.sentinel**
```hcl
import "tfplan-functions" as plan

# Mandatory tags
mandatory_tags = ["Environment"]

# Allowed Environments
allowed_environments = ["dev", "staging", "prod"]

# Get all EC2 instances
allEC2Instances = plan.find_resources("aws_instance")

EC2InstancesWithoutEnvironmentTag =
        plan.filter_attribute_not_contains_list(allEC2Instances,
                        "tags", mandatory_tags, true)

EC2InstancesWithInvalidEnvironmentTag = plan.filter_attribute_map_key_contains_items_not_in_list(allEC2Instances,
                        "tags", "Environment", allowed_environments, true)

# Count violations
violations = length(EC2InstancesWithoutEnvironmentTag["messages"]) + length(EC2InstancesWithInvalidEnvironmentTag["messages"])

# Main rule
main = rule {
  violations is 0
}
```
