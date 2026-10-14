import AppKit
import AVFoundation
import Network
import Darwin
import CryptoKit
import CoreText

private enum InterfaceFont {
    static func register() {
        for name in ["AnonymousPro-Regular", "AnonymousPro-Bold"] {
            if let url = Bundle.main.url(forResource: name, withExtension: "ttf", subdirectory: "Fonts") {
                CTFontManagerRegisterFontsForURL(url as CFURL, .process, nil)
            }
        }
    }
    static func regular(_ size: CGFloat) -> NSFont {
        NSFont(name: "AnonymousPro", size: size) ?? .monospacedSystemFont(ofSize: size, weight: .regular)
    }
    static func bold(_ size: CGFloat) -> NSFont {
        NSFont(name: "AnonymousPro-Bold", size: size) ?? .monospacedSystemFont(ofSize: size, weight: .bold)
    }
}

private enum Effect: String, CaseIterable {
    case webs, stickers, folders, wallpaper, cursor
    var title: String {
        switch self {
        case .webs: return "Spider Web"
        case .stickers: return "Desktop Stickers"
        case .folders: return "Autumn Folder Icons"
        case .wallpaper: return "Pumpkin Wallpaper"
        case .cursor: return "Candy Cursor"
        }
    }
    var detail: String {
        switch self {
        case .webs: return "Four spiders hang from a web"
        case .stickers: return "\(StickerSpec.all.count) movable desktop stickers"
        case .folders: return "Six styles for your folders"
        case .wallpaper: return "Pumpkins & autumn widget decor"
        case .cursor: return "Candy follows your pointer"
        }
    }
}

private final class PreviewCard: NSView {
    let effect: Effect
    var onSelect: ((Effect) -> Void)?
    private let player: AVPlayer
    private var endObserver: NSObjectProtocol?
    private let status = GradientSwitch(frame: .zero)
    init(effect: Effect, active: Bool, video: URL?, frame: NSRect) {
        self.effect = effect
        if let video { player = AVPlayer(url: video) } else { player = AVPlayer() }
        super.init(frame: frame)
        wantsLayer = true
        let preview = CALayer()
        preview.frame = CGRect(x: 2, y: 6, width: 226, height: frame.height - 12)
        preview.cornerRadius = 15
        preview.backgroundColor = NSColor(calibratedWhite: 0.08, alpha: 1).cgColor
        preview.shadowColor = NSColor.black.cgColor
        preview.shadowOpacity = 0.75
        preview.shadowRadius = 13
        preview.shadowOffset = CGSize(width: 0, height: -7)
        layer?.addSublayer(preview)
        let bezel = CAGradientLayer()
        bezel.frame = preview.bounds
        bezel.colors = [NSColor(calibratedWhite: 0.23, alpha: 1).cgColor,
                        NSColor(calibratedWhite: 0.065, alpha: 1).cgColor,
                        NSColor(calibratedWhite: 0.025, alpha: 1).cgColor]
        bezel.locations = [0, 0.38, 1]
        bezel.cornerRadius = 15
        bezel.borderWidth = 1
        bezel.borderColor = NSColor(calibratedWhite: 0.25, alpha: 1).cgColor
        preview.addSublayer(bezel)
        let videoLayer = AVPlayerLayer(player: player)
        videoLayer.frame = preview.bounds.insetBy(dx: 6, dy: 6)
        videoLayer.videoGravity = .resizeAspectFill
        videoLayer.cornerRadius = 10
        videoLayer.masksToBounds = true
        videoLayer.backgroundColor = NSColor(calibratedWhite: 0.07, alpha: 1).cgColor
        preview.addSublayer(videoLayer)
        let title = NSTextField(labelWithString: effect.title)
        title.font = InterfaceFont.bold(20)
        title.textColor = .white
        title.frame = NSRect(x: 250, y: frame.height / 2 + 1, width: frame.width - 355, height: 28)
        addSubview(title)
        let detail = NSTextField(labelWithString: effect.detail)
        detail.font = InterfaceFont.regular(13.5)
        detail.textColor = NSColor(calibratedWhite: 0.49, alpha: 1)
        detail.lineBreakMode = .byTruncatingTail
        detail.frame = NSRect(x: 250, y: frame.height / 2 - 21, width: frame.width - 355, height: 21)
        addSubview(detail)
        status.target = self
        status.action = #selector(didSelect)
        status.setAccessibilityLabel(effect.title)
        status.frame = NSRect(x: frame.width - 95, y: frame.height / 2 - 22, width: 88, height: 44)
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
        status.isOn = active
    }
    @objc private func didSelect() { onSelect?(effect) }
    override func mouseDown(with event: NSEvent) { onSelect?(effect) }
}

private final class GradientSwitch: NSControl {
    var isOn = false { didSet { needsDisplay = true } }
    override var intrinsicContentSize: NSSize { NSSize(width: 88, height: 44) }
    override func draw(_ dirtyRect: NSRect) {
        let trackRect = bounds.insetBy(dx: 1, dy: 2)
        let track = NSBezierPath(roundedRect: trackRect, xRadius: 21, yRadius: 21)
        NSGraphicsContext.saveGraphicsState()
        let trackShadow = NSShadow()
        trackShadow.shadowColor = NSColor.black.withAlphaComponent(0.8)
        trackShadow.shadowBlurRadius = 7
        trackShadow.shadowOffset = CGSize(width: 0, height: -3)
        trackShadow.set()
        if isOn {
            NSGradient(colors: [NSColor(calibratedRed: 1, green: 0.59, blue: 0.17, alpha: 1),
                                NSColor(calibratedRed: 1, green: 0.43, blue: 0.045, alpha: 1),
                                NSColor(calibratedRed: 0.90, green: 0.27, blue: 0.005, alpha: 1)])!.draw(in: track, angle: 90)
        } else {
            NSGradient(colors: [NSColor(calibratedWhite: 0.24, alpha: 1),
                                NSColor(calibratedWhite: 0.105, alpha: 1),
                                NSColor(calibratedWhite: 0.075, alpha: 1)])!.draw(in: track, angle: 90)
        }
        NSGraphicsContext.restoreGraphicsState()
        track.lineWidth = 1.2
        (isOn ? NSColor(calibratedRed: 1, green: 0.62, blue: 0.27, alpha: 1) : NSColor(calibratedWhite: 0.23, alpha: 1)).setStroke()
        track.stroke()
        let diameter: CGFloat = 35
        let x = isOn ? bounds.maxX - diameter - 5 : bounds.minX + 5
        let knob = NSBezierPath(ovalIn: NSRect(x: x, y: (bounds.height - diameter) / 2, width: diameter, height: diameter))
        NSGraphicsContext.saveGraphicsState()
        let shadow = NSShadow(); shadow.shadowColor = NSColor.black.withAlphaComponent(0.6); shadow.shadowBlurRadius = 5; shadow.shadowOffset = CGSize(width: 0, height: -2); shadow.set()
        NSGradient(colors: [NSColor.white, NSColor(calibratedWhite: 0.88, alpha: 1)])!.draw(in: knob, angle: 90)
        NSGraphicsContext.restoreGraphicsState()
        knob.lineWidth = 0.8
        NSColor(calibratedWhite: 0.75, alpha: 1).setStroke()
        knob.stroke()
    }
    override func mouseDown(with event: NSEvent) { isOn.toggle(); sendAction(action, to: target) }
}

