## Day 21: Deploy a Static Website on AWS S3 with Terraform

- **Name:** Salako Lateef
- **Date:** 04/10/2026
- **Task completed:**Deployed a Static Website on AWS S3 and accessible using cloudfront with Terraform


## modules/s3-static-website/main.tf
```
resource "aws_s3_bucket" "static_site" {
  bucket = var.bucket_name
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  tags = {
    Name = var.bucket_name
  }
}

resource "aws_s3_bucket_policy" "public_access" {
  bucket = aws_s3_bucket.static_site.id

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : "*",
        "Action"   : "s3:GetObject",
        "Resource" : "${aws_s3_bucket.static_site.arn}/*"
      }
    ]
  })
}
```
## modules/s3-static-website/variables.tf
```
variable "bucket_name" {
  description = "The name of the S3 bucket."
  type        = string
}
```

## modules/s3-static-website/outputs.tf
```
output "s3_bucket_name" {
  value = aws_s3_bucket.static_site.bucket
}

output "s3_bucket_website_url" {
  value = aws_s3_bucket.static_site.website_endpoint
}

```
## envs/dev/main.tf
```
module "s3_static_website" {
  source      = "../../modules/s3-static-website"
  bucket_name = var.bucket_name
}

resource "aws_cloudfront_distribution" "website_distribution" {
  origin {
    domain_name = module.s3_static_website.s3_bucket_website_url
    origin_id   = "S3-${module.s3_static_website.s3_bucket_name}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.s3_identity.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CloudFront Distribution for static website"
  default_root_object = "index.html"

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${module.s3_static_website.s3_bucket_name}"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
  }
}
```

## backend.tf
```
terraform {
  backend "s3" {
    bucket         = "terraform-state-storage"
    key            = "dev/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```
## provider.tf
```
provider "aws" {
  region = var.region
}
```
## envs/dev/variables.tf
```
variable "bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
  default     = "my-dev-static-website"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}
```
## envs/dev/terraform.tfvars
```
bucket_name = "my-dev-static-website"
region      = "us-west-2"
```
