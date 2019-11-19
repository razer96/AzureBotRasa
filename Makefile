# Set environment variables
include .env
export

# Packer commands
packer-validate:
	@echo === Validating packer config files ===
	@packer validate -var-file ./packer/vars.json ./packer/hb-azure-bot.json

packer-build: packer-validate
	@echo === Building Azure VM with packer ===
	@packer build -var-file ./packer/vars.json ./packer/hb-azure-bot.json 2>&1 | tee terraform-log

# Terraform commands
terraform-init:
	@echo === Initialize terraform ===
	@terraform init ./terraform

terraform-validate: terraform-init
	@echo === Validate terraform configuration ===
	@terraform validate ./terraform
terraform-plan: terraform-validate
	@echo === Plan terraform deployment ===
	@terraform plan -out=tfplan ./terraform

terraform-apply: terraform-plan
	@echo === Apply terraform plan ===
	@terraform apply tfplan 2>&1 | tee terraform-log

# Global commands
check: packer-validate terraform-plan
