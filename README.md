# openconnect_wrapper
Wrapper script for OpenConnect on Mac OS systems

## Description

Tired of running OpenConnect in a foreground window, or have to find and kill the process once you are finished needing a VPN connection?  Then this convenience wrapper will help you no end.

## Requirements

This script assumes you have installed OpenVPN using [Homebrew](https://brew.sh "The missing package manager for MacOS")

## Installation instructions

Just run `pip install git+https://github.com/nicvw/openconnect_wrapper.git`

## Usage

```
openconnect_wrapper start <openconnect arg> <openconnect arg>...
openconnect_wrapper stop
openconnect_wrapper status
```

## Detail

This script simply implements calls the OpenVPN client with **--background --pid-file --setuid** arguments and any other arguments you pass it