private final class PanelSurface: NSView {
    override func draw(_ dirtyRect: NSRect) {
        let outer = NSBezierPath(roundedRect: bounds.insetBy(dx: 8, dy: 8), xRadius: 46, yRadius: 46)
        NSGradient(colors: [NSColor(calibratedWhite: 0.12, alpha: 1),
                            NSColor(calibratedWhite: 0.045, alpha: 1)])!.draw(in: outer, angle: 90)
        outer.lineWidth = 1.5
        NSColor(calibratedWhite: 0.18, alpha: 1).setStroke()
        outer.stroke()
        let inner = NSBezierPath(roundedRect: bounds.insetBy(dx: 26, dy: 26), xRadius: 35, yRadius: 35)
        NSGradient(colors: [NSColor(calibratedWhite: 0.078, alpha: 1),
                            NSColor(calibratedWhite: 0.062, alpha: 1)])!.draw(in: inner, angle: 90)
        inner.lineWidth = 1.6
        NSColor(calibratedWhite: 0.24, alpha: 1).setStroke()
        inner.stroke()
        let innerHighlight = NSBezierPath(roundedRect: bounds.insetBy(dx: 28, dy: 28), xRadius: 33, yRadius: 33)
        innerHighlight.lineWidth = 1
        NSColor(calibratedWhite: 0.11, alpha: 1).setStroke()
        innerHighlight.stroke()
    }
}

private final class GlossyCloseButton: NSButton {
    override func draw(_ dirtyRect: NSRect) {
        let shape = NSBezierPath(roundedRect: bounds.insetBy(dx: 3, dy: 4), xRadius: 15, yRadius: 15)
        NSGraphicsContext.saveGraphicsState()
        let shadow = NSShadow(); shadow.shadowColor = .black; shadow.shadowBlurRadius = 9; shadow.shadowOffset = CGSize(width: 0, height: -4); shadow.set()
        NSGradient(colors: [NSColor(calibratedWhite: 0.29, alpha: 1),
                            NSColor(calibratedWhite: 0.055, alpha: 1),
                            NSColor.black])!.draw(in: shape, angle: 90)
        NSGraphicsContext.restoreGraphicsState()
        shape.lineWidth = 1
        NSColor(calibratedWhite: 0.19, alpha: 1).setStroke()
        shape.stroke()
        let cross = NSBezierPath()
        cross.lineWidth = 4
        cross.lineCapStyle = .round
        cross.move(to: NSPoint(x: bounds.midX - 9, y: bounds.midY - 9))
        cross.line(to: NSPoint(x: bounds.midX + 9, y: bounds.midY + 9))
        cross.move(to: NSPoint(x: bounds.midX - 9, y: bounds.midY + 9))
        cross.line(to: NSPoint(x: bounds.midX + 9, y: bounds.midY - 9))
        NSColor.white.setStroke()
        cross.stroke()
    }
}

private final class TopAlignedView: NSView { override var isFlipped: Bool { true } }

private final class LoadingBatView: NSView {
    private let left = CAShapeLayer()
    private let right = CAShapeLayer()
    private let body = CAShapeLayer()

    override init(frame: NSRect) {
        super.init(frame: frame)
        wantsLayer = true
        let white = NSColor.white.cgColor
        let wing = CGMutablePath()
        wing.move(to: CGPoint(x: 42, y: 18))
        wing.addCurve(to: CGPoint(x: 1, y: 34), control1: CGPoint(x: 28, y: 30), control2: CGPoint(x: 15, y: 37))
        wing.addQuadCurve(to: CGPoint(x: 8, y: 20), control: CGPoint(x: 0, y: 24))
        wing.addQuadCurve(to: CGPoint(x: 18, y: 18), control: CGPoint(x: 15, y: 27))
        wing.addQuadCurve(to: CGPoint(x: 28, y: 14), control: CGPoint(x: 25, y: 23))
        wing.addQuadCurve(to: CGPoint(x: 42, y: 18), control: CGPoint(x: 37, y: 25))
        wing.closeSubpath()
        left.frame = CGRect(x: 0, y: 3, width: 42, height: 37)
        left.anchorPoint = CGPoint(x: 1, y: 0.55)
        left.path = wing
        left.fillColor = white
        right.frame = CGRect(x: 49, y: 3, width: 42, height: 37)
        right.anchorPoint = CGPoint(x: 0, y: 0.55)
        var mirror = CGAffineTransform(a: -1, b: 0, c: 0, d: 1, tx: 42, ty: 0)
        right.path = wing.copy(using: &mirror)
        right.fillColor = white
        let bodyPath = CGMutablePath()
        bodyPath.move(to: CGPoint(x: 8.5, y: 3))
        bodyPath.addCurve(to: CGPoint(x: 2, y: 16), control1: CGPoint(x: 3, y: 6), control2: CGPoint(x: 1, y: 10))
        bodyPath.addLine(to: CGPoint(x: 2, y: 29))
        bodyPath.addLine(to: CGPoint(x: 4, y: 37))
        bodyPath.addLine(to: CGPoint(x: 8.5, y: 32))
        bodyPath.addLine(to: CGPoint(x: 13, y: 37))
        bodyPath.addLine(to: CGPoint(x: 15, y: 29))
        bodyPath.addLine(to: CGPoint(x: 15, y: 16))
        bodyPath.addCurve(to: CGPoint(x: 8.5, y: 3), control1: CGPoint(x: 16, y: 10), control2: CGPoint(x: 14, y: 6))
        bodyPath.closeSubpath()
        body.frame = CGRect(x: 37, y: 3, width: 17, height: 37)
        body.path = bodyPath
        body.fillColor = white
        for part in [left, right, body] { layer?.addSublayer(part) }
        let label = NSTextField(labelWithString: "Applying…")
        label.font = InterfaceFont.regular(12)
        label.textColor = .white
        label.frame = NSRect(x: 92, y: 12, width: 82, height: 18)
        addSubview(label)
        setAccessibilityLabel("Applying Halloween effect")
        isHidden = true
    }
    required init?(coder: NSCoder) { fatalError() }
    func start() {
        isHidden = false
        guard !NSWorkspace.shared.accessibilityDisplayShouldReduceMotion else { return }
        for (wing, from, to) in [(left, -0.30, 0.22), (right, 0.30, -0.22)] {
            let flap = CABasicAnimation(keyPath: "transform.rotation.z")
            flap.fromValue = from
            flap.toValue = to
            flap.duration = 0.32
            flap.autoreverses = true
            flap.repeatCount = .infinity
            wing.add(flap, forKey: "flap")
        }
        let bob = CABasicAnimation(keyPath: "position.y")
        bob.fromValue = body.position.y - 2
        bob.toValue = body.position.y + 2
        bob.duration = 0.32
        bob.autoreverses = true
        bob.repeatCount = .infinity
        body.add(bob, forKey: "bob")
    }
    func stop() {
        left.removeAllAnimations(); right.removeAllAnimations(); body.removeAllAnimations()
        isHidden = true
    }
}

