# Implementation notes

The six independent setting keys are `webs`, `skeletons`, `stickers`, `folders`, `wallpaper`, and `cursor`. The menu bar app is the source of truth. It exposes a read-only JSON snapshot over loopback for the temporary Safari extension, which updates visible pages by polling. This bridge contains no page content and accepts no configuration writes.

The desktop implementation uses public AppKit APIs: NSWindow for movable stickers, NSWorkspace for Desktop folder icons and wallpaper, and NSStatusItem for the single menu. The Safari content script creates one click-through overlay on each ordinary web page. It respects `prefers-reduced-motion`.

The temporary Safari installation and local HTTP bridge are a development path. A packaged Safari Web Extension would use native messaging and app groups as described in Apple's Safari documentation. It requires a full Xcode installation, currently absent from this Mac.

`demo/index.html` is a local visual preview with simulated settings. It does not verify Safari extension loading or native messaging.
