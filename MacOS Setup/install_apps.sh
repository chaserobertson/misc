#! /usr/bin/env bash

# Installs Homebrew software.

if ! command -v brew > /dev/null; then
    ruby -e "$(curl --location --fail --show-error https://raw.githubusercontent.com/Homebrew/install/master/install)"
    export PATH="/usr/local/bin:$PATH"
    printf "export PATH=\"/usr/local/bin:$PATH\"\n" >> $HOME/.bash_profile
fi

printf "Updating brew\n"
brew upgrade && brew update

printf "Installing xcode cli utils\n"
xcode-select --install

printf "brew: Installing cli packages\n"
brew install git
brew install mas            # Apple store cli
brew install wakeonlan
brew install wget

# Install ZSH
brew install zsh zsh-completions zsh-autosuggestions zsh-syntax-highlighting

printf "brew: Installing apps\n"
brew cask install activitywatch
brew cask install atom
brew cask install balenaetcher
brew cask install evernote
brew cask install firefox
brew cask install google-backup-and-sync
brew cask install google-chrome
brew cask install iterm2
brew cask install lastpass
brew cask install lastpass-cli
brew cask install spotify
brew cask install the-unarchiver
brew cask install tor-browser
brew cask install virtualbox
brew cask install virtualbox-extension-pack
brew cask install visual-studio-code
brew cask install vlc
brew cask install windscribe
brew cask install wireshark
brew cask install zoomus
