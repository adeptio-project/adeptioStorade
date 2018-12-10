#!/usr/bin/env bash
#:: By adeptio dev team
#:: 2018-11-30
#:: Check for storADEserver latest version
#:: v1.0

Work_dir=$HOME/adeptioStorade/
git=$(which git)
report_as_storADE_node=$(curl -s https://storade.adeptio.cc/register_storade_node)

cd $Work_dir
new_version_available=$($git fetch origin && $git status | grep -c "git pull")

if [ "$new_version_available" -eq 0 ]; then
   echo "$date storADEserver version up-to-date"
else
   echo "$date storADEserver new version available" && sudo systemctl stop storADEserver && sleep 30 && $git pull && sudo systemctl start storADEserver
fi
