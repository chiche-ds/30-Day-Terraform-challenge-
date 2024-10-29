# Day 18: Automated Testing of Terraform Code
## Participant Details

- **Name:** Njoku Ujunwa Sophia 
- **Task Completed:** Use tools like Terratest to automate these tests and ensure they can be run in a CI/CD pipeline.
- **Date and Time:** 15/09/2024 01:33 PM

```yaml
name: Terraform CI

on:
  push:
    branches:
      - main  

jobs:
  terraform:
    name: Terraform
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Go
      uses: actions/setup-go@v3
      with:
        go-version: '1.20' 

    - name: Install Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: 1.6.0 

    - name: Cache Terraform
      uses: actions/cache@v3
      with:
        path: ~/.terraform
        key: ${{ runner.os }}-terraform-${{ hashFiles('**/*.tf') }}
        restore-keys: |
          ${{ runner.os }}-terraform-

    - name: Terraform Init
      run: terraform init

    - name: Terraform Plan
      run: terraform plan

    - name: Terraform Apply
      run: terraform apply -auto-approve
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        AWS_REGION: ${{ secrets.AWS_REGION }}

    - name: Set up Go Modules
      run: go mod tidy

    - name: Run Tests
      run: go test -v ./test
```
