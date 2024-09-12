# Day 7: Understanding Terraform State Part 2
## Participant Details

- **Name:** Ebenka christian 
- **Date and Time:** 09-09-2024 at 01:45 am
- **Task Completed:** 

**Reading**: 
note to myself: 
    The state file format is a private API that is meant only for internal use within Terraform. You should never edit the Terraform state files by hand or write code that reads them directly.

    The backend block in Terraform does not allow
 you to use any variables or references.


**Activity**: 
   - Practice state isolation:
     - **Workspaces**: Set up isolated environments for development, staging, and production using Workspaces.
     - **File Layouts**: Create isolated environments using separate file layouts for each environment.