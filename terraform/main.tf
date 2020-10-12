# Terraform Main

terraform {
  required_version = ">= 0.12"
  backend "s3" {
    region = "ap-northeast-2"
    bucket = "terraform-nalbam-seoul"
    key    = "deepracer-submit.tfstate"
  }
}

provider "aws" {
  region = var.region
}

module "submit" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = var.name

  runtime = "python3.6"
  handler = "submit.handler"

  layers = [
    module.selenium.this_lambda_layer_arn,
  ]

  memory_size = 2048

  source_path = "${path.module}/src"
}

module "selenium" {
  source = "terraform-aws-modules/lambda/aws"

  create_layer = true

  layer_name = "selenium"

  compatible_runtimes = ["python3.6"]

  source_path = "${path.module}/layer"
}
