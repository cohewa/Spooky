# Privacy and permissions

Spooky is a local macOS app with an optional Safari development extension. It does not create an account, send analytics, or contact a remote service.

| Feature | Access used | What is stored |
| --- | --- | --- |
| Spider Web | Transparent windows above the menu bar | On/off setting |
| Desktop Stickers | Transparent, movable Desktop windows | On/off setting and sticker positions |
| Folder Icons | Reads Desktop folders and changes their Finder icons | Original icon backups and stable style assignments in Application Support |
| Pumpkin Wallpaper | Reads and changes wallpaper for connected displays; reads widget window geometry | Previous wallpaper paths and local backup images |
| Candy Cursor | Reads pointer position and attempts to hide the macOS arrow | On/off setting |
| Safari extension | Runs on all HTTP/HTTPS pages and frames when granted website access | No page contents or browsing history; it asks the Mac app for the cursor setting |

The Mac app listens on `127.0.0.1:47831` and exposes only five on/off values to its Safari extension. The endpoint is read-only and bound to the loopback interface. It does not enable cross-origin reads from ordinary websites. Safari site access is broad because the cursor must appear on whichever site the user is viewing. This is an explicit permission request, not hidden access.

Backups and settings remain under `~/Library/Application Support/Halloween Decor/` and macOS user defaults. Do not delete the backups while themed folder icons or wallpaper are active. Turn effects off first and check that the previous appearance returned.

Spooky does not currently provide automatic updates. Download future builds only from a release published by the repository owner, and verify the developer signature and checksum when those are available.
