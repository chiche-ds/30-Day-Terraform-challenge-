# Day 18: Automated Testing of Terraform Code

## Participant Details

- **Name:** Yusuf Abdulganiyu
- **Task Completed:**
    - Automated Testing using Terratest on my Multi-Region API Gateway deployment to show case multiple providers, modules, production
      grade code deployment, and now test using Terratest for the API Gateway.
  
- **Date and Time:**  December 18, 2024. 22:21🕥
- **Code Github Repo:** - https://github.com/mnswifi/APIGateway-multi-region
## Terratest Code - (api_gateway_test.go)
```hcl
package test

import (
	"fmt"
	"testing"
	"time"

	"github.com/gruntwork-io/terratest/modules/http-helper"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestApiGateway(t *testing.T) {
	t.Parallel()

	// Define Terraform options
	terraformOptions := &terraform.Options{
		TerraformDir: "../modules/apigw", 
	}

	// Resource clean up
	defer terraform.Destroy(t, terraformOptions)

	// Deploy infrastructure
	terraform.InitAndApply(t, terraformOptions)

	// Retrieve API Gateway URL from Terraform output
	apiURL := terraform.Output(t, terraformOptions, "api_gateway_url")

	// Validate API Gateway
	validateApiGateway(t, apiURL)
}

func validateApiGateway(t *testing.T, apiURL string) {
	// Append resource path
	fullURL := fmt.Sprintf("%s/items", apiURL)

	// Allow retries for API Gateway to be ready
	http_helper.HttpGetWithRetry(
		t,
		fullURL,
		nil,
		200,          // Expected HTTP status code
		"",           // Expected body (empty for mock response)
		5,            // Max retries
		5*time.Second, // Wait time between retries
	)
}


```
## Architecture 
![Screenshot 2024-12-18 095852](https://github.com/user-attachments/assets/c27177fa-212b-4cc1-b193-7d355782d33f)

