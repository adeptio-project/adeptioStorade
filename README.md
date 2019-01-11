# adeptioStorade

[![Build Status](https://development.adeptio.cc/job/Adeptio-CI-master-Weekly-Build/badge/icon)](https://development.adeptio.cc/job/storADE-CI-master-CodeTests)
[![](https://img.shields.io/jenkins/c/https/development.adeptio.cc/storADE-CI-master-CodeTests.svg)](https://development.adeptio.cc/job/storADE-CI-master-CodeTests/)
[![](https://img.shields.io/github/last-commit/adeptio-project/adeptioStorade.svg)](https://github.com/adeptio-project/adeptioStorade/commits/master)
[![](https://img.shields.io/github/release/adeptio-project/adeptioStorade.svg)](https://github.com/adeptio-project/adeptioStorade/releases)
[![](https://img.shields.io/github/issues/adeptio-project/adeptioStorade.svg)](https://github.com/adeptio-project/adeptioStorade/issues)
[![](https://img.shields.io/website-up-down-green-red/https/explorer.adeptio.cc.svg?label=storADEstats)](https://explorer.adeptio.cc)
<a href="https://discord.gg/RBXjTBa">
<img src="https://img.shields.io/discord/447850979627630603.svg?logo=discord"
alt="chat on Discord"></a>
[![](https://img.shields.io/twitter/follow/adeptioproject.svg?label=Follow&style=social)](https://twitter.com/intent/user?screen_name=adeptioproject)

v1.2 /beta testing for adeptio storage & streaming project. Code written by [Adeptio](https://github.com/adeptio-project) development team. 

Please register all bugs and issues at [Discord](https://discord.gg/RBXjTBa) (storade-issues) or [Github issues tab](https://github.com/adeptio-project/adeptioStorade/issues)

![Alt text](https://github.com/adeptio-project/adeptio/raw/master/logo/1_shadow.png)

# adeptioStorADE requirements:

• Working adeptiod with successfully started masternode:

• Ubuntu 16.04 LTS or Ubuntu 18.04 LTS;

• Python 2.7 or greater version;

• 2 or more CPU Cores;

• At least 10GB free space;

• At least 1024MB memory space;

• 100 Mbps bandwidth up/down speed or greater;

• An open firewall for 9079/tcp/udp port;

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

4.1 Create auto updater for storADEupdater service:

    echo \
    "[Unit]
    Description=storADEupdater.service
 
    [Service]
    Type=oneshot
    WorkingDirectory=$HOME/adeptioStorade
    ExecStart=$HOME/adeptioStorade/storADEserver-updater.sh
    PrivateTmp=true" | sudo tee /etc/systemd/system/storADEupdater.service
   
4.2 Create timer for storADEupdater service:

    echo \
    "[Unit]
    Description=Run storADEupdater unit daily @ 00:00:00 (UTC)
 
    [Timer]
    OnCalendar=*-*-* 00:00:00
    Unit=storADEupdater.service
    Persistent=true
 
    [Install]
    WantedBy=timers.target" | sudo tee /etc/systemd/system/storADEupdater.timer
    
4.3 Change permissions:

    sudo chmod 664 /etc/systemd/system/storADEupdater.service
    sudo chmod 664 /etc/systemd/system/storADEupdater.timer
    
4.4 Enable & start the storADEupdater.service & storADEupdater.timer   

    sudo systemctl start storADEupdater.service
    sudo systemctl start storADEupdater.timer
    sudo systemctl enable storADEupdater.service
    sudo systemctl enable storADEupdater.timer

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
    RestartSec=3600
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

9.0 Update the Firewall:

    sudo ufw allow 9079/tcp
    sudo ufw allow 9079/udp

10.0 Star a service:

    sudo systemctl start storADEserver.service
    
# Check the status (debug):

11.1 Check the storADEserver status:

    sudo systemctl status storADEserver.service

11.2 Check the adeptiocore status:

    sudo systemctl status adeptiocore.service && /usr/bin/adeptio-cli getinfo

11.3 Good idea is to check the storADE logs (Optional):

    tail -n 30 ~/adeptioStorade/storage/storADE.log

11.4 If something not working we can check storADEserver process logs (Optional):

    journalctl --since today -u storADEserver

Need help? [Discord](https://discord.gg/RBXjTBa) 
