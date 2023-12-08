#!/usr/bin/env python
# -*- coding: utf-8 -*-
gConfig = {
    "downloadThreads": 3,  #not used any more
    "downloadUsingProxy": {
        "enabled": True,
        "proxies": {
            'http': 'http://127.0.0.1:8087', 
            'https': 'https://127.0.0.1:8087'
        }
    },
    "downloadTimeout": 10   #download timeout, used by requests.get()
}

<     printf "\n    Response must be a listed numeric option\n"; manualsetup
        fi
        printf "\n    Select Internet Interface:\n"
        for i in "${!ifaces[@]}"; do
            printf "    [$(tput bold)%s$(tput sgr0)]\t%s\t" "$i" "${ifaces[$i]}"
            printf "$(ip -4 addr show ${ifaces[$i]} | grep inet | awk {'print $2'} | head -1)\n"
        done
        read -r -p "    > " inetq
        if [ "$inetq" -eq "$inetq" ] 2>/dev/null; then
            sbunnywan=(${ifaces[inetq]})
        else
            printf "\n    Response must be a listed numeric option\n"; manualsetup
        fi
        printf "\n$(netstat -nr)\n\n"
        read -r -p "    Specify Default Gateway IP Address: " sbunnygw
        savechanges
    else
        printf "\n\n    Configuration requires the 'iproute2' package (aka the 'ip' command).\n    Please install 'iproute2' to continue.\n"
        menu
    fi
}

function guidedsetup {
    bunnydetected=$(ip addr | grep '00:11:22' -B1 | awk {'print $2'} | head -1 | grep 'eth\|en')
    if [[ "$?" == 0 ]]; then
        printf "\n    Bash Bunny detected. Please disconnect the Bash Bunny from\n    this computer and $(tput bold)press any key$(tput sgr0) to continue with guided setup.\n    "
        read -r -sn1 anykey
        guidedsetup
    fi
    hasiproute2=$(which ip)
    if [[ "$?" == 1 ]]; then
        printf "\n\n    Configuration requires the 'iproute2' package (aka the 'ip' command).\n    Please install 'iproute2' to continue.\n"; menu
@@ -174,7 +168,7 @@ function guidedsetup {
    printf "\n    $(tput setaf 3)Step 3 of 3: Select Bash Bunny Interface$(tput sgr0)\n    Please connect the Bash Bunny to this computer.\n    "

    a="0"
    until bunnyiface=$(ip addr | grep '00:11:22' -B1 | awk {'print $2'} | head -1 | grep 'eth\|en')
    until bunnyiface=$(ip addr | grep '00:11:22:33:44:55' -B1 | awk {'print $2'} | head -1 | grep 'eth\|en')
    do
        printf "."
        sleep 1
@@ -186,7 +180,7 @@ function guidedsetup {
    done
    printf "[Checking]"
    sleep 5 # Wait as the system is likely to rename interface. Sleeping rather than more advanced error handling becasue reasons.
    bunnyiface=$(ip addr | grep '00:11:22' -B1 | awk {'print $2'} | head -1 | grep 'eth\|en' | sed 's/://g')
    bunnyiface=$(ip addr | grep '00:11:22:33:44:55' -B1 | awk {'print $2'} | head -1 | grep 'eth\|en' | sed 's/://g')
    printf "\n    Detected Bash Bunny on interface $(tput bold)$bunnyiface$(tput sgr0)\n";
    read -r -p "    Use the above detected Bash Bunny interface?    [Y/n]? " pi
    case $pi in
