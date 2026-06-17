#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SKILL_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function usage() {
  return `Usage:
  node scripts/extract_book_codes.mjs <folder> [--out references/book-chapter-card-catalog.json] [--md references/book-chapter-card-catalog.md]

Scans Markdown/TXT/JSON files for Luhmann-style codes and writes a relative-path catalog.
Public catalogs should not contain absolute source paths or raw manuscript excerpts.`;
}

function parseArgs(argv) {
  const args = [...argv];
  const folder = args.shift();
  if (!folder || folder === "-h" || folder === "--help") {
    console.log(usage());
    process.exit(folder ? 0 : 2);
  }
  const options = {
    root: path.resolve(folder),
    out: path.join(SKILL_ROOT, "references", "book-chapter-card-catalog.json"),
    md: path.join(SKILL_ROOT, "references", "book-chapter-card-catalog.md"),
  };
  for (let i = 0; i < args.length; i += 1) {
    if (args[i] === "--out") options.out = path.resolve(args[++i]);
    else if (args[i] === "--md") options.md = path.resolve(args[++i]);
    else throw new Error(`Unknown argument: ${args[i]}`);
  }
  return options;
}

function normalizeTitle(raw = "") {
  return raw
    .replace(/\[\[[^\]|]+\|([^\]]+)\]\]/g, "$1")
    .replace(/\[\[([^\]]+)\]\]/g, "$1")
    .replace(/[`*_#>-]/g, " ")
    .replace(/<br\s*\/?>/gi, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function codeKind(code) {
  if (/^K\d{3}$/.test(code)) return "keyword_index";
  if (/[A-Za-z]/.test(code)) return "luhmann_branch";
  const labels = ["部", "章", "節", "項", "目"];
  return labels[code.split(".").length - 1] || "over_depth";
}

function codeDepth(code) {
  if (/^K\d{3}$/.test(code)) return 0;
  return code.split(".").length;
}

function compareCodes(a, b) {
  const tokenize = (code) =>
    code
      .split(/(?<=\d)(?=[A-Za-z])|(?<=[A-Za-z])(?=\d)|\./)
      .map((part) => (/^\d+$/.test(part) ? { type: "n", value: Number(part) } : { type: "s", value: part.toLowerCase() }));
  const aa = tokenize(a);
  const bb = tokenize(b);
  const len = Math.max(aa.length, bb.length);
  for (let i = 0; i < len; i += 1) {
    if (!aa[i]) return -1;
    if (!bb[i]) return 1;
    if (aa[i].type !== bb[i].type) return aa[i].type === "n" ? -1 : 1;
    if (aa[i].value < bb[i].value) return -1;
    if (aa[i].value > bb[i].value) return 1;
  }
  return 0;
}

function walk(root) {
  const files = [];
  const skip = new Set([".git", "node_modules", "assets", "_epub_work"]);
  for (const name of fs.readdirSync(root)) {
    const full = path.join(root, name);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) {
      if (!skip.has(name)) files.push(...walk(full));
      continue;
    }
    if (/\.(md|markdown|txt|json)$/i.test(name)) files.push(full);
  }
  return files;
}

function fileCode(filePath) {
  const base = path.basename(filePath, path.extname(filePath));
  const match = base.match(/^([0-9]+(?:\.[0-9]+){0,4}(?:\.[A-Za-z][A-Za-z0-9]*|[A-Za-z][A-Za-z0-9]*|(?:\.[0-9]+)*)?)/);
  return match ? match[1] : null;
}

function extractCodes(text) {
  const found = [];
  const codeRe = /^\s*(?:#{1,6}\s*)?(?:[-*]\s*)?`?([0-9]+(?:\.[0-9]+){0,4}(?:\.[A-Za-z][A-Za-z0-9]*|[A-Za-z][A-Za-z0-9]*)?|K\d{3})`?(?:[.、\s:：|-]+)(.+?)\s*$/i;
  const sectionRe = /<!--\s*section:\s*(1(?:\.[1-8]){0,2})\s*-->/gi;
  text.split(/\r?\n/).forEach((line, index) => {
    const match = line.match(codeRe);
    if (match) {
      found.push({
        code: match[1],
        title: normalizeTitle(match[2]),
        kind: codeKind(match[1]),
        depth: codeDepth(match[1]),
        line: index + 1,
      });
    }
  });
  const sections = [...text.matchAll(sectionRe)].map((match) => match[1]);
  return { found, sections: [...new Set(sections)] };
}

function dedupe(entries) {
  const map = new Map();
  for (const entry of entries) {
    if (!map.has(entry.code)) map.set(entry.code, entry);
  }
  return [...map.values()].sort((a, b) => compareCodes(a.code, b.code));
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  if (!fs.existsSync(options.root) || !fs.statSync(options.root).isDirectory()) {
    throw new Error(`Folder not found: ${options.root}`);
  }

  const chapters = walk(options.root).map((file) => {
    const rel = path.relative(options.root, file);
    const text = fs.readFileSync(file, "utf8");
    const primary = fileCode(file);
    const { found, sections } = extractCodes(text);
    const seed = primary
      ? [{ code: primary, title: normalizeTitle(path.basename(file, path.extname(file)).replace(primary, "")), kind: codeKind(primary), depth: codeDepth(primary), line: null }]
      : [];
    const observed = dedupe([...seed, ...found]).map((entry) => {
      const prefixOk = primary ? entry.code === primary || entry.code.startsWith(`${primary}.`) || /^K\d{3}$/.test(entry.code) : true;
      return { ...entry, prefix_status: prefixOk ? "ok" : "off_prefix" };
    });
    return {
      code: primary || rel,
      title: seed[0]?.title || rel,
      kind: primary ? codeKind(primary) : "unclassified_file",
      depth: primary ? codeDepth(primary) : null,
      source_path: rel,
      observed_codes: observed.filter((entry) => entry.prefix_status !== "off_prefix"),
      off_prefix_codes: observed.filter((entry) => entry.prefix_status === "off_prefix"),
      mandala_sections: sections,
    };
  });

  const payload = {
    schema: "auto-luhmann-numberer.catalog.v0.2",
    updated: new Date().toISOString().slice(0, 10),
    source_folder_name: path.basename(options.root),
    privacy_note: "source_path values are relative to the scanned folder; absolute local paths are intentionally omitted.",
    summary: {
      chapters: chapters.map((chapter) => chapter.code).filter((code) => /^[0-9]/.test(code)).sort(compareCodes),
      warnings: [],
    },
    chapters,
  };

  fs.mkdirSync(path.dirname(options.out), { recursive: true });
  fs.mkdirSync(path.dirname(options.md), { recursive: true });
  fs.writeFileSync(options.out, `${JSON.stringify(payload, null, 2)}\n`, "utf8");

  const lines = [
    "# 自動魯曼編號機 catalog",
    "",
    `來源資料夾：\`${payload.source_folder_name}\``,
    "",
    "本 catalog 只保留相對路徑；公開分享前請再次檢查是否含私人章節標題。",
    "",
  ];
  for (const chapter of chapters) {
    lines.push(`## ${chapter.code} ${chapter.title}`.trim(), "");
    lines.push(`來源：\`${chapter.source_path}\``, "");
    for (const entry of chapter.observed_codes) {
      lines.push(`- \`${entry.code}\` ${entry.title || ""} _${entry.kind}_`);
    }
    if (chapter.off_prefix_codes.length) {
      lines.push("", "待校正或跨章引用：");
      for (const entry of chapter.off_prefix_codes) lines.push(`- \`${entry.code}\` ${entry.title || ""} _${entry.kind}_`);
    }
    if (chapter.mandala_sections.length) {
      lines.push("", `Mandala sections：${chapter.mandala_sections.join("、")}`);
    }
    lines.push("");
  }
  fs.writeFileSync(options.md, `${lines.join("\n")}\n`, "utf8");

  console.log(JSON.stringify({ json: options.out, markdown: options.md, chapter_count: chapters.length }, null, 2));
}

main();
