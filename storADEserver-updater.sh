#!/usr/bin/env bash
#:: By adeptio dev team
#:: 2018-11-30
#:: Check for storADEserver latest version
#:: v2.2

Work_dir=/$USER/adeptioStorade/
git=$(which git)

cd $Work_dir
new_version_available=$($git fetch origin && $git status | grep -c "git pull")

if [ "$new_version_available" -eq 0 ]; then
   echo "$date storADEserver version up-to-date"
else
   echo "$date storADEserver new version available" && systemctl stop storADEserver && sleep 30 && $git pull && systemctl start storADEserver
fi
