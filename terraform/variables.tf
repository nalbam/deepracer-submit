# variable

variable "region" {
  default = "us-east-1"
}

variable "name" {
  default = "deepracer-submit"
}

variable "build_no" {
  default = "0"
}

variable "s3_bucket" {
  default = "repo.deepracer.nalbam.com"
}

variable "USERNO" {
  default = "123456789012"
}

variable "USERNAME" {
  default = "username"
}

variable "PASSWORD" {
  default = "password"
}

variable "LEAGUE" {
  default = "competition/arn%3Aaws%3Adeepracer/submitModel"
}

variable "MODEL" {
  default = "my-model"
}
