#!/usr/bin/env node
const fs = require("fs");
const input = process.argv[2];
const out = process.argv.includes("-o")
  ? process.argv[process.argv.indexOf("-o") + 1]
  : process.argv[3];
if (!input || !out) {
  console.error("Usage: json2csv.js input.json -o out.csv");
  process.exit(1);
}
let data = JSON.parse(fs.readFileSync(input, "utf8"));
if (data && !Array.isArray(data) && Array.isArray(data.items)) data = data.items;
if (!Array.isArray(data)) {
  console.error("JSON root must be array");
  process.exit(1);
}
const fields = [];
const seen = new Set();
for (const row of data) {
  for (const k of Object.keys(row || {})) {
    if (!seen.has(k)) {
      seen.add(k);
      fields.push(k);
    }
  }
}
const esc = (v) => {
  if (v == null) return "";
  const s = String(v);
  return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
};
const lines = [fields.join(",")];
for (const row of data) lines.push(fields.map((f) => esc(row[f])).join(","));
fs.writeFileSync(out, lines.join("\n") + "\n");
console.log("Wrote", data.length, "rows ->", out);
