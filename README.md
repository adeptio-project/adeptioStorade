# adeptioStorade
v1.0 alpha testing for adeptio storage & streaming project

![Alt text](https://blog.adeptio.cc/wp-content/uploads/2018/11/Selection_105.png)

# adeptioStorADE requirements:

• Python 2.7 or greater version

• 2 or more CPU Cores;

• At least 10GB free space;

• At least 1024MB memory space;

• 100 Mbps bandwidth up/down speed or greater;

• An open firewall for 9079/tcp/udp port

• Python OpenSSL module;

# How to install:

1.0 Install dependencies for Python OpenSSL:

    sudo apt-get update -y
    sudo apt-get install python-openssl -y

2.0 Make sure you have working adeptiod & adeptio-cli daemon at path:

    /usr/bin/adeptiod
    /usr/bin/adeptio-cli

3.0 Go to your home directory & copy storADE content from github:

    cd ~/
    git clone https://github.com/adeptio-project/adeptioStorade.git

4.0 Add autoupdater to crontab job:

    crontab -l | { cat; echo "0 0 * * * $HOME/adeptioStorade/storADEserver-updater.sh"; } | crontab -

5.0 Create a systemd process storADEserver.service file

    sudo echo \
    "[Unit]
    Description=Adeptio storADEserver daemon for encrypted file storage
    After=network.target
    [Service]
    User=$USER
    Type=simple
    WorkingDirectory=$HOME/adeptioStorade
    ExecStart=$(which python) $HOME/adeptioStorade/storADEserver.py
    Restart=always
    Restart=on-failure
    RestartSec=60
    [Install]
    WantedBy=default.target" | sudo tee /etc/systemd/system/storADEserver.service

6.1 Check if user is root? If false - create sudoers files to manage systemd services for auto updater:

    echo $EUID

6.2 If the output is not 0 follow the next:

    sudo su
    nano /etc/sudoers.d/storADEserver

6.3 Rename the line - "yourUSERnameHERE" & paste the lines:
    %yourUSERnameHERE ALL= NOPASSWD: /bin/systemctl start storADEserver
    %yourUSERnameHERE ALL= NOPASSWD: /bin/systemctl stop storADEserver
    %yourUSERnameHERE ALL= NOPASSWD: /bin/systemctl restart storADEserver

6.4 Save the file first. Then exit from root user:

    exit

7.0 Change permissions for storADEserver.service:

    sudo chmod 664 /etc/systemd/system/storADEserver.service

8.0 Enable service after reboot:

    sudo systemctl enable storADEserver.service

9.0 Star a service:

    sudo systemctl start storADEserver.service

10.0 Check the status:

    sudo systemctl status storADEserver.service
