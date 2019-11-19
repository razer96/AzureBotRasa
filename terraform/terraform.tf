terraform {
  backend "azurerm" {
    resource_group_name  = "DevOps"
    storage_account_name = "uirhbdevops"
    container_name       = "tfstate"
    key                  = "hb-azure-bot.prod.tfstate"
  }
}

provider "azurerm" {
  version = "=1.28.0"
}
