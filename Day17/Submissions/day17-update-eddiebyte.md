# Day 17: Manual Testing of Terraform Code

## Participant Details

- **Name:** Eddie Chem
- **Task Completed:** All tasks for Day 17
- **Date and Time:** 1/10/2025 1:17 PM

##  Manual Testing of Terraform Configuration: Steps and Key Focus Areas 

1. **Review Terraform Code Syntax**  
   Use `terraform validate` to ensure the code is syntactically correct. Check for typos, formatting issues, and unused resources.  

2. **Check Resource Configuration**  
   Verify resource definitions for correctness, including provider details, resource types, and attributes. Ensure values align with requirements.  

3. **Validate Input Variables**  
   Test input variables with different values to confirm they are correctly defined, typed, and behave as expected during deployment.  

4. **Test Dependency Mapping**  
   Examine resource dependencies (`depends_on` or implicit dependencies) to ensure Terraform builds resources in the correct order.  

5. **Run Plan Command**  
   Execute `terraform plan` to preview the changes Terraform will make. Confirm that the output matches expected configurations.  

6. **Apply in a Test Environment**  
   Deploy the configuration in a controlled environment using `terraform apply` to validate actual resource creation and confirm there are no errors.  

7. **Check State File**  
   Inspect the Terraform state file to ensure all resources are tracked accurately and that no unnecessary sensitive data is stored.  

8. **Perform Drift Detection**  
   Use `terraform plan` on existing infrastructure to identify if there are changes between actual resources and the configuration.  

9. **Test Rollback**  
   Simulate resource failure or misconfigurations to test `terraform destroy` or manual rollback capabilities without causing disruptions.  

10. **Verify Outputs**  
    Confirm that defined outputs match the expected values after applying the configuration.  

11. **Security and Compliance Checks**  
    Ensure sensitive information is securely stored and that resources meet security and compliance standards (e.g., IAM roles, security groups).  

12. **Document Findings**  
    Record issues, resolutions, and results for future reference and continuous improvement of the configuration.  
