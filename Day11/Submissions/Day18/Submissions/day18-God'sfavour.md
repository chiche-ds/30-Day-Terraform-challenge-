### Day 18: Automated Testing for Terraform EKS Infrastructure
### Overview
This demonstrates the implementation of automated testing for Terraform EKS infrastructure using Terratest. The tests cover VPC configuration, IAM roles, and overall infrastructure deployment validation.
Test Structure
# Automated Testing for EKS Infrastructure

## Test Structure
- Unit Tests: Validate individual module configurations
- Integration Tests: Verify resource interactions
- End-to-End Tests: Test complete infrastructure deployment

## Prerequisites
- Go 1.17+
- Terraform 1.0.0+
- AWS credentials
- GitHub account

## Running Tests Locally
1. Install dependencies:
```bash
cd test
go mod init eks-test
go mod tidy

```
func TestVPCCreation(t *testing.T) {
    t.Parallel()

    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../environments/dev",
        Vars: map[string]interface{}{
            "environment": "test",
            "project_name": "eks-test",
            "vpc_cidr": "10.0.0.0/16",
            "az_count": 2,
        },
    })

    // Clean up resources when test completes
    defer terraform.Destroy(t, terraformOptions)

    // Deploy infrastructure
    terraform.InitAndApply(t, terraformOptions)

    // Get VPC ID from Terraform output
    vpcID := terraform.Output(t, terraformOptions, "vpc_id")

    // Test VPC configuration
    vpc := aws.GetVpcById(t, vpcID, "us-west-2")
    assert.Equal(t, "10.0.0.0/16", *vpc.CidrBlock)

    // Test subnet creation
    subnets := aws.GetSubnetsForVpc(t, vpc.VpcId, "us-west-2")
    assert.Equal(t, 4, len(subnets)) // 2 public + 2 private subnets

    // Test route table configuration
    routeTables := aws.GetRouteTablesForVpc(t, vpc.VpcId, "us-west-2")
    assert.GreaterOrEqual(t, len(routeTables), 3) // 1 public + 2 private route tables

    // Test NAT Gateway
    natGateways := aws.GetNatGatewaysForVpc(t, vpc.VpcId, "us-west-2")
    assert.Equal(t, 1, len(natGateways))
}

func TestIAMRoles(t *testing.T) {
    t.Parallel()

    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../environments/dev",
        Vars: map[string]interface{}{
            "environment": "test",
            "project_name": "eks-test",
            "enable_irsa": true,
        },
    })

    // Clean up resources when test completes
    defer terraform.Destroy(t, terraformOptions)

    // Deploy infrastructure
    terraform.InitAndApply(t, terraformOptions)

    // Get role ARNs from Terraform output
    clusterRoleARN := terraform.Output(t, terraformOptions, "cluster_role_arn")
    nodeRoleARN := terraform.Output(t, terraformOptions, "node_role_arn")

    // Test cluster role
    clusterRole := aws.GetIamRole(t, clusterRoleARN)
    assert.Contains(t, *clusterRole.RoleName, "cluster-role")

    // Test node role
    nodeRole := aws.GetIamRole(t, nodeRoleARN)
    assert.Contains(t, *nodeRole.RoleName, "node-role")

    // Test cluster role policies
    attachedPolicies := aws.GetIamRolePolicies(t, *clusterRole.RoleName, "us-west-2")
    assert.Contains(t, attachedPolicies, "AmazonEKSClusterPolicy")

    // Test node role policies
    nodePolicies := aws.GetIamRolePolicies(t, *nodeRole.RoleName, "us-west-2")
    expectedPolicies := []string{
        "AmazonEKSWorkerNodePolicy",
        "AmazonEKS_CNI_Policy",
        "AmazonEC2ContainerRegistryReadOnly",
    }
    
    for _, policy := range expectedPolicies {
        assert.Contains(t, nodePolicies, policy)
    }

    // Test IRSA configuration if enabled
    if terraform.Output(t, terraformOptions, "enable_irsa") == "true" {
        oidcProvider := aws.GetIamOpenIdConnectProvider(t, 
            terraform.Output(t, terraformOptions, "oidc_provider_arn"))
        assert.NotNil(t, oidcProvider)
    }
}
```