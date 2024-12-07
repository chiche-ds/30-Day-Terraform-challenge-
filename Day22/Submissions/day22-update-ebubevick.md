# Day 22: Integrating Workflows for Application and Infrastructure Code

## Participant Details

- **Name:** Omekwu Victor Ebube  
- **Task Completed:** Integrated workflows for application and infrastructure code, including version control and Sentinel policies.  
- **Date and Time:** 25-November-2024 at 8:50 PM WAT.
---
## mandatory-tagss.tftest.hcl
```bash
run "setup_tests" 
    module {
        source = "./tests/setup"
    }
}

run "resource_group" {
  command = plan

  variables {
    resource_group_name = "${run.setup_tests.bucket_prefix}-aws-s3-website-test"
  }

  # Check that the bucket name is correct
  assert {
    condition     = resource_group_name.s3_bucket.bucket == "${run.setup_tests.bucket_prefix}-aws-s3-website-test"
    error_message = "Invalid bucket name"
  }
}
```