private struct StickerSpec {
    let name: String
    let size: NSSize
    static let all: [StickerSpec] = {
        var designs = [
        StickerSpec(name: "scorpio", size: NSSize(width: 118, height: 142)),
        StickerSpec(name: "taurus", size: NSSize(width: 166, height: 111)),
        StickerSpec(name: "axe-ghost", size: NSSize(width: 139, height: 139)),
        StickerSpec(name: "pumpkin-ghost", size: NSSize(width: 120, height: 106)),
        StickerSpec(name: "virgo-stamp", size: NSSize(width: 166, height: 111)),
        StickerSpec(name: "treat-ghost", size: NSSize(width: 125, height: 145)),
        StickerSpec(name: "leo-stamp", size: NSSize(width: 124, height: 124)),
        StickerSpec(name: "pixel-cat", size: NSSize(width: 112, height: 112))
        ]
        if let directory = Bundle.main.resourceURL?.appendingPathComponent("Stickers/Objects"),
           let files = try? FileManager.default.contentsOfDirectory(at: directory, includingPropertiesForKeys: nil) {
            for file in files.filter({ $0.pathExtension == "png" }).sorted(by: { $0.lastPathComponent < $1.lastPathComponent }) {
                guard let image = NSImage(contentsOf: file) else { continue }
                let scale = 84 / max(image.size.width, image.size.height)
                designs.append(StickerSpec(name: "Objects/" + file.deletingPathExtension().lastPathComponent,
                                           size: NSSize(width: image.size.width * scale + 8, height: image.size.height * scale + 8)))
            }
        }
        return designs
    }()
}

private final class StickerView: NSView {
    private let image: NSImage?
    init(spec: StickerSpec) {
        image = (Bundle.main.resourceURL?.appendingPathComponent("Stickers/\(spec.name).png")).flatMap(NSImage.init(contentsOf:))
        super.init(frame: NSRect(origin: .zero, size: spec.size))
    }
    required init?(coder: NSCoder) { fatalError() }
    override func draw(_ dirtyRect: NSRect) {
        guard let image else { return }
        let size = image.size
        let scale = min((bounds.width - 4) / size.width, (bounds.height - 4) / size.height)
        let fitted = NSSize(width: size.width * scale, height: size.height * scale)
        let frame = NSRect(x: (bounds.width - fitted.width) / 2, y: (bounds.height - fitted.height) / 2, width: fitted.width, height: fitted.height)
        NSGraphicsContext.saveGraphicsState()
        NSGraphicsContext.current?.imageInterpolation = .high
        NSGraphicsContext.current?.cgContext.setShadow(offset: CGSize(width: 2, height: -4), blur: 7, color: NSColor.black.withAlphaComponent(0.24).cgColor)
        image.draw(in: frame, from: .zero, operation: .sourceOver, fraction: 1)
        NSGraphicsContext.restoreGraphicsState()
    }
}

private final class StickerWindow: NSWindow {
    let index: Int
    let moved: (Int, NSPoint) -> Void
    init(index: Int, spec: StickerSpec, origin: NSPoint, moved: @escaping (Int, NSPoint) -> Void) {
        self.index = index; self.moved = moved
        super.init(contentRect: NSRect(origin: origin, size: spec.size), styleMask: [.borderless], backing: .buffered, defer: false)
        isOpaque = false; backgroundColor = .clear; hasShadow = false
        animationBehavior = .none
        level = NSWindow.Level(rawValue: Int(CGWindowLevelForKey(.desktopIconWindow)) + 1)
        collectionBehavior = [.canJoinAllSpaces, .stationary]
        isMovableByWindowBackground = true
        contentView = StickerView(spec: spec)
        orderFrontRegardless()
    }
    override func mouseUp(with event: NSEvent) { super.mouseUp(with: event); moved(index, frame.origin) }
}

private final class WebOverlay {
    private var windows: [NSWindow] = []
    private let artwork = Bundle.main.resourceURL?.appendingPathComponent("WebDecor", isDirectory: true)

    private func image(_ name: String) -> CGImage? {
        guard let url = artwork?.appendingPathComponent(name + ".png"),
              let image = NSImage(contentsOf: url) else { return nil }
        return image.cgImage(forProposedRect: nil, context: nil, hints: nil)
    }
    private func art(_ name: String, frame: CGRect) -> CALayer {
        let layer = CALayer()
        layer.frame = frame
        layer.contents = image(name)
        layer.contentsGravity = .resizeAspect
        layer.contentsScale = NSScreen.main?.backingScaleFactor ?? 2
        return layer
    }
    func show() {
        hide()
        for screen in NSScreen.screens {
            let size = screen.frame.size
            let visible = screen.visibleFrame
            let window = NSWindow(contentRect: screen.frame, styleMask: [.borderless], backing: .buffered, defer: false)
            window.isOpaque = false
            window.backgroundColor = .clear
            window.hasShadow = false
            window.ignoresMouseEvents = true
            // Draw over the menu bar; the transparent window stays click-through.
            window.level = .statusBar
            window.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary, .stationary]
            let view = NSView(frame: CGRect(origin: .zero, size: size))
            view.wantsLayer = true
            window.contentView = view
            guard let root = view.layer else { continue }
            // Pin the cropped artwork directly to the usable screen's top edge
            // and reduce it to half of its current size.
            let width = min(visible.width * 0.80, 1170)
            let web = image("wide-web")
            let height = web.map { width * CGFloat($0.height) / CGFloat($0.width) } ?? width / 2
            let centerX = visible.midX - screen.frame.minX
            let webLayer = art("wide-web", frame: CGRect(x: centerX - width / 2, y: size.height - height + 6, width: width, height: height))
            // Pivot at the screen edge and keep a little artwork above it, so
            // the web remains attached to the top throughout its gentle sway.
            webLayer.anchorPoint = CGPoint(x: 0.5, y: 1)
            webLayer.position = CGPoint(x: centerX, y: size.height + 6)
            root.addSublayer(webLayer)
            if !NSWorkspace.shared.accessibilityDisplayShouldReduceMotion {
                let sway = CABasicAnimation(keyPath: "transform.rotation.z")
                sway.fromValue = -0.003
                sway.toValue = 0.003
                sway.duration = 3.5
                sway.autoreverses = true
                sway.repeatCount = .infinity
                sway.timingFunction = CAMediaTimingFunction(name: .easeInEaseOut)
                webLayer.add(sway, forKey: "web-sway")
                let drift = CABasicAnimation(keyPath: "position.x")
                drift.fromValue = centerX - 3
                drift.toValue = centerX + 3
                drift.duration = 3.5
                drift.autoreverses = true
                drift.repeatCount = .infinity
                drift.timingFunction = CAMediaTimingFunction(name: .easeInEaseOut)
                webLayer.add(drift, forKey: "web-drift")
            }
            window.orderFrontRegardless()
            windows.append(window)
        }
    }
    func hide() {
        windows.forEach { $0.orderOut(nil) }
        windows.removeAll()
    }
}

