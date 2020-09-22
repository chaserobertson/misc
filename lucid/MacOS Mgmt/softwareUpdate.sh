#!/bin/bash

# Pause automatic update check
sudo softwareupdate --schedule OFF

# Automatically check for updates (required for any downloads):
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate AutomaticCheckEnabled -bool YES

# Download updates automatically in the background
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate AutomaticDownload -bool YES

# Install app updates automatically:
sudo defaults write /Library/Preferences/com.apple.commerce AutoUpdate -bool YES

# Install system data file updates automatically:
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate ConfigDataInstall -bool YES

# Install critical security updates automatically:
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate CriticalUpdateInstall -bool YES

# Install regular MacOS updates automatically:
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate AutomaticallyInstallMacOSUpdates -bool YES

# Restart automatic update check
sudo softwareupdate --schedule ON