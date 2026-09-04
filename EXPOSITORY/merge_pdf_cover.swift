import Foundation
import CryptoKit
import PDFKit

guard CommandLine.arguments.count == 4 else {
    fputs("usage: merge_pdf_cover.swift COVER.pdf BODY.pdf OUTPUT.pdf\n", stderr)
    exit(64)
}

let coverURL = URL(fileURLWithPath: CommandLine.arguments[1])
let bodyURL = URL(fileURLWithPath: CommandLine.arguments[2])
let outputURL = URL(fileURLWithPath: CommandLine.arguments[3])

guard let cover = PDFDocument(url: coverURL), let body = PDFDocument(url: bodyURL) else {
    fputs("unable to read input PDF\n", stderr)
    exit(66)
}

let merged = PDFDocument()
for document in [cover, body] {
    for index in 0..<document.pageCount {
        guard let page = document.page(at: index) else {
            fputs("unable to read input PDF page\n", stderr)
            exit(65)
        }
        merged.insert(page, at: merged.pageCount)
    }
}

guard let epochText = ProcessInfo.processInfo.environment["SOURCE_DATE_EPOCH"],
      let epoch = TimeInterval(epochText) else {
    fputs("SOURCE_DATE_EPOCH must be set to an integer Unix timestamp\n", stderr)
    exit(64)
}
let timestamp = Date(timeIntervalSince1970: epoch)
merged.documentAttributes = [
    PDFDocumentAttribute.titleAttribute: "Six Matches and a Wider Wedge",
    PDFDocumentAttribute.authorAttribute: "John Savva",
    PDFDocumentAttribute.subjectAttribute: "A public account of the Jensen two-thirds proof candidate",
    PDFDocumentAttribute.creatorAttribute: "Version 1.1 attribution cover merger",
    PDFDocumentAttribute.creationDateAttribute: timestamp,
    PDFDocumentAttribute.modificationDateAttribute: timestamp,
]

guard merged.write(to: outputURL) else {
    fputs("unable to write output PDF\n", stderr)
    exit(74)
}

func replaceExactly(
    _ input: String,
    pattern: String,
    replacement: String,
    expectedCount: Int
) throws -> String {
    let regex = try NSRegularExpression(pattern: pattern)
    let range = NSRange(input.startIndex..<input.endIndex, in: input)
    guard regex.numberOfMatches(in: input, range: range) == expectedCount else {
        throw NSError(
            domain: "merge_pdf_cover",
            code: 1,
            userInfo: [NSLocalizedDescriptionKey: "unexpected PDF metadata structure"]
        )
    }
    return regex.stringByReplacingMatches(
        in: input,
        range: range,
        withTemplate: replacement
    )
}

do {
    let calendar = Calendar(identifier: .gregorian)
    let components = calendar.dateComponents(
        in: TimeZone(secondsFromGMT: 0)!,
        from: timestamp
    )
    let fixedDate = String(
        format: "%04d%02d%02d%02d%02d%02dZ00'00'",
        components.year!, components.month!, components.day!,
        components.hour!, components.minute!, components.second!
    )
    let outputData = try Data(contentsOf: outputURL)
    guard var normalized = String(data: outputData, encoding: .isoLatin1) else {
        throw NSError(
            domain: "merge_pdf_cover",
            code: 2,
            userInfo: [NSLocalizedDescriptionKey: "unable to decode output PDF"]
        )
    }

    normalized = try replaceExactly(
        normalized,
        pattern: "/CreationDate \\(D:[^)]*\\)",
        replacement: "/CreationDate (D:\(fixedDate))",
        expectedCount: 1
    )
    normalized = try replaceExactly(
        normalized,
        pattern: "/ModDate \\(D:[^)]*\\)",
        replacement: "/ModDate (D:\(fixedDate))",
        expectedCount: 1
    )

    let zeroIdentifier = String(repeating: "0", count: 32)
    let identifierPattern = "/ID \\[ <[0-9A-Fa-f]{32}>\\n<[0-9A-Fa-f]{32}> \\]"
    let placeholder = "/ID [ <\(zeroIdentifier)>\n<\(zeroIdentifier)> ]"
    normalized = try replaceExactly(
        normalized,
        pattern: identifierPattern,
        replacement: placeholder,
        expectedCount: 1
    )

    let normalizedData = normalized.data(using: .isoLatin1)!
    let identifier = SHA256.hash(data: normalizedData).prefix(16).map {
        String(format: "%02x", $0)
    }.joined()
    normalized = try replaceExactly(
        normalized,
        pattern: NSRegularExpression.escapedPattern(for: placeholder),
        replacement: "/ID [ <\(identifier)>\n<\(identifier)> ]",
        expectedCount: 1
    )
    try normalized.data(using: .isoLatin1)!.write(to: outputURL, options: .atomic)
} catch {
    fputs("unable to normalize output PDF: \(error.localizedDescription)\n", stderr)
    exit(74)
}
