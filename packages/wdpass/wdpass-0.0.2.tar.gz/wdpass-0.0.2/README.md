# wdpass
WD Passport Ultra Complete Utilities for Linux.

Thanks to:
- [Dan Lenski](https://github.com/dlenski) for [py_sg](https://pypi.org/project/py_sg/) (Python2)
- [0-duke](https://github.com/0-duke) and [derekhe](https://github.com/derekhe) for [wdpassport-utils](https://github.com/derekhe/wdpassport-utils) (Python2)
- [crypto-universe](https://github.com/crypto-universe/) for Python3 migration of [py_sg](https://github.com/crypto-universe/py_sg) and [wdpassport-utils](https://github.com/crypto-universe/wdpassport-utils)

## Intro

This script let you unlock, change password and erase Western Digital Passport devices on Linux platform. 

## Install

### Install Dependencies:
- `lsscsi` package or any package provides `lsscsi` command.
- `<Python.h>` header file in libraries. (`python3-dev` or `python3-devel` package)

For example on Fedora:

```shell
sudo dnf install lsscsi python3-devel
```

### Install `wdpass`
```shell
sudo python3 -m pip install wdpass
```

## Usage

Run script as root. 

There are few options:
```
-h, --help            show this help message and exit
```
Lists all possible arguments.

```
-s, --status          Check device status and encryption type
```
Get device encryption status and cipher suites used.
```
-u, --unlock          Unlock
```
You will be asked to enter the unlock password. If everything is fine device will be unlocked.

```
-us, --unlock_with_saved_passwd Unlock with the password saved
```
Unlock using the saved password. If everything is fine device will be unlocked.

```
-sp, --save_passwd    Save password
```
When unlock password, it will save user password to passwd.bin, so you can use "-us" for next time to auto unlock.

```
-m, --mount           Enable mount point for an unlocked device
```
After unlock, your operating system still thinks that your device is a strange thing attached to his usb port and he don't know how to manage. You need this option to force the O.S. to rescan the device and handle it as a normal external usb harddrive.

```
-c, --change_passwd   Change (or disable) password
```
This option let you to encrypt your device, remove password protection and change your current password.
If device is "without lock" and you want it to be password protect leave the "OLD password" field empty and choose insert the new password.
If the device is password protected and you want to be as a normal unencrypted device, inser the old password and leave the "NEW password" field empty.
If you only want to change password do it as usual.

```
-e, --erase           Secure erase device
```
"Erase" the device. This will remove the internal key associated to you password and all your data will be unaccessible. You will also lose your partition table and you will need to create a new one (you can use fdisk and mkfs).

```
-d DEVICE, --device DEVICE  Force device path (ex. /dev/sdb). Usually you don't need this option.
```
The script will try to auto detect the current device path of your WD Passport device.
If something is wrong or you want to manually specify the device path yourself you can use this option.

## Disclaimer
I'm in no way sponsored by or connected with Western Digital.
Use any of the information contained in this repository at your own risk. I accept no
responsibility.
