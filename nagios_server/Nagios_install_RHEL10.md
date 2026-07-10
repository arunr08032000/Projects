### 🔹 1. Prerequisites
Update system
sudo dnf update -y

### Install required packages
```
sudo dnf install -y
httpd php php-cli php-common php-gd php-mbstring
gcc glibc glibc-common wget unzip
make autoconf automake
openssl-devel perl net-snmp net-snmp-utils
gd gd-devel
```

### Enable & start Apache:

```
sudo systemctl enable httpd
sudo systemctl start httpd
```

### 🔹 2. Create Nagios User & Groups
```
sudo useradd nagios
sudo groupadd nagcmd
sudo usermod -aG nagcmd nagios
sudo usermod -aG nagcmd apache
```

### 🔹 3. Download Nagios Core
```
cd /tmp
wget https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.4.14.tar.gz
tar -xzf nagios-4.4.14.tar.gz
cd nagios-4.4.14
```

### 🔹 4. Compile & Install Nagios
```
./configure --with-command-group=nagcmd
make all
```

### Install components:
```
sudo make install
sudo make install-init
sudo make install-commandmode
sudo make install-config
sudo make install-webconf
```

### 🔹 5. Set Nagios Web UI Password

    sudo htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin

(Enter password when prompted)

Restart Apache:

sudo systemctl restart httpd

🔹 6. Install Nagios Plugins
cd /tmp
wget https://nagios-plugins.org/download/nagios-plugins-2.4.6.tar.gz
tar -xzf nagios-plugins-2.4.6.tar.gz
cd nagios-plugins-2.4.6

Compile & install:

./configure --with-nagios-user=nagios --with-nagios-group=nagios
make
sudo make install

🔹 7. Verify Nagios Configuration
/usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg

✔️ You should see:

Total Warnings: 0
Total Errors: 0

🔹 8. Start Nagios Service
sudo systemctl enable nagios
sudo systemctl start nagios

Check status:

systemctl status nagios

🔹 9. Open Firewall (Important)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload

🔹 10. Access Nagios Web UI

Open browser:

http://<server-ip>/nagios

Login:

Username: nagiosadmin

Password: (you created earlier)

🔹 Common Paths (Important for Admins)
Component 	Path
Nagios binary 	/usr/local/nagios/bin/nagios
Config file 	/usr/local/nagios/etc/nagios.cfg
Objects 	/usr/local/nagios/etc/objects/
Plugins 	/usr/local/nagios/libexec/
Logs 	/usr/local/nagios/var/nagios.log
