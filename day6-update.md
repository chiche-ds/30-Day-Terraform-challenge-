**Name**: Jully Achenchi

**Architecture diagram**
![](https://github.com/achenchi7/terraform-projects/blob/main/Untitled-2024-05-29-1021.excalidraw.png)

### How to setup remote state in Terraform
1. Create an S3 bucket and add a lifecycle setting, enable versioning, enable server-side encryption, and block public access

```hcl
resource "aws_s3_bucket" "tf_state-bucket" {
  bucket = "terraform-state"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "tf_state-bucket-versioning" {
  bucket = aws_s3_bucket.tf_state-bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "tf_state-bucket-encryption" {
  bucket = aws_s3_bucket.tf_state-bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "tf_state-bucket-public-access-block" {
  bucket = aws_s3_bucket.tf_state-bucket.id

  block_public_acls       = true
  block_public_policy     = true
  restrict_public_buckets = true
  ignore_public_acls      = true
}
```

2. Create a dynamoDB table for state locking. Create a primary key called LockID (use the same spelling and capitalization)

```hcl
resource "aws_dynamodb_table" "tf_state-lock" {
  name         = "terraform-state-lock"
  hash_key     = "LockID"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

3. It is at this point that we will deploy the resources above before including the backend block.

**NOTE**: Terraform cannot use the S3 backend until the S3 bucket and DynamoDB table exist!

```hcl
terraform init
terraform plan
terraform apply
```
4. Putting it all together in the `backend` block

```hcl
terraform {
  backend "s3" {
    bucket = "terraform-state"
    key    = "terraform.tfstate"
    region = "us-east-1"

    dynamodb_table = "terraform-state-lock"
    encrypt = true
  }
}
```
5. Initialize Terraform again to make use of the S3 bucket we just created.

```
terraform init
terraform plan
terraform apply
```