private final class AutumnWidgetView: NSView {
    private let webCorner: Int
    private let leaves: [NSImage] = ["oak-leaf", "autumn-leaf"].compactMap {
        (Bundle.main.resourceURL?.appendingPathComponent("Stickers/Objects/\($0).png")).flatMap { NSImage(contentsOf: $0) }
    }
    private let pinecone = (Bundle.main.resourceURL?.appendingPathComponent("Stickers/Objects/pinecone.png")).flatMap { NSImage(contentsOf: $0) }
    private let star = (Bundle.main.resourceURL?.appendingPathComponent("Stickers/Objects/star.png")).flatMap { NSImage(contentsOf: $0) }
    init(frame: NSRect, webCorner: Int) {
        self.webCorner = webCorner
        super.init(frame: frame)
    }
    required init?(coder: NSCoder) { fatalError() }
    private func leaf(at point: NSPoint, angle: CGFloat, index: Int, size: CGFloat = 32) {
        guard !leaves.isEmpty else { return }
        NSGraphicsContext.saveGraphicsState()
        let transform = NSAffineTransform()
        transform.translateX(by: point.x, yBy: point.y)
        transform.rotate(byDegrees: angle)
        transform.concat()
        let image = leaves[index % leaves.count]
        let scale = size / max(image.size.width, image.size.height)
        let fitted = NSSize(width: image.size.width * scale, height: image.size.height * scale)
        image.draw(in: NSRect(x: -fitted.width / 2, y: -fitted.height / 2, width: fitted.width, height: fitted.height))
        NSGraphicsContext.restoreGraphicsState()
    }
    private func cornerWeb(at origin: NSPoint, xDirection: CGFloat, yDirection: CGFloat) {
        NSGraphicsContext.saveGraphicsState()
        let transform = NSAffineTransform()
        transform.translateX(by: origin.x, yBy: origin.y)
        transform.scaleX(by: xDirection, yBy: yDirection)
        transform.concat()
        let web = NSBezierPath()
        for angle in [CGFloat(0), .pi / 6, .pi / 3, .pi / 2] {
            web.move(to: .zero)
            web.line(to: NSPoint(x: cos(angle) * 36, y: sin(angle) * 36))
        }
        for radius in [CGFloat(12), 24, 36] {
            web.move(to: NSPoint(x: radius, y: 0))
            for step in 1...3 {
                let start = CGFloat(step - 1) * .pi / 6
                let end = CGFloat(step) * .pi / 6
                web.curve(to: NSPoint(x: cos(end) * radius, y: sin(end) * radius),
                          controlPoint1: NSPoint(x: cos(start + .pi / 18) * radius * 0.82, y: sin(start + .pi / 18) * radius * 0.82),
                          controlPoint2: NSPoint(x: cos(end - .pi / 18) * radius * 0.82, y: sin(end - .pi / 18) * radius * 0.82))
            }
        }
        web.lineWidth = 0.9
        NSColor(calibratedRed: 0.18, green: 0.10, blue: 0.055, alpha: 0.8).setStroke()
        web.stroke()
        NSGraphicsContext.restoreGraphicsState()
    }
    private func garland(around widget: NSRect) {
        let left = widget.minX + 6
        let right = widget.maxX - 6
        let top = widget.maxY - 1
        let width = right - left
        let branch = NSBezierPath()
        branch.move(to: NSPoint(x: left, y: top))
        branch.curve(to: NSPoint(x: right, y: top),
                     controlPoint1: NSPoint(x: left + width * 0.32, y: top - 11),
                     controlPoint2: NSPoint(x: right - width * 0.32, y: top - 11))
        branch.lineWidth = 1.4
        NSColor(calibratedRed: 0.28, green: 0.17, blue: 0.09, alpha: 0.9).setStroke()
        branch.stroke()
        let count = max(3, Int(widget.width / 95) + 1)
        for index in 0..<count {
            let fraction = (CGFloat(index) + 0.4) / CGFloat(count)
            let x = left + width * fraction + CGFloat((index * 11 + webCorner * 7) % 9 - 4)
            let y = top - 8 * sin(.pi * fraction)
            let dx: CGFloat = index.isMultiple(of: 2) ? -4 : 4
            let drop = CGFloat(9 + (index * 5 + webCorner * 3) % 9)
            let stem = NSBezierPath()
            stem.move(to: NSPoint(x: x, y: y))
            stem.curve(to: NSPoint(x: x + dx, y: y - drop),
                       controlPoint1: NSPoint(x: x + dx * 0.2, y: y - drop * 0.4),
                       controlPoint2: NSPoint(x: x + dx * 0.8, y: y - drop * 0.7))
            stem.lineWidth = 0.9
            NSColor(calibratedRed: 0.35, green: 0.20, blue: 0.09, alpha: 0.9).setStroke()
            stem.stroke()
            leaf(at: NSPoint(x: x + dx, y: y - drop - 8),
                 angle: index.isMultiple(of: 2) ? 154 : 206, index: index,
                 size: CGFloat(23 + (index * 3) % 7))
            if index.isMultiple(of: 2) {
                let twig = NSBezierPath()
                twig.move(to: NSPoint(x: x, y: y))
                twig.line(to: NSPoint(x: x - 6, y: y + 3))
                twig.lineWidth = 0.8
                twig.stroke()
            }
        }
        guard let pinecone else { return }
        let coneFractions: [CGFloat] = widget.width > 260 ? [0.28, 0.75] : [0.67]
        for fraction in coneFractions {
            let x = left + width * fraction
            let y = top - 8 * sin(.pi * fraction)
            let stem = NSBezierPath()
            stem.move(to: NSPoint(x: x, y: y))
            stem.line(to: NSPoint(x: x + 1, y: y - 9))
            stem.lineWidth = 0.8
            NSColor(calibratedRed: 0.35, green: 0.20, blue: 0.09, alpha: 0.9).setStroke()
            stem.stroke()
            pinecone.draw(in: NSRect(x: x - 7, y: y - 24, width: 15, height: 18))
        }
    }
    override func draw(_ dirtyRect: NSRect) {
        let widget = bounds.insetBy(dx: 28, dy: 28)
        NSGraphicsContext.current?.imageInterpolation = .high
        let origin: NSPoint
        let xDirection: CGFloat
        let yDirection: CGFloat
        switch webCorner {
        case 0: origin = NSPoint(x: widget.minX, y: widget.maxY); xDirection = 1; yDirection = -1
        case 1: origin = NSPoint(x: widget.maxX, y: widget.maxY); xDirection = -1; yDirection = -1
        case 2: origin = NSPoint(x: widget.minX, y: widget.minY); xDirection = 1; yDirection = 1
        default: origin = NSPoint(x: widget.maxX, y: widget.minY); xDirection = -1; yDirection = 1
        }
        cornerWeb(at: origin, xDirection: xDirection, yDirection: yDirection)
        garland(around: widget)
        if let star {
            star.draw(in: NSRect(x: widget.maxX + 3, y: widget.midY - 8, width: 15, height: 15))
            star.draw(in: NSRect(x: widget.minX - 18, y: widget.maxY - 50, width: 10, height: 10))
        }
    }
}

