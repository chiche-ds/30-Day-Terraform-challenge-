# Day 18: Automated Testing of Terraform Code
## Participant Details

- **Name:** Dwayne Chima
- **Task Completed:** Used Terratest to automate tests and ensure they can be run in a CI/CD pipeline.
- **Date and Time:** 19th Dec 2024 12:30 am

## Architecture Diagram
![ci-cd](https://github.com/user-attachments/assets/d57008b6-210d-4f4e-b3b5-6a68b0a50048)

## Summary
- **Pipeline Configuration**: The CI/CD pipeline is configured to run automated tests using GitHub Actions. It is triggered by a push event to the main branch.
- **Linting**: The pipeline first runs a linting step to ensure that the code adheres to the defined coding standards.
- **Terratest Integration**: Terratest is used for infrastructure testing, specifically to validate the deployment of infrastructure resources on cloud platforms.
- **OIDC Setup**: OIDC (OpenID Connect) is used for better management of pipelines and resources.
- **Testing Flow**: The pipeline runs Terratest after a successful push to the main branch, ensuring that the infrastructure behaves as expected.
- **Deployment**: The deployment process includes a manual approval step before releasing changes to the production environment.

## Terratest code
```go
package test

import (
	"fmt"
	"testing"
	"time"

	"github.com/gruntwork-io/terratest/modules/http-helper"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestWebServerResponse(t *testing.T) {
    t.Parallel()

    terraformOptions := &terraform.Options{
        // Path to the Terraform configuration files
        TerraformDir: "../",
    }

    // Ensure resources are cleaned up at the end of the test
    defer terraform.Destroy(t, terraformOptions)

    // Initialize and apply Terraform configuration
    terraform.InitAndApply(t, terraformOptions)

    // Fetch the public IP of the EC2 instance from Terraform outputs
    publicIp := terraform.Output(t, terraformOptions, "public_ip")
    fmt.Println("Public IP:", publicIp)

    assert.NotEmpty(t, publicIp)

    // Construct the URL to the web server
    url := "http://" + publicIp
    expectedText := "<h1>Hello from Apple</h1>"

    // Define a retryable HTTP test to ensure the server is up and running
    maxRetries := 7
    timeBetweenRetries := 10 * time.Second
    http_helper.HttpGetWithRetry(t, url, nil, 200, expectedText, maxRetries, timeBetweenRetries)
}
```


## Pipeline sample
```yaml
name: Terraform

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  lint:
    name: Terraform Linting
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Install tflint
      run: |
        curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash

    - name: Run tflint
      run: |
        tflint 

  terratest:
    name: Terraform Test
    runs-on: ubuntu-latest
    needs: lint 

    defaults:
      run:
        shell: bash

    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Setup Go
      uses: actions/setup-go@v3
      with:
        go-version: "1.22"

    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: "1.10.3"
        terraform_wrapper: false

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: ${{ secrets.ASSUME_ROLE }}
        role-session-name: github-action-role
        aws-region: ${{ secrets.REGION }}

    - name: Cache Terraform
      uses: actions/cache@v3
      with:
        path: ~/.terraform
        key: ${{ runner.os }}-terraform-${{ hashFiles('**/*.tf') }}
        restore-keys: |
          ${{ runner.os }}-terraform-

    - name: Install dependencies
      run: |
        cd test
        go mod tidy

    - name: Terratest
      if: success() && (github.ref == 'refs/heads/main') && (github.event_name == 'push')
      run: |
        cd test
        go test -v

  deploy:
    name: Terraform Deploy
    runs-on: ubuntu-latest
    needs: terratest
    environment: production
    if: success()  # Only run if Terratest passes

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: "1.10.3"
          terraform_wrapper: false

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.ASSUME_ROLE }}
          role-session-name: github-action-role
          aws-region: ${{ secrets.REGION }}

      - name: Cache Terraform
        uses: actions/cache@v3
        with:
          path: ~/.terraform
          key: ${{ runner.os }}-terraform-${{ hashFiles('**/*.tf') }}
          restore-keys: |
            ${{ runner.os }}-terraform-

      - name: Terraform Init
        run: terraform init

      - name: Terraform Apply
        run: |
          terraform apply -auto-approve
```
