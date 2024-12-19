### Steps for Manual Testing:

1. Initialize Terraform
   ```bash
   terraform init
   ```

2. Use Terraform validate to check if the configuration files are syntactically correct and valid.
   ```hcl
   terraform validate
   ```

3. Run Terraform Plan to check what changes Terraform will apply before actually applying them.
   ```hcl
   terraform plan
   ```

4. Apply the changes to create the infrastructure. 
   ```hcl
   terraform apply
   ```

5. Verify Resource Creation

6. Test Resource Functionality
7. Check for Regressions
   - To ensure no regressions have been introduced:
     - **Rerun Plan**: Run `terraform plan` again after applying the changes to verify that there are no 
unexpected diffs. Ideally, it should show no changes.
     - **Change Variables**: Modify some input variables (e.g., instance type) and rerun the plan to 
ensure the infrastructure can handle variable changes correctly.
     - **Apply and Rollback**: Apply a set of changes, then roll them back to the previous state, 
ensuring that Terraform tracks state and restores resources correctly.

8. Clean Up Resources

```hcl
   terraform destroy
   ```
