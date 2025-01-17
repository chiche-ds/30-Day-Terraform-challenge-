# Day 13: Managing Sensitive Data in Terraform

## Participant Details

- **Name:** Ejibode Ibraheem A 
- **Task Completed:** Managing Sensitive Data in Terraform
- **Date and Time:** 18/12/2024

provider "aws" {
 region = "us-east-2"
}
data "aws_caller_identity" "self" {}

# create IAM POLICY
data "aws_iam_policy_document" "cmk_admin_policy" {
 statement {
 effect = "Allow"
 resources = ["*"]
 actions = ["kms:*"]
 principals {
 type = "AWS"
 identifiers = [data.aws_caller_identity.self.arn]
 }
 }
}


# CREATE CUSTOMER MANAGED KEY USING THE AWS KEY MANAGED SERVICE

resource "aws_kms_key" "cmk" {
 policy = data.aws_iam_policy_document.cmk_admin_policy.json
}

# CREATE HUMAN FRIENDLY ALIAS FOR YOUR CMK USING AWS KMS RESOURCE
resource "aws_kms_alias" "cmk" {
 name = "alias/kms-cmk-example"
 target_key_id = aws_kms_key.cmk.id
}

# NOW THE CMK CAN THEN BE USED WITH AWS API AND CLI TO ENCRYPT AND DECRYPT DATA
