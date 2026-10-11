import AppKit
import AVFoundation
import Network
import Darwin

private enum Effect: String, CaseIterable {
    case webs, skeletons, stickers, folders, wallpaper, cursor
    var title: String {
        switch self {
        case .webs: return "Safari Spiderwebs"
        case .skeletons: return "Falling Skeletons"
        case .stickers: return "Desktop Stickers"
        case .folders: return "Autumn Folder Icons"
        case .wallpaper: return "Autumn Wallpaper"
        case .cursor: return "Halloween Cursor"
        }
    }
    var detail: String {
        switch self {
        case .webs: return "Delicate webs in the top corners of pages"
        case .skeletons: return "Two or three appear occasionally, without sound"
        case .stickers: return "Three stickers you can move around"
        case .folders: return "Folders on your desktop"
        case .wallpaper: return "A warm autumn scene"
        case .cursor: return "A themed pointer on web pages"
        }
    }
}

private final class PreviewCard: NSView {
    let effect: Effect
    var onSelect: ((Effect) -> Void)?
    private let player: AVPlayer
    private var endObserver: NSObjectProtocol?
    private let status = NSSwitch()
    init(effect: Effect, active: Bool, video: URL?, frame: NSRect) {
        self.effect = effect
        if let video { player = AVPlayer(url: video) } else { player = AVPlayer() }
        super.init(frame: frame)
        wantsLayer = true
        layer?.backgroundColor = NSColor(calibratedRed: 1, green: 0.987, blue: 0.96, alpha: 1).cgColor
        layer?.cornerRadius = 17
        layer?.borderWidth = 1
        layer?.borderColor = NSColor(calibratedRed: 0.74, green: 0.59, blue: 0.45, alpha: 0.35).cgColor
        let videoLayer = AVPlayerLayer(player: player)
        videoLayer.frame = CGRect(x: 10, y: 62, width: frame.width - 20, height: 108)
        videoLayer.videoGravity = .resizeAspectFill
        videoLayer.cornerRadius = 11
        videoLayer.masksToBounds = true
        videoLayer.backgroundColor = NSColor(calibratedRed: 0.25, green: 0.16, blue: 0.18, alpha: 1).cgColor
        layer?.addSublayer(videoLayer)
        let title = NSTextField(labelWithString: effect.title)
        title.font = .systemFont(ofSize: 15, weight: .semibold)
        title.textColor = NSColor(calibratedRed: 0.27, green: 0.16, blue: 0.13, alpha: 1)
        title.frame = NSRect(x: 17, y: 34, width: frame.width - 115, height: 21)
        addSubview(title)
        let detail = NSTextField(labelWithString: effect.detail)
        detail.font = .systemFont(ofSize: 11)
        detail.textColor = NSColor(calibratedRed: 0.48, green: 0.39, blue: 0.34, alpha: 1)
        detail.frame = NSRect(x: 17, y: 14, width: frame.width - 112, height: 17)
        addSubview(detail)
        status.target = self
        status.action = #selector(didSelect)
        status.setAccessibilityLabel(effect.title)
        status.frame = NSRect(x: frame.width - 75, y: 25, width: 55, height: 28)
        addSubview(status)
        setActive(active)
        player.isMuted = true
        player.actionAtItemEnd = .none
        if let current = player.currentItem {
            endObserver = NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime, object: current, queue: .main) { [weak self] _ in
                self?.player.seek(to: .zero)
                self?.player.play()
            }
            player.play()
        }
    }
    required init?(coder: NSCoder) { fatalError() }
    deinit { if let endObserver { NotificationCenter.default.removeObserver(endObserver) }; player.pause() }
    func pausePreview() { player.pause() }
    func resumePreview() { if player.currentItem != nil { player.play() } }
    func setActive(_ active: Bool) {
        status.state = active ? .on : .off
        layer?.borderColor = (active ? NSColor(calibratedRed: 0.77, green: 0.35, blue: 0.18, alpha: 1) : NSColor(calibratedRed: 0.74, green: 0.59, blue: 0.45, alpha: 0.35)).cgColor
        layer?.borderWidth = active ? 2 : 1
    }
    @objc private func didSelect() { onSelect?(effect) }
    override func mouseDown(with event: NSEvent) { onSelect?(effect) }
}

