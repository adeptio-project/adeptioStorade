#!/usr/bin/env bash
#:: By adeptio dev team
#:: 2019-04-30
#:: Check for storADEserver latest version
#:: v1.2

Work_dir=$HOME/adeptioStorade/
git=$(which git)

cd $Work_dir
new_version_available=$($git fetch origin && $git status | grep -c "git pull")

service_stop_sleep=5
random_sleep=$(echo $(($RANDOM % 100)))

if [ "$new_version_available" -eq 0 ]; then
   echo "$date storADEserver version up-to-date"
else
   echo "$date storADEserver new version available";
   sleep $random_sleep; 
   sudo systemctl stop storADEserver; 
   sleep $service_stop_sleep; 
   $git pull;
   sudo systemctl start storADEserver
fi
