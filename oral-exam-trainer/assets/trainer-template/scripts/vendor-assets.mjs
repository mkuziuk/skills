import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const copies = [
  ["node_modules/mathjax/tex-svg-nofont.js", "trainer/frontend/vendor/mathjax/tex-svg-nofont.js"],
  ["node_modules/mathjax/sre", "trainer/frontend/vendor/mathjax/sre"],
  ["node_modules/mermaid/dist/mermaid.min.js", "trainer/frontend/vendor/mermaid/mermaid.min.js"],
];

for (const [from, to] of copies) {
  const source = path.join(root, from);
  const target = path.join(root, to);
  if (!fs.existsSync(source)) {
    throw new Error(`Missing dependency asset: ${from}. Run npm install first.`);
  }
  fs.rmSync(target, { recursive: true, force: true });
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.cpSync(source, target, { recursive: true });
}

console.log("Vendored MathJax and Mermaid assets.");