private final class StickerView: NSView {
    let kind: Int
    init(kind: Int) { self.kind = kind; super.init(frame: NSRect(x: 0, y: 0, width: 112, height: 112)) }
    required init?(coder: NSCoder) { fatalError() }
    override func draw(_ dirtyRect: NSRect) {
        let c = NSGraphicsContext.current?.cgContext
        c?.setShadow(offset: CGSize(width: 2, height: -4), blur: 7, color: NSColor.black.withAlphaComponent(0.24).cgColor)
        switch kind {
        case 0:
            NSColor(calibratedRed: 0.92, green: 0.43, blue: 0.14, alpha: 1).setFill()
            for x in [28.0, 43.0, 58.0] { NSBezierPath(ovalIn: NSRect(x: x, y: 21, width: 37, height: 61)).fill() }
            NSColor(calibratedRed: 0.35, green: 0.31, blue: 0.13, alpha: 1).setFill()
            NSBezierPath(roundedRect: NSRect(x: 52, y: 75, width: 9, height: 20), xRadius: 3, yRadius: 3).fill()
            NSColor(calibratedRed: 0.35, green: 0.15, blue: 0.11, alpha: 1).setFill()
            NSBezierPath(ovalIn: NSRect(x: 42, y: 52, width: 6, height: 8)).fill()
            NSBezierPath(ovalIn: NSRect(x: 64, y: 52, width: 6, height: 8)).fill()
            let smile = NSBezierPath(); smile.move(to: NSPoint(x: 43, y: 44)); smile.curve(to: NSPoint(x: 70, y: 44), controlPoint1: NSPoint(x: 52, y: 30), controlPoint2: NSPoint(x: 62, y: 30)); smile.lineWidth = 3; smile.stroke()
        case 1:
            let ghost = NSBezierPath(); ghost.move(to: NSPoint(x: 25, y: 25)); ghost.line(to: NSPoint(x: 25, y: 63)); ghost.curve(to: NSPoint(x: 87, y: 63), controlPoint1: NSPoint(x: 25, y: 105), controlPoint2: NSPoint(x: 87, y: 105)); ghost.line(to: NSPoint(x: 87, y: 25)); ghost.line(to: NSPoint(x: 75, y: 34)); ghost.line(to: NSPoint(x: 64, y: 25)); ghost.line(to: NSPoint(x: 55, y: 34)); ghost.line(to: NSPoint(x: 44, y: 25)); ghost.line(to: NSPoint(x: 34, y: 34)); ghost.close()
            NSColor(calibratedWhite: 0.97, alpha: 0.95).setFill(); ghost.fill()
            NSColor(calibratedRed: 0.29, green: 0.16, blue: 0.17, alpha: 1).setFill()
            NSBezierPath(ovalIn: NSRect(x: 44, y: 57, width: 7, height: 10)).fill(); NSBezierPath(ovalIn: NSRect(x: 65, y: 57, width: 7, height: 10)).fill()
        default:
            NSColor(calibratedRed: 0.43, green: 0.22, blue: 0.16, alpha: 1).setFill()
            let leaf = NSBezierPath(); leaf.move(to: NSPoint(x: 55, y: 16)); leaf.curve(to: NSPoint(x: 84, y: 83), controlPoint1: NSPoint(x: 18, y: 45), controlPoint2: NSPoint(x: 32, y: 100)); leaf.curve(to: NSPoint(x: 55, y: 16), controlPoint1: NSPoint(x: 110, y: 55), controlPoint2: NSPoint(x: 79, y: 25)); leaf.fill()
            NSColor(calibratedRed: 0.91, green: 0.57, blue: 0.25, alpha: 1).setStroke(); let vein = NSBezierPath(); vein.move(to: NSPoint(x: 55, y: 18)); vein.line(to: NSPoint(x: 70, y: 78)); vein.lineWidth = 3; vein.stroke()
        }
    }
}

private final class StickerWindow: NSWindow {
    let index: Int
    let moved: (Int, NSPoint) -> Void
    init(index: Int, origin: NSPoint, moved: @escaping (Int, NSPoint) -> Void) {
        self.index = index; self.moved = moved
        super.init(contentRect: NSRect(origin: origin, size: NSSize(width: 112, height: 112)), styleMask: [.borderless], backing: .buffered, defer: false)
        isOpaque = false; backgroundColor = .clear; hasShadow = false
        animationBehavior = .none
        level = NSWindow.Level(rawValue: Int(CGWindowLevelForKey(.desktopIconWindow)) + 1)
        collectionBehavior = [.canJoinAllSpaces, .stationary]
        isMovableByWindowBackground = true
        contentView = StickerView(kind: index)
        orderFrontRegardless()
    }
    override func mouseUp(with event: NSEvent) { super.mouseUp(with: event); moved(index, frame.origin) }
}

