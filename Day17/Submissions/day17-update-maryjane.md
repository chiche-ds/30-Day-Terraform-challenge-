# Day 17: Manual Testing of Terraform Code 

## Participant Details

- **Name:** Maryjane Enechukwu
- **Task Completed:**Reading: Start Chapter 9 of "Terraform: Up & Running"
Sections: "Manual Tests", "Manual Testing Basics", "Cleaning Up After Tests"

Performed manual tests on an existing Terraform configuration by creating example folder
- **Date and Time:** 23/10/2024  7:30pm

## Manual Testing of Terraform Configuration: Steps and Key Focus Areas

1. **Preparation**
   - **Review the Terraform Configuration**: Before starting the manual testing, ensure that you understand the infrastructure you are deploying. Check the `main.tf`, `variables.tf`, and `outputs.tf` files, and make sure you know what resources will be created.

 2. **Apply the Configuration**
   - **Run `terraform plan`**: This step allows you to preview the changes that will be made to your infrastructure. Check the output carefully to verify that the correct resources will be created, modified, or destroyed.
   
   - **Run `terraform apply`**: Once you are satisfied with the plan, run `apply` to deploy the resources.

 3. **Testing the Infrastructure**
   After applying the configuration, manually inspect and verify the resources in the cloud provider console (e.g., AWS, Azure, or Google Cloud).

4. **Cleanup**
   - **Manual Cleanup**: Once testing is complete, clean up all resources to avoid unnecessary costs.
     - Use `terraform destroy` to tear down the infrastructure. This ensures you don’t leave behind any orphaned resources.
     - Manually double-check in the cloud provider’s console that no resources are lingering (sometimes certain resources may not be fully deleted).

5. **Post-Test Verification**
   - After the cleanup, run a final `terraform plan` to ensure that Terraform’s state and the actual cloud infrastructure are synchronized and clean.
####