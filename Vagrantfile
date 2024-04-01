# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-22.04-arm64"

  config.vm.provider "vmware_fusion" do |v|
    v.gui = true
  end

  config.vm.hostname = "ecorp_webserver"
  config.vm.network "private_network", ip: "192.168.13.37"
  # Mount the app folder as a volume inside the virtual machine
  config.vm.synced_folder "./app", "/vagrant/app"

  # Shell provisioner to set up the environment
  config.vm.provision "shell", inline: <<-SHELL
    # Update apt and install necessary packages
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip sqlite3

    # Install requirements for the Flask app
    sudo pip3 install -r /vagrant/app/requirements.txt

    # Start the Flask application
    cd /vagrant/app
    python3 app.py &
  SHELL
end

