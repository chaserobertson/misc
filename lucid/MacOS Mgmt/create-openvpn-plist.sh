#!/bin/bash

consoleUser=$(ls -l /dev/console | awk '{ print $3 }')
dir="/Users/$consoleUser/Library/LaunchAgents"
plist="$dir/org.openvpn.toggle-dns.plist"

# Check for existence of LaunchAgents dir, create if not exist
[ ! -d "$dir" ] && mkdir "$dir" && echo "Created $dir"

# Check for existence of plist, unload if exist
[ -f "$plist" ] && sudo -u $consoleUser launchctl unload "$plist"  && echo "Unloaded launchd job"

# Create or overwrite plist
echo '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
	<dict>
		<key>Label</key>
		<string>org.openvpn.toggle-dns</string>

		<key>ProgramArguments</key>
		<array>
			<string>/bin/bash</string>
			<string>/etc/openvpn/toggle-dns.sh</string>
		</array>

		<key>WatchPaths</key>
		<array>
			<string>/Users/'$consoleUser'/Library/Application Support/OpenVPN Connect/</string>
		</array>
	</dict>
</plist>' > "$plist"

echo "Created or overwrote launchd plist"

# Load new plist
sudo -u $consoleUser launchctl load -w "$plist" && echo "Loaded launchd job"

exit 0