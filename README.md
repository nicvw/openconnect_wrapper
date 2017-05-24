# openconnect_wrapper
Wrapper script for OpenConnect on Mac OS systems

## Description

Tired of the (admittedly trivial) overhead of running openconnect from the command line and having to find and kill it once you are ready to disconnect?  Then this convenience wrapper will help you no end.

## Requirements

This script assumes you have installed OpenVPN using [Homebrew](https://brew.sh "The missing package manager for MacOS")

For ease of use I would recommend sudo rights to the openconnect executable and setting NOPASSWD, this can be done by running

`sudo visudo -f /private/etc/sudoers.d/openconnect`

and adding the following line to the file

`%admin  ALL=(ALL) NOPASSWD: /usr/local/bin/openconnect`

All this does is allow you to connect to the VPN without needing to type in your password for sudo as well as your password for the VPN.  It does **NOT** grant any special permissions to this wrapper script.

## Installation instructions

Just run `pip install git+https://github.com/nicvw/openconnect_wrapper.git`

## Usage

```
openconnect_wrapper start <openconnect arg> <openconnect arg>...
openconnect_wrapper stop
openconnect_wrapper status
```

## Example

connect to your vpn

`$ openconnect_wrapper start --user=your.username --authgroup=YOUR_AUTHGROUP vpn-server.example.net`

check the status

`$ openconnect_wrapper status`

disconnect from the vpn

`$ openconnect_wrapper stop`

## Detail

This script simply calls the OpenVPN client with **--background --pid-file --setuid** arguments plus any other arguments you pass it
