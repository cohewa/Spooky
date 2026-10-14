import AppKit
import UniformTypeIdentifiers

let output = URL(fileURLWithPath: "macos/PreviewScene", isDirectory: true)
try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
func save(_ image: NSImage, _ name: String, size: NSSize) throws {
    let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(size.width), pixelsHigh: Int(size.height), bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
    image.draw(in: NSRect(origin: .zero, size: size))
    NSGraphicsContext.restoreGraphicsState()
    try bitmap.representation(using: .png, properties: [:])!.write(to: output.appendingPathComponent(name + ".png"))
}
for (name, bundle) in [("finder", "com.apple.finder"), ("safari", "com.apple.Safari"), ("calendar", "com.apple.iCal"), ("notes", "com.apple.Notes"), ("settings", "com.apple.systempreferences")] {
    if let app = NSWorkspace.shared.urlForApplication(withBundleIdentifier: bundle) {
        try save(NSWorkspace.shared.icon(forFile: app.path), name, size: NSSize(width: 128, height: 128))
    }
}
try save(NSWorkspace.shared.icon(for: .folder), "folder", size: NSSize(width: 128, height: 128))
if let wallpaper = NSImage(contentsOfFile: "/System/Library/Desktop Pictures/Sonoma.heic") {
    try save(wallpaper, "desktop", size: NSSize(width: 1280, height: 800))
}
