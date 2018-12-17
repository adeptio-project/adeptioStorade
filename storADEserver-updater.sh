#!/usr/bin/env bash
#:: By adeptio dev team
#:: 2018-12-17
#:: Check for storADEserver latest version
#:: v1.0

Work_dir=$HOME/adeptioStorade/
git=$(which git)
report_as_storADE_node=$(curl -s https://storade.adeptio.cc/register_storade_node)

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