private final class Bridge {
    private var listener: NWListener?
    private let snapshot: () -> [String: Bool]
    init(snapshot: @escaping () -> [String: Bool]) { self.snapshot = snapshot }
    func start() {
        guard let port = NWEndpoint.Port(rawValue: 47831) else { return }
        let parameters = NWParameters.tcp
        parameters.requiredLocalEndpoint = .hostPort(host: .ipv4(.loopback), port: port)
        do { listener = try NWListener(using: parameters) } catch { NSLog("Bridge: %@", error.localizedDescription); return }
        listener?.stateUpdateHandler = { state in NSLog("Bridge state: %@", String(describing: state)) }
        listener?.newConnectionHandler = { [weak self] connection in
            connection.start(queue: .main)
            connection.receive(minimumIncompleteLength: 1, maximumLength: 4096) { data, _, _, _ in
                guard let self else { connection.cancel(); return }
                let request = String(data: data ?? Data(), encoding: .utf8) ?? ""
                guard request.hasPrefix("GET /settings ") else { connection.cancel(); return }
                let json = (try? JSONSerialization.data(withJSONObject: self.snapshot(), options: [.sortedKeys])) ?? Data("{}".utf8)
                let header = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nCache-Control: no-store\r\nContent-Length: \(json.count)\r\nConnection: close\r\n\r\n"
                connection.send(content: Data(header.utf8) + json, completion: .contentProcessed { _ in connection.cancel() })
            }
        }
        listener?.start(queue: .main)
    }
}

