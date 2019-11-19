# AzureBot

Azure bot has been created as a server for registration process automatization. 

The main framework used for development of the bot is RASA.

Packer and Terraform are used for environment configuration. Packer builds OS image and Terraform creates Virtual Machine in Azure Cloud with Packer images installed on it.


Running process using docker-compose:
  1. Training the modal: ``` rasa train ```
  2. Run docker-compose: ``` docker-compose up -d ```
