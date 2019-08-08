# PurgeApp
Cleanly uninstall a macOS application by also removing related files and directories.

###### Inspired by: [hrik2001/macuninstaller](https://github.com/hrik2001/macuninstaller)

### Usage
```
./purge_app.py '/Applications/Example.app'
```

#### Example
```
$ ./purge_app.py '/Applications/OneDrive.app'

* Searching for app-related data...
 - /Library/LaunchDaemons/com.microsoft.OneDriveUpdaterDaemon.plist
 - /var/db/receipts/com.microsoft.OneDrive.bom
 - /var/db/receipts/com.microsoft.OneDrive.plist
 - /Users/codesamuraii/Library/Group Containers/UBF8T346G9.OfficeOneDriveSyncIntegration

* Delete (along with the app) ? [y/N] y
* Done !
```

### Note
This software is still in development. Double check the path you give as an argument or you may delete files you don't want to delete.