private final class App: NSObject, NSApplicationDelegate, NSWindowDelegate {
    private let defaults = UserDefaults.standard
    private var item: NSStatusItem!
    private var window: NSWindow!
    private var cards: [Effect: PreviewCard] = [:]
    private var stickers: [StickerWindow] = []
    private var bridge: Bridge!
    private var folderTimer: Timer?
    private let fm = FileManager.default
    private var support: URL { fm.homeDirectoryForCurrentUser.appendingPathComponent("Library/Application Support/Halloween Decor", isDirectory: true) }
    private var desktop: URL { fm.homeDirectoryForCurrentUser.appendingPathComponent("Desktop", isDirectory: true) }
    private func enabled(_ effect: Effect) -> Bool { defaults.bool(forKey: effect.rawValue) }
    func applicationDidFinishLaunching(_ notification: Notification) {
        try? fm.createDirectory(at: support, withIntermediateDirectories: true)
        item = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        item.button?.title = "🎃"
        item.button?.target = self
        item.button?.action = #selector(showWindow)
        makeWindow()
        bridge = Bridge(snapshot: { [weak self] in Dictionary(uniqueKeysWithValues: Effect.allCases.map { ($0.rawValue, self?.enabled($0) ?? false) }) })
        bridge.start()
        if enabled(.stickers) { showStickers() }
        if enabled(.folders) { applyFolderIcons() }
        folderTimer = Timer.scheduledTimer(withTimeInterval: 20, repeats: true) { [weak self] _ in if self?.enabled(.folders) == true { self?.applyFolderIcons() } }
        showWindow()
    }
    private func makeWindow() {
        let size = NSSize(width: 920, height: 730)
        window = NSWindow(contentRect: NSRect(origin: .zero, size: size), styleMask: [.titled, .closable, .miniaturizable], backing: .buffered, defer: false)
        window.title = "Halloween Decor"
        window.center()
        window.isReleasedWhenClosed = false
        window.delegate = self
        let root = NSView(frame: NSRect(origin: .zero, size: size))
        root.wantsLayer = true
        root.layer?.backgroundColor = NSColor(calibratedRed: 0.97, green: 0.94, blue: 0.89, alpha: 1).cgColor
        window.contentView = root
        let heading = NSTextField(labelWithString: "Set your Halloween mood")
        heading.font = .systemFont(ofSize: 29, weight: .bold)
        heading.textColor = NSColor(calibratedRed: 0.29, green: 0.17, blue: 0.15, alpha: 1)
        heading.frame = NSRect(x: 24, y: 674, width: 680, height: 38)
        root.addSubview(heading)
        let intro = NSTextField(labelWithString: "Click a card to apply its effect. Mix and match any combination.")
        intro.font = .systemFont(ofSize: 13)
        intro.textColor = NSColor(calibratedRed: 0.44, green: 0.34, blue: 0.29, alpha: 1)
        intro.frame = NSRect(x: 25, y: 648, width: 780, height: 20)
        root.addSubview(intro)
        let videoRoot = Bundle.main.resourceURL?.appendingPathComponent("Previews")
        for (index, effect) in Effect.allCases.enumerated() {
            let column = index % 2, row = index / 2
            let card = PreviewCard(effect: effect, active: enabled(effect), video: videoRoot?.appendingPathComponent(effect.rawValue + ".mp4"), frame: NSRect(x: 20 + column * 450, y: 450 - row * 195, width: 430, height: 180))
            card.onSelect = { [weak self] effect in self?.toggle(effect) }
            root.addSubview(card)
            cards[effect] = card
        }
        let restore = NSButton(title: "Restore Everything", target: self, action: #selector(restoreEverything))
        restore.bezelStyle = .rounded
        restore.frame = NSRect(x: 20, y: 28, width: 120, height: 30)
        root.addSubview(restore)
        let quit = NSButton(title: "Quit Halloween Decor", target: self, action: #selector(quitApp))
        quit.bezelStyle = .rounded
        quit.frame = NSRect(x: 746, y: 28, width: 150, height: 30)
        root.addSubview(quit)
    }
    @objc private func showWindow() {
        window.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
        cards.values.forEach { $0.resumePreview() }
    }
    func windowWillClose(_ notification: Notification) { cards.values.forEach { $0.pausePreview() } }
    private func toggle(_ effect: Effect) {
        let active = !enabled(effect)
        if effect == .wallpaper {
            let succeeded = active ? applyWallpaper() : restoreWallpaper()
            if !succeeded {
                cards[effect]?.setActive(enabled(effect))
                let alert = NSAlert()
                alert.messageText = active ? "Couldn’t change the wallpaper" : "Couldn’t restore the previous wallpaper"
                alert.informativeText = "Check that the original wallpaper file is available. Other effects are unaffected."
                alert.runModal()
                return
            }
        }
        defaults.set(active, forKey: effect.rawValue)
        cards[effect]?.setActive(active)
        switch effect {
        case .stickers: active ? showStickers() : hideStickers()
        case .folders: active ? applyFolderIcons() : restoreFolderIcons()
        case .wallpaper: break
        default: break
        }
    }
    @objc private func restoreEverything() {
        hideStickers(); restoreFolderIcons()
        let wallpaperRestored = restoreWallpaper()
        for effect in Effect.allCases {
            let active = effect == .wallpaper && !wallpaperRestored
            defaults.set(active, forKey: effect.rawValue)
            cards[effect]?.setActive(active)
        }
        if !wallpaperRestored {
            let alert = NSAlert()
            alert.messageText = "Couldn’t restore the previous wallpaper"
            alert.informativeText = "The original wallpaper and its backup are unavailable. Other effects have been turned off."
            alert.runModal()
        }
    }
    @objc private func quitApp() { NSApp.terminate(nil) }
    private func showStickers() {
        if !stickers.isEmpty { stickers.forEach { $0.orderFrontRegardless() }; return }
        let visible = NSScreen.main?.visibleFrame ?? NSRect(x: 0, y: 0, width: 900, height: 700)
        for index in 0..<3 {
            let key = "sticker.\(index)"
            let origin: NSPoint
            if let saved = defaults.string(forKey: key) { origin = NSPointFromString(saved) }
            else { origin = NSPoint(x: visible.minX + 120 + CGFloat(index) * 135, y: visible.minY + 110) }
            let sticker = StickerWindow(index: index, origin: origin) { [weak self] i, point in self?.defaults.set(NSStringFromPoint(point), forKey: "sticker.\(i)") }
            NotificationCenter.default.addObserver(forName: NSWindow.didMoveNotification, object: sticker, queue: .main) { [weak self, weak sticker] _ in
                guard let sticker else { return }
                self?.defaults.set(NSStringFromPoint(sticker.frame.origin), forKey: "sticker.\(index)")
            }
            stickers.append(sticker)
        }
    }
    private func hideStickers() { stickers.forEach { $0.orderOut(nil) } }
    private func folderBackupURL() -> URL { support.appendingPathComponent("folder-backups.json") }
    private func folderBackups() -> [String: String] {
        guard let data = try? Data(contentsOf: folderBackupURL()) else { return [:] }
        return (try? JSONDecoder().decode([String: String].self, from: data)) ?? [:]
    }
    private func saveFolderBackups(_ map: [String: String]) { if let data = try? JSONEncoder().encode(map) { try? data.write(to: folderBackupURL(), options: .atomic) } }
    private func hasCustomIcon(_ path: String) -> Bool {
        var bytes = [UInt8](repeating: 0, count: 32)
        let count = path.withCString { p in bytes.withUnsafeMutableBytes { buffer in getxattr(p, "com.apple.FinderInfo", buffer.baseAddress, 32, 0, 0) } }
        return count >= 10 && (UInt16(bytes[8]) << 8 | UInt16(bytes[9])) & 0x0400 != 0
    }
    private func applyFolderIcons() {
        guard let urls = try? fm.contentsOfDirectory(at: desktop, includingPropertiesForKeys: [.isDirectoryKey, .isSymbolicLinkKey], options: [.skipsHiddenFiles]) else { return }
        var backups = folderBackups()
        let icon = drawFolderIcon()
        for url in urls {
            let values = try? url.resourceValues(forKeys: [.isDirectoryKey, .isSymbolicLinkKey])
            guard values?.isDirectory == true, values?.isSymbolicLink != true, backups[url.path] == nil else { continue }
            let backupName: String
            if hasCustomIcon(url.path), let data = NSWorkspace.shared.icon(forFile: url.path).tiffRepresentation {
                backupName = UUID().uuidString + ".tiff"
                try? data.write(to: support.appendingPathComponent(backupName), options: .atomic)
            } else { backupName = "default" }
            // Persist the original before changing Finder metadata.
            backups[url.path] = backupName; saveFolderBackups(backups)
            if !NSWorkspace.shared.setIcon(icon, forFile: url.path, options: []) { backups.removeValue(forKey: url.path); saveFolderBackups(backups) }
        }
    }
    private func restoreFolderIcons() {
        var backups = folderBackups()
        for (path, name) in backups {
            guard fm.fileExists(atPath: path) else { continue }
            let original = name == "default" ? nil : NSImage(contentsOf: support.appendingPathComponent(name))
            if name != "default" && original == nil { continue }
            if NSWorkspace.shared.setIcon(original, forFile: path, options: []) {
                backups.removeValue(forKey: path)
                if name != "default" { try? fm.removeItem(at: support.appendingPathComponent(name)) }
            }
        }
        saveFolderBackups(backups)
    }
    private func wallpaperBackupURL() -> URL { support.appendingPathComponent("wallpaper-backups.json") }
    private func applyWallpaper() -> Bool {
        guard let wallpaper = drawWallpaper() else { return false }
        var backups: [String: String] = [:]
        if let data = try? Data(contentsOf: wallpaperBackupURL()) { backups = (try? JSONDecoder().decode([String: String].self, from: data)) ?? [:] }
        for (index, screen) in NSScreen.screens.enumerated() {
            let key = "screen.\(index)"
            if backups[key] == nil {
                guard let old = NSWorkspace.shared.desktopImageURL(for: screen), old != wallpaper, old.isFileURL, fm.fileExists(atPath: old.path) else { return false }
                let copy = support.appendingPathComponent("wallpaper-original-\(index)-\(UUID().uuidString).\(old.pathExtension)")
                guard (try? fm.copyItem(at: old, to: copy)) != nil else { return false }
                backups[key] = old.absoluteString
                backups[key + ".copy"] = copy.absoluteString
            }
        }
        guard let data = try? JSONEncoder().encode(backups), (try? data.write(to: wallpaperBackupURL(), options: .atomic)) != nil else { return false }
        for screen in NSScreen.screens {
            do { try NSWorkspace.shared.setDesktopImageURL(wallpaper, for: screen, options: [:]) }
            catch { _ = restoreWallpaper(); return false }
        }
        return true
    }
    private func restoreWallpaper() -> Bool {
        guard fm.fileExists(atPath: wallpaperBackupURL().path) else { return !enabled(.wallpaper) }
        guard let data = try? Data(contentsOf: wallpaperBackupURL()), let backups = try? JSONDecoder().decode([String: String].self, from: data) else { return false }
        var remaining = backups
        for (index, screen) in NSScreen.screens.enumerated() {
            let key = "screen.\(index)"
            if let raw = backups[key], let original = URL(string: raw) {
                let copy = backups[key + ".copy"].flatMap(URL.init(string:))
                let candidate = fm.fileExists(atPath: original.path) ? original : copy
                if let candidate, (try? NSWorkspace.shared.setDesktopImageURL(candidate, for: screen, options: [:])) != nil {
                    remaining.removeValue(forKey: key)
                    remaining.removeValue(forKey: key + ".copy")
                    if candidate == original, let copy { try? fm.removeItem(at: copy) }
                }
            }
        }
        if remaining.isEmpty { try? fm.removeItem(at: wallpaperBackupURL()) }
        else if let data = try? JSONEncoder().encode(remaining) { try? data.write(to: wallpaperBackupURL(), options: .atomic) }
        return remaining.isEmpty
    }
    private func drawFolderIcon() -> NSImage {
        let image = NSImage(size: NSSize(width: 512, height: 512))
        image.lockFocus()
        NSColor(calibratedRed: 0.42, green: 0.22, blue: 0.15, alpha: 1).setFill()
        NSBezierPath(roundedRect: NSRect(x: 34, y: 104, width: 444, height: 304), xRadius: 48, yRadius: 48).fill()
        NSBezierPath(roundedRect: NSRect(x: 34, y: 352, width: 176, height: 93), xRadius: 30, yRadius: 30).fill()
        NSColor(calibratedRed: 0.63, green: 0.36, blue: 0.23, alpha: 1).setFill()
        NSBezierPath(roundedRect: NSRect(x: 34, y: 104, width: 444, height: 272), xRadius: 48, yRadius: 48).fill()
        NSColor(calibratedRed: 0.91, green: 0.55, blue: 0.25, alpha: 1).setFill()
        NSBezierPath(ovalIn: NSRect(x: 203, y: 158, width: 108, height: 135)).fill()
        NSColor(calibratedRed: 0.97, green: 0.69, blue: 0.33, alpha: 1).setFill()
        NSBezierPath(ovalIn: NSRect(x: 228, y: 158, width: 58, height: 135)).fill()
        NSColor(calibratedRed: 0.29, green: 0.32, blue: 0.15, alpha: 1).setFill()
        NSBezierPath(roundedRect: NSRect(x: 251, y: 281, width: 12, height: 23), xRadius: 4, yRadius: 4).fill()
        image.unlockFocus(); return image
    }
    private func drawWallpaper() -> URL? {
        let url = support.appendingPathComponent("autumn-wallpaper.png")
        if fm.fileExists(atPath: url.path) { return url }
        let size = NSSize(width: 1920, height: 1200)
        let image = NSImage(size: size); image.lockFocus()
        let colors = [NSColor(calibratedRed: 0.18, green: 0.11, blue: 0.15, alpha: 1), NSColor(calibratedRed: 0.51, green: 0.28, blue: 0.22, alpha: 1)]
        NSGradient(colors: colors)?.draw(in: NSRect(origin: .zero, size: size), angle: 90)
        NSColor(calibratedRed: 0.99, green: 0.80, blue: 0.52, alpha: 0.85).setFill()
        NSBezierPath(ovalIn: NSRect(x: 1350, y: 650, width: 210, height: 210)).fill()
        NSColor(calibratedRed: 0.18, green: 0.11, blue: 0.15, alpha: 1).setFill()
        NSBezierPath(ovalIn: NSRect(x: 1300, y: 685, width: 195, height: 210)).fill()
        NSColor(calibratedRed: 0.10, green: 0.13, blue: 0.12, alpha: 1).setFill()
        let ground = NSBezierPath(); ground.move(to: NSPoint(x: 0, y: 0)); ground.line(to: NSPoint(x: 1920, y: 0)); ground.line(to: NSPoint(x: 1920, y: 255)); ground.curve(to: NSPoint(x: 0, y: 230), controlPoint1: NSPoint(x: 1310, y: 365), controlPoint2: NSPoint(x: 620, y: 145)); ground.close(); ground.fill()
        for i in 0..<72 {
            let x = CGFloat((i * 233 + 81) % 1920), y = CGFloat((i * 137 + 230) % 870)
            NSColor(calibratedRed: 0.94, green: 0.58, blue: 0.29, alpha: 0.23).setFill()
            NSBezierPath(ovalIn: NSRect(x: x, y: y, width: CGFloat(i % 3 + 3), height: CGFloat(i % 3 + 3))).fill()
        }
        image.unlockFocus()
        guard let tiff = image.tiffRepresentation, let rep = NSBitmapImageRep(data: tiff), let png = rep.representation(using: .png, properties: [:]) else { return nil }
        try? png.write(to: url, options: .atomic); return url
    }
}

let application = NSApplication.shared
private let delegate = App()
application.delegate = delegate
application.setActivationPolicy(.accessory)
application.run()
