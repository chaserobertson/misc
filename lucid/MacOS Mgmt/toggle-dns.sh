#!/bin/bash

# VPN DNS Servers
vpndns=("8.8.8.8 1.1.1.1")

# VPN subnet
vpninterface="inet 10.3."

# Get list of all subnets
interfaces=`ifconfig | grep inet`

# Determine if VPN subnet is listed aka VPN is connected
if [[ "$interfaces" = *"$vpninterface"* ]]; then
    echo "VPN Connected: Configuring DNS server addresses."
else
    echo "VPN Not Connected: Resetting DNS to DHCP provided servers."
fi

# Get adapter list
IFS=$"\n" adapters=`networksetup -listallnetworkservices | grep -v denotes`

for adapter in $adapters
do
        dnssvr=(`networksetup -getdnsservers $adapter`)

        if [[ "$interfaces" = *"$vpninterface"* ]]; then
            # set dns server to the vpn dns servers
            echo configuring dns for $adapter
            networksetup -setdnsservers $adapter ${vpndns[@]}
        else
            # revert back to DHCP assigned DNS Servers
            echo resetting dns for $adapter
            networksetup -setdnsservers $adapter empty
        fi
done