# lambda layer selenium_python36

data "aws_caller_identity" "current" {
}

locals {
  account_id = data.aws_caller_identity.current.account_id

  s3_bucket = format("%s-lambda-layer-%s", var.name, local.account_id)
}

resource "aws_s3_bucket" "selenium" {
  bucket = local.s3_bucket
  acl    = "private"

  force_destroy = true
}

resource "aws_s3_bucket_object" "selenium" {
  bucket = aws_s3_bucket.selenium.id
  key    = "layer/selenium_python36.zip"
  source = "${path.module}/layer/selenium_python36.zip"
}

resource "aws_lambda_layer_version" "selenium" {
  layer_name = "selenium"

  compatible_runtimes = ["python3.6"]

  s3_bucket = aws_s3_bucket.selenium.id
  s3_key    = aws_s3_bucket_object.selenium.id
}
