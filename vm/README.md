After running Ansible scripts through Vagrant, it is possible that RVM is not correctly installed. To make sure, get inside the VM, and run the following commands at /var/www/html/

```
rvm requirements
rvm install 2.1.5
rvm use 2.1.5 --default
```

Then, set up Gems and modules at the same folder (/var/www/html) by running:
```
gem install bundle # if you don't already have it
bundle
sudo npm install
```

Inside the VM, it is possible that Nodejs' symbolic link is not correctly generated. In you have an error about Nodejs, make a symbolic link:
```
ln -s /usr/bin/nodejs /usr/bin/node
```
