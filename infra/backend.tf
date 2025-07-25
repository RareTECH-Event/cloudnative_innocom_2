
terraform {
  backend "s3" {
    bucket = "terraform-state-cloudnative-innocom-osaka-017121236507" # ★★★ 要変更: Terraformの状態を保存するS3バケット名
    key    = "cloudnative-innocom/terraform.tfstate"
    region = "ap-northeast-3"
  }
}
