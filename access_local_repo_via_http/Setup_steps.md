Step 1: Install Apache & SSL module

    sudo apt update
    sudo apt install apache2 -y
    sudo a2enmod ssl
    sudo systemctl restart apache2

Verify Apache:

    http://localhost or http://<your ip address>

Step 2: Point Apache to your Public folder

    sudo nano /etc/apache2/sites-available/public.conf

Paste this 👇 (replace arun if username differs):
```sh
<VirtualHost *:80>
    ServerName localhost
    DocumentRoot /home/arun/Public

    <Directory /home/arun/Public>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
```

Enable site:

    sudo a2ensite public.conf
    sudo systemctl reload apache2

Test:

    http://localhost or http://<your-ip-address>

Step 3: Fix folder permissions (VERY IMPORTANT)
Apache must read your home directory:

    chmod 755 /home/arun
    chmod 755 /home/arun/Public

Step 4: Enable HTTPS (SSL)

Option A: Self-signed certificate (Quick & offline)

    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/public.key \
    -out /etc/ssl/certs/public.crt

Step 5: Create HTTPS VirtualHost

    sudo nano /etc/apache2/sites-available/public-ssl.conf

Paste:
```sh
<VirtualHost *:443>
    ServerName localhost
    DocumentRoot /home/arun/Public

    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/public.crt
    SSLCertificateKeyFile /etc/ssl/private/public.key

    <Directory /home/arun/Public>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
```

Enable SSL site:

    sudo a2ensite public-ssl.conf
    sudo systemctl reload apache2

Step 6: Allow HTTPS in firewall (if enabled)

    sudo ufw allow https
    sudo ufw reload
    
Step 7: Access your Public folder via HTTPS

Open browser:

    https://localhost or https://<your-ip-address>
    
⚠️ Browser warning is normal for self-signed cert → click Advanced → Proceed

(Optional) Redirect HTTP → HTTPS

Edit HTTP config:
    
    sudo nano /etc/apache2/sites-available/public.conf

Add inside <VirtualHost *:80>:

    Redirect / https://localhost/
    
Reload:

    sudo systemctl reload apache2