private final class AutumnWidgetOverlay {
    private var windows: [Int: NSWindow] = [:]
    private var timer: Timer?
    func show() {
        refresh()
        if timer == nil {
            timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { [weak self] _ in self?.refresh() }
            timer?.tolerance = 0.2
        }
    }
    private func refresh() {
        let owners = Set(NSWorkspace.shared.runningApplications.filter { $0.bundleIdentifier == "com.apple.notificationcenterui" }.map { $0.processIdentifier })
        let list = CGWindowListCopyWindowInfo([.optionAll], kCGNullWindowID) as? [[String: Any]] ?? []
        let primaryTop = NSScreen.screens.first?.frame.maxY ?? 0
        var visible = Set<Int>()
        for item in list {
            guard let pid = item[kCGWindowOwnerPID as String] as? Int32, owners.contains(pid),
                  let level = item[kCGWindowLayer as String] as? Int, level < 0,
                  item[kCGWindowIsOnscreen as String] as? Bool == true,
                  let number = item[kCGWindowNumber as String] as? Int,
                  let dictionary = item[kCGWindowBounds as String] as? [String: Any],
                  let bounds = CGRect(dictionaryRepresentation: dictionary as CFDictionary),
                  bounds.width >= 100, bounds.height >= 100 else { continue }
            visible.insert(number)
            // Widget windows include eight points of transparent system padding.
            let widget = NSRect(x: bounds.minX + 8, y: primaryTop - bounds.maxY + 8,
                                width: bounds.width - 16, height: bounds.height - 16)
            let frame = widget.insetBy(dx: -28, dy: -28)
            if let window = windows[number] {
                if window.frame != frame { window.setFrame(frame, display: true) }
            } else {
                let window = NSWindow(contentRect: frame, styleMask: [.borderless], backing: .buffered, defer: false)
                window.title = "Spooky Widget Decor"
                window.isOpaque = false
                window.backgroundColor = .clear
                window.hasShadow = false
                window.ignoresMouseEvents = true
                window.animationBehavior = .none
                window.level = NSWindow.Level(rawValue: level + 1)
                window.collectionBehavior = [.canJoinAllSpaces, .stationary]
                let view = AutumnWidgetView(frame: NSRect(origin: .zero, size: frame.size), webCorner: number % 4)
                view.autoresizingMask = [.width, .height]
                window.contentView = view
                window.orderFrontRegardless()
                windows[number] = window
            }
        }
        for number in Array(windows.keys) where !visible.contains(number) {
            windows.removeValue(forKey: number)?.orderOut(nil)
        }
    }
    func hide() {
        timer?.invalidate(); timer = nil
        windows.values.forEach { $0.orderOut(nil) }
        windows.removeAll()
    }
}

private final class CandyPointerView: NSView {
    var pointerLocation: NSPoint = .zero { didSet { needsDisplay = true } }
    var screenOrigin: NSPoint = .zero
    private let candyImage: NSImage? = {
        guard let url = Bundle.main.url(forResource: "CandyCursor", withExtension: "png") else { return nil }
        return NSImage(contentsOf: url)
    }()
    override var isFlipped: Bool { false }

    override func draw(_ dirtyRect: NSRect) {
        // NSEvent.mouseLocation and this view both use bottom-left screen coordinates.
        let x = pointerLocation.x - screenOrigin.x
        let y = pointerLocation.y - screenOrigin.y
        let size = NSSize(width: 40, height: 42)
        NSGraphicsContext.saveGraphicsState()
        NSGraphicsContext.current?.imageInterpolation = .none
        // Keep the candy just below the pointer hotspot so a native arrow, if
        // macOS restores it in another app, does not cover the candy artwork.
        candyImage?.draw(in: NSRect(x: x - 8, y: y - 49, width: size.width, height: size.height),
                         from: NSRect(origin: .zero, size: candyImage?.size ?? size),
                         operation: .sourceOver, fraction: 1, respectFlipped: false, hints: nil)
        NSGraphicsContext.restoreGraphicsState()
    }
}

private final class CandyPointerOverlay {
    private var panel: NSPanel?
    private var view: CandyPointerView?
    private var timer: Timer?
    private var hideCountByDisplay: [CGDirectDisplayID: Int] = [:]
    private var activationObserver: NSObjectProtocol?

    func show() {
        guard panel == nil else { return }
        let union = NSScreen.screens.reduce(NSRect.null) { $0.union($1.frame) }
        guard !union.isNull else { return }
        let pointerView = CandyPointerView(frame: NSRect(origin: .zero, size: union.size))
        pointerView.pointerLocation = NSEvent.mouseLocation
        pointerView.screenOrigin = union.origin
        let overlay = NSPanel(contentRect: union, styleMask: [.borderless, .nonactivatingPanel], backing: .buffered, defer: false)
        overlay.isOpaque = false
        overlay.backgroundColor = .clear
        overlay.hasShadow = false
        overlay.ignoresMouseEvents = true
        overlay.level = NSWindow.Level(rawValue: Int(CGWindowLevelForKey(.cursorWindow)))
        overlay.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary, .stationary]
        overlay.contentView = pointerView
        overlay.orderFrontRegardless()
        panel = overlay
        view = pointerView
        hideSystemCursorWherePossible()
        activationObserver = NSWorkspace.shared.notificationCenter.addObserver(
            forName: NSWorkspace.didActivateApplicationNotification, object: nil, queue: .main
        ) { [weak self] _ in self?.hideSystemCursorWherePossible() }
        timer = Timer.scheduledTimer(withTimeInterval: 1.0 / 60.0, repeats: true) { [weak self] _ in
            self?.view?.pointerLocation = NSEvent.mouseLocation
        }
    }

    private func hideSystemCursorWherePossible() {
        // Reapply on app activation: macOS can restore its native cursor when
        // focus changes. Pair every successful hide with a show when disabled.
        let displays = NSScreen.screens.compactMap { screen -> CGDirectDisplayID? in
            screen.deviceDescription[NSDeviceDescriptionKey("NSScreenNumber")] as? CGDirectDisplayID
        }
        for display in displays {
            if CGDisplayHideCursor(display) == .success { hideCountByDisplay[display, default: 0] += 1 }
        }
    }

    func hide() {
        timer?.invalidate(); timer = nil
        panel?.orderOut(nil); panel = nil; view = nil
        if let activationObserver {
            NSWorkspace.shared.notificationCenter.removeObserver(activationObserver)
            self.activationObserver = nil
        }
        for (display, count) in hideCountByDisplay {
            for _ in 0..<count { CGDisplayShowCursor(display) }
        }
        hideCountByDisplay.removeAll()
    }
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
                let header = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nX-Content-Type-Options: nosniff\r\nCache-Control: no-store\r\nContent-Length: \(json.count)\r\nConnection: close\r\n\r\n"
                connection.send(content: Data(header.utf8) + json, completion: .contentProcessed { _ in connection.cancel() })
            }
        }
        listener?.start(queue: .main)
    }
}

private final class MenuBarPumpkinFallback {
    private var panel: NSPanel?
    func show(in frame: NSRect, target: AnyObject, action: Selector) {
        if panel == nil {
            let panel = NSPanel(contentRect: frame, styleMask: [.borderless, .nonactivatingPanel], backing: .buffered, defer: false)
            panel.isOpaque = false
            panel.backgroundColor = .clear
            panel.hasShadow = false
            panel.hidesOnDeactivate = false
            panel.animationBehavior = .none
            panel.level = NSWindow.Level(rawValue: NSWindow.Level.statusBar.rawValue + 2)
            panel.collectionBehavior = [.canJoinAllSpaces, .stationary]
            let button = NSButton(frame: NSRect(origin: .zero, size: frame.size))
            button.title = "🎃"
            button.isBordered = false
            button.font = NSFont.systemFont(ofSize: 18)
            button.alignment = .center
            button.setAccessibilityLabel("Spooky pumpkin")
            button.target = target
            button.action = action
            button.autoresizingMask = [.width, .height]
            panel.contentView = button
            self.panel = panel
        }
        if panel?.frame != frame { panel?.setFrame(frame, display: true) }
        if panel?.isVisible != true { panel?.orderFrontRegardless() }
    }
    func hide() { panel?.orderOut(nil) }
}

