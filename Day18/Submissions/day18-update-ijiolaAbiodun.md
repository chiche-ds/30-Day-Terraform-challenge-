```
name: terraform config

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  terraform-test:
    name: terraform 
    runs-on: ubuntu-latest
    steps:
    - name: checking repo
      uses: actions/checkout@v2

    - name: setting up terraform 
      uses: hashicorp/setup-terraform@v3
      with:
        terraform_version: "1.1.7"
        
    - uses: hashicorp/setup-terraform@v3
      name : backend- setup
      with:
        cli_config_credentials_token: ${{ secrets.TF_API_TOKEN }}
        
    - name: Terraform init 
      run: terraform init

    - name: Terraform plan
      run: terraform plan
      
    - name: Terraform apply
      run: terraform apply -auto-approve
      env: 
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
        
    - name: Terraform destroy
      run: terraform destroy -auto-approve
```
