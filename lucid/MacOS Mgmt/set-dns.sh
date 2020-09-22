#!/bin/bash

# These are the DNS servers to lock in, change to 2 to reset
DNSServers1="8.8.8.8 1.1.1.1"
DNSServers2=empty

# List all Network Devices that are availabe on MacOS
NetworkServices=$(networksetup -listallnetworkservices)

# Create an array arr of network services, then split it by newline
IFS=$'\n' read -r -d '' -a array < <(printf '%s\0' "$NetworkServices")
arr=("${array[@]}")

# Interate through all network services
for i in ${!arr[*]}
do
  # Skip the first item, it's an OS message, not a Service
  if [[ $i > 0 ]]
  then
    Service=${arr[$i]}

    # Set the DNS Servers for this service
    $(networksetup -setdnsservers "$Service" $DNSServers2)
    echo $(networksetup -getdnsservers "$Service")
  fi
done