private final class App: NSObject, NSApplicationDelegate, NSWindowDelegate {
    private let defaults = UserDefaults.standard
    private var item: NSStatusItem!
    private var window: NSWindow!
    private var cards: [Effect: PreviewCard] = [:]
    private var loadingBat: LoadingBatView!
    private var isApplying = false
    private var stickers: [StickerWindow] = []
    private let webOverlay = WebOverlay()
    private let menuBarPumpkinFallback = MenuBarPumpkinFallback()
    private var menuBarTimer: Timer?
    private let autumnWidgetOverlay = AutumnWidgetOverlay()
    private let candyPointerOverlay = CandyPointerOverlay()
    private var bridge: Bridge!
    private var folderTimer: Timer?
    private let folderQueue = DispatchQueue(label: "spooky.folder-icons", qos: .utility)
    private var folderApplyPending = false
    private let fm = FileManager.default
    private var support: URL { fm.homeDirectoryForCurrentUser.appendingPathComponent("Library/Application Support/Halloween Decor", isDirectory: true) }
    private var desktop: URL { fm.homeDirectoryForCurrentUser.appendingPathComponent("Desktop", isDirectory: true) }
    private func enabled(_ effect: Effect) -> Bool { defaults.bool(forKey: effect.rawValue) }
    func applicationDidFinishLaunching(_ notification: Notification) {
        try? fm.createDirectory(at: support, withIntermediateDirectories: true)
        InterfaceFont.register()
        item = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        item.button?.image = nil
        item.button?.title = "🎃"
        item.button?.setAccessibilityLabel("Spooky pumpkin")
        item.button?.target = self
        item.button?.action = #selector(showWindow)
        makeWindow()
        bridge = Bridge(snapshot: { [weak self] in Dictionary(uniqueKeysWithValues: Effect.allCases.map { ($0.rawValue, self?.enabled($0) ?? false) }) })
        bridge.start()
        showWindow()
        if enabled(.stickers) { showStickers() }
        if enabled(.webs) { webOverlay.show() }
        if enabled(.wallpaper) {
            if let wallpaper = drawWallpaper() {
                for screen in NSScreen.screens { try? NSWorkspace.shared.setDesktopImageURL(wallpaper, for: screen, options: [:]) }
            }
            autumnWidgetOverlay.show()
        }
        if enabled(.cursor) { candyPointerOverlay.show() }
        if enabled(.folders) { runApplying { [weak self] in self?.applyFolderIcons() } }
        folderTimer = Timer.scheduledTimer(withTimeInterval: 20, repeats: true) { [weak self] _ in if self?.enabled(.folders) == true { self?.applyFolderIcons() } }
        NotificationCenter.default.addObserver(forName: NSApplication.didChangeScreenParametersNotification, object: nil, queue: .main) { [weak self] _ in
            if self?.enabled(.webs) == true { self?.webOverlay.show() }
            if self?.enabled(.wallpaper) == true { self?.autumnWidgetOverlay.show() }
            self?.updateMenuBarPumpkin()
        }
        menuBarTimer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { [weak self] _ in self?.updateMenuBarPumpkin() }
        menuBarTimer?.tolerance = 0.2
        updateMenuBarPumpkin()
    }
    private func updateMenuBarPumpkin() {
        guard let button = item.button, let host = button.window,
              let screen = host.screen ?? NSScreen.screens.first,
              let rightSide = screen.auxiliaryTopRightArea else {
            menuBarPumpkinFallback.hide()
            return
        }
        let buttonFrame = host.convertToScreen(button.convert(button.bounds, to: nil))
        if rightSide.contains(NSPoint(x: buttonFrame.midX, y: buttonFrame.midY)) {
            menuBarPumpkinFallback.hide()
        } else {
            let fallbackFrame = NSRect(x: rightSide.minX + 4, y: rightSide.maxY - 29, width: 27, height: 27)
            menuBarPumpkinFallback.show(in: fallbackFrame, target: self, action: #selector(showWindow))
        }
    }
    private func makeWindow() {
        let availableHeight = NSScreen.main?.visibleFrame.height ?? 960
        let size = NSSize(width: 780, height: max(560, min(760, availableHeight - 24)))
        window = NSWindow(contentRect: NSRect(origin: .zero, size: size), styleMask: [.titled, .closable, .miniaturizable, .fullSizeContentView], backing: .buffered, defer: false)
        window.title = "Spooky"
        window.titleVisibility = .hidden
        window.titlebarAppearsTransparent = true
        window.backgroundColor = .clear
        window.isOpaque = false
        window.hasShadow = true
        window.isMovableByWindowBackground = true
        window.center()
        window.isReleasedWhenClosed = false
        window.delegate = self
        for button in [NSWindow.ButtonType.closeButton, .miniaturizeButton, .zoomButton] {
            window.standardWindowButton(button)?.isHidden = true
        }
        let root = PanelSurface(frame: NSRect(origin: .zero, size: size))
        window.contentView = root
        let heading = NSTextField(labelWithString: "Set your Halloween mood")
        heading.font = InterfaceFont.regular(34)
        heading.textColor = .white
        heading.frame = NSRect(x: 65, y: size.height - 108, width: 570, height: 43)
        root.addSubview(heading)
        let intro = NSTextField(labelWithString: "Choose your Halloween decorations")
        intro.font = InterfaceFont.regular(17)
        intro.textColor = NSColor(calibratedWhite: 0.48, alpha: 1)
        intro.frame = NSRect(x: 65, y: size.height - 143, width: 570, height: 26)
        root.addSubview(intro)
        let close = GlossyCloseButton(frame: NSRect(x: size.width - 103, y: size.height - 108, width: 51, height: 51))
        close.title = ""
        close.isBordered = false
        close.target = self
        close.action = #selector(closeWindow)
        close.setAccessibilityLabel("Close Spooky")
        root.addSubview(close)
        loadingBat = LoadingBatView(frame: NSRect(x: size.width - 253, y: size.height - 161, width: 175, height: 50))
        root.addSubview(loadingBat)
        let scroll = NSScrollView(frame: NSRect(x: 65, y: 35, width: size.width - 130, height: size.height - 207))
        scroll.drawsBackground = false
        scroll.hasVerticalScroller = true
        scroll.autohidesScrollers = true
        scroll.borderType = .noBorder
        let cardHeight: CGFloat = 94
        let cardGap: CGFloat = 10
        let contentHeight = CGFloat(Effect.allCases.count) * cardHeight + CGFloat(Effect.allCases.count - 1) * cardGap
        let list = TopAlignedView(frame: NSRect(x: 0, y: 0, width: scroll.contentSize.width, height: contentHeight))
        scroll.documentView = list
        root.addSubview(scroll)
        let videoRoot = Bundle.main.resourceURL?.appendingPathComponent("Previews")
        for (index, effect) in Effect.allCases.enumerated() {
            let card = PreviewCard(effect: effect, active: enabled(effect), video: videoRoot?.appendingPathComponent(effect.rawValue + ".mp4"), frame: NSRect(x: 0, y: CGFloat(index) * (cardHeight + cardGap), width: scroll.contentSize.width - 8, height: cardHeight))
            card.onSelect = { [weak self] effect in self?.toggle(effect) }
            list.addSubview(card)
            cards[effect] = card
        }
    }
    @objc private func closeWindow() { window.close() }
    @objc private func showWindow() {
        if !item.isVisible { item.isVisible = true }
        item.button?.needsDisplay = true
        updateMenuBarPumpkin()

        // A screen recorder can become the active app. Switch out of accessory
        // mode before activation so macOS is allowed to bring Spooky's window
        // forward from the menu bar while recording is in progress.
        NSApp.setActivationPolicy(.regular)
        NSRunningApplication.current.activate(options: [.activateAllWindows])
        window.orderFrontRegardless()
        window.makeKeyAndOrderFront(nil)
        cards.values.forEach { $0.resumePreview() }
    }
    func windowWillClose(_ notification: Notification) {
        cards.values.forEach { $0.pausePreview() }
        NSApp.setActivationPolicy(.accessory)
    }
    private func toggle(_ effect: Effect) {
        runApplying { [weak self] in self?.applyToggle(effect) }
    }
    private func runApplying(_ work: @escaping () -> Void) {
        guard !isApplying else { return }
        isApplying = true
        loadingBat.start()
        let started = ProcessInfo.processInfo.systemUptime
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.08) { [weak self] in
            work()
            guard let self else { return }
            let remaining = max(0, 0.65 - (ProcessInfo.processInfo.systemUptime - started))
            DispatchQueue.main.asyncAfter(deadline: .now() + remaining) {
                self.loadingBat.stop()
                self.isApplying = false
            }
        }
    }
    private func applyToggle(_ effect: Effect) {
        let active = !enabled(effect)
        if effect == .wallpaper {
            let succeeded = active ? applyWallpaper() : restoreWallpaper()
            if !succeeded {
                cards[effect]?.setActive(enabled(effect))
                let alert = NSAlert()
                alert.messageText = active ? "Couldn’t change the wallpaper" : "Couldn’t restore the previous wallpaper"
                alert.informativeText = "Spooky couldn’t find the original wallpaper file or its macOS backup. Other effects are unaffected."
                alert.runModal()
                return
            }
        }
        defaults.set(active, forKey: effect.rawValue)
        cards[effect]?.setActive(active)
        switch effect {
        case .webs: active ? webOverlay.show() : webOverlay.hide()
        case .stickers: active ? showStickers() : hideStickers()
        case .folders: active ? applyFolderIcons() : restoreFolderIcons()
        case .wallpaper: active ? autumnWidgetOverlay.show() : autumnWidgetOverlay.hide()
        case .cursor: active ? candyPointerOverlay.show() : candyPointerOverlay.hide()
        }
    }
    @objc private func restoreEverything() {
        runApplying { [weak self] in self?.applyRestoreEverything() }
    }
    private func applyRestoreEverything() {
        webOverlay.hide(); autumnWidgetOverlay.hide(); candyPointerOverlay.hide(); hideStickers(); restoreFolderIcons()
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
    func applicationWillTerminate(_ notification: Notification) {
        menuBarTimer?.invalidate()
        menuBarPumpkinFallback.hide()
        candyPointerOverlay.hide()
    }
    private func showStickers() {
        if !stickers.isEmpty { stickers.forEach { $0.orderFrontRegardless() }; return }
        let visible = NSScreen.main?.visibleFrame ?? NSRect(x: 0, y: 0, width: 900, height: 700)
        let columns = max(5, Int(visible.width / 180))
        let rows = Int(ceil(Double(StickerSpec.all.count) / Double(columns)))
        let cellWidth = (visible.width - 60) / CGFloat(columns)
        let cellHeight = (visible.height - 60) / CGFloat(rows)
        let legacyNames = ["scorpio", "taurus", "axe-ghost", "pumpkin-ghost", "virgo-stamp", "halloween-objects", "treat-ghost", "leo-stamp", "pixel-cat"]
        for (index, spec) in StickerSpec.all.enumerated() {
            let key = "sticker.v3.\(spec.name)"
            let origin: NSPoint
            if let saved = defaults.string(forKey: key) { origin = NSPointFromString(saved) }
            else if let oldIndex = legacyNames.firstIndex(of: spec.name),
                    let saved = defaults.string(forKey: "sticker.v2.\(oldIndex)") { origin = NSPointFromString(saved) }
            else {
                let column = index % columns
                let row = index / columns
                origin = NSPoint(x: visible.minX + 30 + CGFloat(column) * cellWidth + (cellWidth - spec.size.width) / 2,
                                 y: visible.maxY - 30 - CGFloat(row + 1) * cellHeight + (cellHeight - spec.size.height) / 2)
            }
            let sticker = StickerWindow(index: index, spec: spec, origin: origin) { [weak self] _, point in self?.defaults.set(NSStringFromPoint(point), forKey: key) }
            NotificationCenter.default.addObserver(forName: NSWindow.didMoveNotification, object: sticker, queue: .main) { [weak self, weak sticker] _ in
                guard let sticker else { return }
                self?.defaults.set(NSStringFromPoint(sticker.frame.origin), forKey: key)
            }
            stickers.append(sticker)
        }
    }
    private func hideStickers() { stickers.forEach { $0.orderOut(nil) } }
    private func folderBackupURL() -> URL { support.appendingPathComponent("folder-backups.json") }
    private func folderStylesURL() -> URL { support.appendingPathComponent("folder-styles.json") }
    private let folderStyleNames = ["maple", "pumpkin", "knit", "stripes", "bat", "kitten"]
    private func folderBackups() -> [String: String] {
        guard let data = try? Data(contentsOf: folderBackupURL()) else { return [:] }
        return (try? JSONDecoder().decode([String: String].self, from: data)) ?? [:]
    }
    private func saveFolderBackups(_ map: [String: String]) { if let data = try? JSONEncoder().encode(map) { try? data.write(to: folderBackupURL(), options: .atomic) } }
    private func folderStyles() -> [String: String] {
        guard let data = try? Data(contentsOf: folderStylesURL()) else { return [:] }
        return (try? JSONDecoder().decode([String: String].self, from: data)) ?? [:]
    }
    private func saveFolderStyles(_ map: [String: String]) { if let data = try? JSONEncoder().encode(map) { try? data.write(to: folderStylesURL(), options: .atomic) } }
    private func hasCustomIcon(_ path: String) -> Bool {
        var bytes = [UInt8](repeating: 0, count: 32)
        let count = path.withCString { p in bytes.withUnsafeMutableBytes { buffer in getxattr(p, "com.apple.FinderInfo", buffer.baseAddress, 32, 0, 0) } }
        return count >= 10 && (UInt16(bytes[8]) << 8 | UInt16(bytes[9])) & 0x0400 != 0
    }
    private func finderSafeIcon(_ source: NSImage) -> NSImage {
        // Crop transparent source padding first, then fit the visible artwork
        // proportionally. This keeps wide/tall designs intact in Finder.
        guard let cgImage = source.cgImage(forProposedRect: nil, context: nil, hints: nil) else { return source }
        let width = cgImage.width
        let height = cgImage.height
        var pixels = [UInt8](repeating: 0, count: width * height * 4)
        let bounds = pixels.withUnsafeMutableBytes { buffer -> CGRect? in
            guard let context = CGContext(
                data: buffer.baseAddress,
                width: width,
                height: height,
                bitsPerComponent: 8,
                bytesPerRow: width * 4,
                space: CGColorSpaceCreateDeviceRGB(),
                bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue | CGBitmapInfo.byteOrder32Big.rawValue
            ) else { return nil }
            context.draw(cgImage, in: CGRect(x: 0, y: 0, width: width, height: height))
            var minX = width, minY = height, maxX = -1, maxY = -1
            for y in 0..<height {
                for x in 0..<width where buffer[(y * width + x) * 4 + 3] > 8 {
                    minX = min(minX, x); minY = min(minY, y)
                    maxX = max(maxX, x); maxY = max(maxY, y)
                }
            }
            guard maxX >= minX, maxY >= minY else { return nil }
            return CGRect(x: minX, y: minY, width: maxX - minX + 1, height: maxY - minY + 1)
        }
        guard let bounds, let visible = cgImage.cropping(to: bounds) else { return source }
        let cropped = NSImage(cgImage: visible, size: NSSize(width: visible.width, height: visible.height))
        let scale = min(464 / CGFloat(visible.width), 464 / CGFloat(visible.height))
        let drawWidth = CGFloat(visible.width) * scale
        let drawHeight = CGFloat(visible.height) * scale
        let canvas = NSImage(size: NSSize(width: 512, height: 512))
        canvas.lockFocus()
        NSGraphicsContext.current?.imageInterpolation = .high
        cropped.draw(
            in: NSRect(x: (512 - drawWidth) / 2, y: (512 - drawHeight) / 2, width: drawWidth, height: drawHeight),
            from: .zero,
            operation: .sourceOver,
            fraction: 1
        )
        canvas.unlockFocus()
        return canvas
    }
    private func applyFolderIcons() {
        guard !folderApplyPending else { return }
        folderApplyPending = true
        folderQueue.async { [weak self] in
            self?.applyFolderIconsNow()
            DispatchQueue.main.async { self?.folderApplyPending = false }
        }
    }
    private func applyFolderIconsNow() {
        guard let urls = try? fm.contentsOfDirectory(at: desktop, includingPropertiesForKeys: [.isDirectoryKey, .isSymbolicLinkKey], options: [.skipsHiddenFiles]) else { return }
        var backups = folderBackups()
        var styles = folderStyles()
        // Migrate the removed skeleton artwork to the pumpkin-only style.
        for (path, style) in Array(styles) where style == "skeleton" { styles[path] = "pumpkin" }
        saveFolderStyles(styles)
        let folderIconDirectory = Bundle.main.resourceURL?.appendingPathComponent("FolderStyles", isDirectory: true)
        for url in urls {
            let values = try? url.resourceValues(forKeys: [.isDirectoryKey, .isSymbolicLinkKey])
            guard values?.isDirectory == true, values?.isSymbolicLink != true else { continue }
            if backups[url.path] == nil {
                let backupName: String
                if hasCustomIcon(url.path) {
                    guard let data = NSWorkspace.shared.icon(forFile: url.path).tiffRepresentation else { continue }
                    backupName = UUID().uuidString + ".tiff"
                    guard (try? data.write(to: support.appendingPathComponent(backupName), options: .atomic)) != nil else { continue }
                } else { backupName = "default" }
                // Persist the original before changing Finder metadata.
                backups[url.path] = backupName; saveFolderBackups(backups)
            }
            let style = styles[url.path] ?? folderStyleNames.randomElement() ?? "pumpkin"
            guard let iconURL = folderIconDirectory?.appendingPathComponent(style + ".png"), let sourceIcon = NSImage(contentsOf: iconURL) else { continue }
            let icon = finderSafeIcon(sourceIcon)
            styles[url.path] = style
            saveFolderStyles(styles)
            if !NSWorkspace.shared.setIcon(icon, forFile: url.path, options: []) {
                styles.removeValue(forKey: url.path); saveFolderStyles(styles)
            }
        }
    }
    private func restoreFolderIcons() {
        folderQueue.async { [weak self] in self?.restoreFolderIconsNow() }
    }
    private func restoreFolderIconsNow() {
        var backups = folderBackups()
        var styles = folderStyles()
        for (path, name) in backups {
            guard fm.fileExists(atPath: path) else {
                backups.removeValue(forKey: path)
                styles.removeValue(forKey: path)
                continue
            }
            let original = name == "default" ? nil : NSImage(contentsOf: support.appendingPathComponent(name))
            if name != "default" && original == nil { continue }
            if NSWorkspace.shared.setIcon(original, forFile: path, options: []) {
                backups.removeValue(forKey: path)
                if name != "default" { try? fm.removeItem(at: support.appendingPathComponent(name)) }
            }
        }
        saveFolderBackups(backups)
        if backups.isEmpty { try? fm.removeItem(at: folderStylesURL()) }
        else { saveFolderStyles(styles) }
    }
    private func wallpaperBackupURL() -> URL { support.appendingPathComponent("wallpaper-backups.json") }
    private func applyWallpaper() -> Bool {
        guard let wallpaper = drawWallpaper() else { return false }
        var backups: [String: String] = [:]
        if let data = try? Data(contentsOf: wallpaperBackupURL()) { backups = (try? JSONDecoder().decode([String: String].self, from: data)) ?? [:] }
        for (index, screen) in NSScreen.screens.enumerated() {
            let key = "screen.\(index)"
            if backups[key] == nil {
                guard let old = NSWorkspace.shared.desktopImageURL(for: screen), old != wallpaper, old.isFileURL else { return false }
                let copy: URL
                if fm.fileExists(atPath: old.path) {
                    copy = support.appendingPathComponent("wallpaper-original-\(index)-\(UUID().uuidString).\(old.pathExtension)")
                    guard (try? fm.copyItem(at: old, to: copy)) != nil else { return false }
                } else {
                    guard let cached = cachedWallpaper(for: old) else { return false }
                    copy = support.appendingPathComponent("wallpaper-original-\(index)-\(UUID().uuidString).png")
                    guard copyWallpaperCacheImage(cached, to: copy) else { return false }
                }
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
    private func cachedWallpaper(for original: URL) -> URL? {
        let sourcePath = original.standardizedFileURL.path
        let key = SHA256.hash(data: Data(sourcePath.utf8)).map { String(format: "%02x", $0) }.joined()
        let cache = fm.homeDirectoryForCurrentUser
            .appendingPathComponent("Library/Containers/com.apple.wallpaper.agent/Data/Library/Caches/com.apple.wallpaper.caches/extension-com.apple.wallpaper.extension.image", isDirectory: true)
        guard let entries = try? fm.contentsOfDirectory(at: cache, includingPropertiesForKeys: nil) else { return nil }
        return entries.first { $0.lastPathComponent.hasPrefix(key + "-") && $0.pathExtension.lowercased() == "bmp" }
    }
    private func copyWallpaperCacheImage(_ source: URL, to destination: URL) -> Bool {
        guard let image = NSImage(contentsOf: source),
              let tiff = image.tiffRepresentation,
              let bitmap = NSBitmapImageRep(data: tiff),
              let png = bitmap.representation(using: .png, properties: [:]) else { return false }
        do { try png.write(to: destination, options: .atomic); return true }
        catch { NSLog("Wallpaper backup failed: %@", error.localizedDescription); return false }
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
    private func drawWallpaper() -> URL? {
        guard let source = Bundle.main.url(forResource: "pumpkin-field", withExtension: "png", subdirectory: "Wallpaper"),
              let artwork = try? Data(contentsOf: source) else { return nil }
        let url = support.appendingPathComponent("spooky-pumpkin-field-v2.png")
        if (try? Data(contentsOf: url)) != artwork {
            guard (try? artwork.write(to: url, options: .atomic)) != nil else { return nil }
        }
        return url
    }

}

let application = NSApplication.shared
private let delegate = App()
application.delegate = delegate
application.setActivationPolicy(.accessory)
application.run()
