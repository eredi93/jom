project_home_dir = "/var/www/jom"
server_ip = "192.168.33.10"
args = "-a 192.168.33.0/24 -d /var/www/jom"

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "jom"
  config.vm.network "private_network", ip: server_ip
  config.vm.synced_folder ".", "/vagrant", id: "vagrant-root", disabled: true
  config.vm.synced_folder ".", project_home_dir
  config.vm.provision "shell", path: "install.sh", args: args

  config.vm.provider "virtualbox" do |vb|
    vb.name = "jom"
    vb.memory = "1024"
  end
end
