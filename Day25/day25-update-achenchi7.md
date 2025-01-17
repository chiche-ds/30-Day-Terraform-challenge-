# Day 25: Deploy a Static Website on AWS S3 with Terraform
## Participant Details

- **Name:** Jully Achenchi
- **Task Completed:** Deploy a Static Website on AWS S3 with Terraform.
- **Date and Time:** 10/01/2025


### modules/website/main.tf
```hcl
resource "aws_s3_bucket" "website_bucket" {
  bucket = var.bucket_name

  website {
    index_document = "index.html"
    error_document = "error.html"
  }
}

resource "aws_s3_bucket_object" "index_html" {
  bucket       = aws_s3_bucket.website_bucket.bucket
  key          = "index.html"
  source       = "index.html"  # Ensure this is the correct path
  content_type = "text/html"
}

resource "aws_s3_bucket_object" "styles_css" {
  bucket       = aws_s3_bucket.website_bucket.bucket
  key          = "styles.css"
  source       = "styles.css"  # Ensure this is the correct path
  content_type = "text/css"
}

# Disable public access block (Ensure public policies can be applied)
resource "aws_s3_bucket_public_access_block" "website_bucket_public_access" {
  bucket                 = aws_s3_bucket.website_bucket.id
  block_public_acls      = false
  block_public_policy    = false
  ignore_public_acls     = false
  restrict_public_buckets = false
}

resource "aws_cloudfront_origin_access_identity" "example" {
  comment = "Origin Access Identity for my static website"
}

resource "aws_cloudfront_distribution" "cdn" {
  origin {
    domain_name = "${aws_s3_bucket.website_bucket.bucket}.s3.amazonaws.com"
    origin_id   = "S3-${aws_s3_bucket.website_bucket.id}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.example.id
    }
  }

  enabled             = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.website_bucket.id}"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
  }

  price_class = "PriceClass_100"

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
}

resource "aws_s3_bucket_policy" "allow_cloudfront" {
  bucket = aws_s3_bucket.website_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity ${aws_cloudfront_origin_access_identity.example.id}"
        }
        Action = "s3:GetObject"
        Resource = "${aws_s3_bucket.website_bucket.arn}/*"
      }
    ]
  })
}
```

### modules/website/variables.tf
```hcl
variable "bucket_name" {
  description = "The name of the S3 bucket to create"
  default        = "jully-static-website-bucket"
}
```

### modules/website/outputs.tf
```hcl
output "bucket_name" {
  value = aws_s3_bucket.website_bucket.bucket
}
```

### state.tf
```hcl
provider "aws" {
  region = "us-east-1"  # Change the region as needed
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "jully-bucket"  
}

resource "aws_s3_bucket_versioning" "terraform_state_versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name           = "terraform-locks"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
}
```

### main.tf
```hcl
module "website" {
  source      = "./modules/website"
  bucket_name = "jully-static-website-bucket"  
}

terraform {
  backend "s3" {
    bucket         = "jully-static-website-bucket"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```
