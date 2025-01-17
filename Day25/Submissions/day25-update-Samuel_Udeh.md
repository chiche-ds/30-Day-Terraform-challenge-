Day 25: Deploy a Static Website on AWS S3 with Terraform
Name: Udeh Samuel Chibuike
Task Completed: Deploy a Static Website on AWS S3 with Terraform
Date and Time: 15/1/2025 7:25pm

 # main.tf
provider "aws" {
  region = "us-east-1"  # Adjust to your desired AWS region
}

resource "aws_s3_bucket" "static_website" {
  bucket = "samley-bucket12"  # Ensure this matches your existing bucket name
}

# Remove ACL and manage permissions via a policy
resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = aws_s3_bucket.static_website.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.static_website.arn}/*"
      }
    ]
  })
}

# Define the website configuration
resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.static_website.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}


resource "aws_s3_object" "index" {
  bucket = aws_s3_bucket.static_website.id
  key    = "index.html"
  source = "../../website/index.html"
  content_type = "text/html"  
}

resource "aws_s3_object" "error" {
  bucket = aws_s3_bucket.static_website.id
  key    = "error.html"
  source = "../../website/error.html"
  content_type = "text/html" 
}

resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket                  = aws_s3_bucket.static_website.id
  block_public_acls       = true
  ignore_public_acls      = false
  block_public_policy     = false
  restrict_public_buckets = false
}

# cloudfront creation
resource "aws_cloudfront_distribution" "cdn" {
  origin {
    origin_id   = "S3-${module.s3_website.bucket_name}"
    domain_name = module.s3_website.regional_domain_name
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${module.s3_website.bucket_name}"

    viewer_protocol_policy = "allow-all"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}