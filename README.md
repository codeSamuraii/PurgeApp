# PurgeApp
Cleanly uninstall a macOS application by also removing related files and directories.

###### Inspired by: [hrik2001/macuninstaller](https://github.com/hrik2001/macuninstaller)

### Usage
```sh
python purge_app.py /Applications/Example.app
```
or
```sh
./purge_app.py /Applications/Example.app
```
>You may need to `chmod +x purge_app.py` once before to allow execution.

#### Example
```
$ ./purge_app.py /Applications/Adium.app
- Reading app informations...
  > /Applications/Adium.app

- Identifiers found:
  > com.adiumX.adiumX       use? (Y/n) y
  > Adium                   use? (Y/n) y
  > AdIM                    use? (Y/n) n    # Short and generic, might cause false positives.

- Searching for app-related data (may take a while)...
  > '/Users/me/Library/Application Support/Adium 2.0' (y/N/skip) y
  > '/Users/me/Library/Address Book Plug-Ins/AdiumAddressBookAction_ICQ.scpt' (y/N/skip) y
  > '/Users/me/Library/Address Book Plug-Ins/AdiumAddressBookAction_AIM.scpt' (y/N/skip) y
  > '/Users/me/Library/Address Book Plug-Ins/AdiumAddressBookAction_SMS.scpt' (y/N/skip) s
  Skipped: '/Users/me/Library/Address Book Plug-Ins/'
  > '/Users/me/Library/Preferences/com.adiumX.adiumX.plist' (y/N/skip) y
  > '/Users/me/Library/Caches/Adium' (y/N/skip) y
  > '/Users/me/Library/Caches/com.adiumX.adiumX' (y/N/skip) y

- Delete the app itself ? [y/N] y
* Done !
```
Use `y` to accept a choice, `n` to refuse and `s` to skip that folder.

### Warning
This software is still in development, please use with caution!
- Do not use short identifiers (eg. `port` will catch `WeatherReport`)
- Check every path before deleting.
- Only run as root if you know what you're doing.
