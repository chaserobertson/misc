#! /usr/bin/env bash

# Apply machine hostname
read -p "What is this machine's label (Example: \"chafe\")? " mac_os_label
if [[ -z "$mac_os_label" ]]; then
    printf "ERROR: Invalid MacOS label.\n"
    exit 1
fi

read -p "What is this machine's name (Example: \"chafe\")? " mac_os_name
if [[ -z "$mac_os_name" ]]; then
    printf "ERROR: Invalid MacOS name.\n"
    exit 1
fi

printf "Setting system label and name...\n"
sudo scutil --set ComputerName $mac_os_label
sudo scutil --set HostName $mac_os_name
sudo scutil --set LocalHostName $mac_os_name
sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.smb.server NetBIOSName -string $mac_os_name

printf "Disabling guest user..\n"
sudo dscl . -delete /Users/Guest
sudo security delete-generic-password -a Guest -s com.apple.loginwindow.guest-account -D "application password" /Library/Keychains/System.keychain
sudo defaults write /Library/Preferences/com.apple.loginwindow GuestEnabled -bool FALSE

# Applies system and application defaults.

printf "System - Enabling Dark mode\n"
defaults write NSGlobalDomain AppleInterfaceStyle Dark

printf "System - Disable boot sound effects\n"
sudo nvram SystemAudioVolume=" "

printf "System - Expand save panel by default\n"
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode -bool true

printf "System - Disable the 'Are you sure you want to open this application?' dialog\n"
defaults write com.apple.LaunchServices LSQuarantine -bool false

printf "System - Disable auto-correct\n"
defaults write NSGlobalDomain NSAutomaticSpellingCorrectionEnabled -bool false

printf "System - Disable smart quotes\n"
defaults write NSGlobalDomain NSAutomaticQuoteSubstitutionEnabled -bool false

printf "System - Disable smart dashes\n"
defaults write NSGlobalDomain NSAutomaticDashSubstitutionEnabled -bool false

printf "System - Require password immediately after sleep or screen saver begins\n"
defaults write com.apple.screensaver askForPassword -int 1
defaults write com.apple.screensaver askForPasswordDelay -int 0

printf "System - Avoid creating .DS_Store files on network & USB volumes\n"
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true
defaults write com.apple.desktopservices DSDontWriteUSBStores -bool true

printf "System - Don't chime when power is plugged in\n"
defaults write com.apple.PowerChime ChimeOnAllHardware -bool false

printf "System - Disable autocorrect\n"
defaults write -g NSAutomaticSpellingCorrectionEnabled -bool false

printf "System - Disable Bonjour\n"
sudo defaults write /System/Library/LaunchDaemons/com.apple.mDNSResponder.plist ProgramArguments -array-add "-NoMulticastAdvertisements"

printf "Bluetooth - Increase sound quality for headphones/headsets\n"
defaults write com.apple.BluetoothAudioAgent "Apple Bitpool Min (editable)" -int 40

printf "Dock - Remove all default app icons\n"
defaults write com.apple.dock persistent-apps -array

printf "Dock - Automatically hide and show\n"
defaults write com.apple.dock autohide -bool true

printf "Dock - Remove the auto-hiding delay\n"
defaults write com.apple.dock autohide-delay -float 0

printf "Dock - Don’t show Dashboard as a Space\n"
defaults write com.apple.dock "dashboard-in-overlay" -bool true

printf "iCloud - Save to disk by default\n"
defaults write NSGlobalDomain NSDocumentSaveNewDocumentsToCloud -bool false

printf "Finder - Show the $HOME/Library folder\n"
chflags nohidden $HOME/Library

printf "Finder - Show hidden files\n"
defaults write com.apple.finder AppleShowAllFiles -bool true

printf "Finder - Show filename extensions\n"
defaults write NSGlobalDomain AppleShowAllExtensions -bool true

printf "Finder - Show path bar\n"
defaults write com.apple.finder ShowPathbar -bool true

printf "Finder - Show status bar\n"
defaults write com.apple.finder ShowStatusBar -bool true

printf "Finder - Use list view in all Finder windows\n"
defaults write com.apple.finder FXPreferredViewStyle -string "clmv"

printf "Finder - Allow text selection in Quick Look\n"
defaults write com.apple.finder QLEnableTextSelection -bool true

printf "Chrome - Prevent native print dialog, use system dialog instead\n"
defaults write com.google.Chrome DisablePrintPreview -boolean true

printf "TextEdit - Use plain text mode for new documents\n"
defaults write com.apple.TextEdit RichText -int 0

printf "TextEdit - Open and save files as UTF-8 encoding\n"
defaults write com.apple.TextEdit PlainTextEncoding -int 4
defaults write com.apple.TextEdit PlainTextEncodingForWrite -int 4

printf "Printer - Expand print panel by default\n"
defaults write NSGlobalDomain PMPrintingExpandedStateForPrint -bool true

printf "Printer - Automatically quit printer app once the print jobs complete\n"
defaults write com.apple.print.PrintingPrefs "Quit When Finished" -bool true

printf "Game Center - Disable Game Center\n"
defaults write com.apple.gamed Disabled -bool true

printf "App Store - Enable the WebKit Developer Tools in the Mac App Store\n"
defaults write com.apple.appstore WebKitDeveloperExtras -bool true

printf "App Store - Enable Debug Menu in the Mac App Store\n"
defaults write com.apple.appstore ShowDebugMenu -bool true

printf "You should reboot now\n"
