resource "azurerm_resource_group" "hb-azure-bot" {
  name     = "hb-azure-bot"
  location = "North Europe"

  tags = {
    environment = "Production"
    application = "hb-azure-bot"
  }
}

data "azurerm_image" "rasa" {
  name                = "rasa"
  resource_group_name = "DevOps"
}

resource "azurerm_virtual_machine" "hb-azure-bot-vm" {
  name                  = "hb-azure-bot-vm"
  location              = "${azurerm_resource_group.hb-azure-bot.location}"
  resource_group_name   = "${azurerm_resource_group.hb-azure-bot.name}"
  network_interface_ids = ["${azurerm_network_interface.hb_azure_bot_private_nic.id}"]
  vm_size               = "Standard_B1ms"

  delete_os_disk_on_termination    = true
  delete_data_disks_on_termination = true

  storage_image_reference {
    id = "${data.azurerm_image.rasa.id}"
  }

  storage_os_disk {
    name              = "hb-azure-bot-vm-os-disk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  os_profile {
    computer_name  = "hb-azure-bot"
    admin_username = "hb-azure-bot-admin"
    admin_password = "1q2w3e4r%T"
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }

  tags = {
    environment = "Production"
    application = "hb-azure-bot"
  }
}
