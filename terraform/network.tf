# Define network resources
resource "azurerm_virtual_network" "hb_azure_bot_vnet" {
  name                = "hb-azure-bot-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = "${azurerm_resource_group.hb-azure-bot.location}"
  resource_group_name = "${azurerm_resource_group.hb-azure-bot.name}"

  tags = {
    environment = "Production"
    application = "HB-Azure-Bot"
  }
}

resource "azurerm_subnet" "hb_azure_bot_snet" {
  name                 = "hb-azure-bot-subnet"
  resource_group_name  = "${azurerm_resource_group.hb-azure-bot.name}"
  virtual_network_name = "${azurerm_virtual_network.hb_azure_bot_vnet.name}"
  address_prefix       = "10.0.1.0/24"
}

resource "azurerm_public_ip" "hb_azure_bot_vm_pip" {
  name                    = "hb-azure-bot-vm-pip"
  location                = "${azurerm_resource_group.hb-azure-bot.location}"
  resource_group_name     = "${azurerm_resource_group.hb-azure-bot.name}"
  allocation_method       = "Dynamic"
  idle_timeout_in_minutes = 30

  tags = {
    environment = "Production"
    application = "hb-azure-bot"
  }
}

resource "azurerm_network_interface" "hb_azure_bot_private_nic" {
  name                = "hb-azure-bot-vm-nic"
  location            = "${azurerm_resource_group.hb-azure-bot.location}"
  resource_group_name = "${azurerm_resource_group.hb-azure-bot.name}"

  ip_configuration {
    name                          = "privateIPConfig"
    subnet_id                     = "${azurerm_subnet.hb_azure_bot_snet.id}"
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = "${azurerm_public_ip.hb_azure_bot_vm_pip.id}"
  }

  tags = {
    environment = "Production"
    application = "hb-azure-bot"
  }
}
