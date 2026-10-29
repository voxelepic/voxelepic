// Generated transparent atlases, each embedded once per panel for offline rendering.
import { readFileSync } from "node:fs";

const originalIconIds = [
  "n8n", "langchain", "autonomous-agents", "llm-orchestration",
  "python", "typescript", "javascript", "sql",
  "cloudflare", "docker", "serverless-computing", "rest-graphql",
  "git", "linux", "figma", "postman",
];

const additionalIconIds = ["codex", "claude", "antigravity", "affinity", "android-studio", "blender", "fl-studio"];
const cloudIconIds = ["google-cloud", "azure", "firebase"];
const studioTradingIconIds = ["roblox-studio", "metatrader-5", "tradingview"];
export const techIconIds = [...originalIconIds, ...additionalIconIds, ...cloudIconIds, "comfyui", ...studioTradingIconIds, "supabase"];

// Source bounds measured from the generated atlas; the artwork's padding is
// intentionally not assumed to be an exact grid. Each viewport adds breathing
// room and centers the complete silhouette instead of clipping wide marks.
const bounds = [
  [38, 97, 327, 321], [355, 111, 629, 333], [649, 66, 924, 334], [957, 68, 1232, 330],
  [51, 368, 313, 625], [365, 377, 607, 619], [669, 376, 908, 620], [985, 370, 1198, 629],
  [36, 693, 343, 864], [363, 667, 647, 894], [651, 658, 929, 900], [972, 651, 1219, 920],
  [48, 927, 312, 1189], [360, 926, 609, 1197], [685, 924, 888, 1195], [963, 935, 1218, 1192],
];

const additionalBounds = [
  [80, 98, 396, 408], [499, 77, 843, 414], [920, 86, 1302, 408], [1391, 97, 1694, 408],
  [87, 474, 389, 816], [473, 483, 848, 812], [1003, 466, 1247, 828],
];

const cloudBounds = [[77, 135, 688, 619], [808, 116, 1392, 630], [1572, 65, 2071, 658]];

export const techIconOverrides = Object.fromEntries(techIconIds.map((id) => [id, {
  path: null,
  viewBox: "0 0 100 100",
  body: `<use href="#tech-icon-${id}" width="100" height="100"/>`,
}]));

export function techIconDefinitions() {
  const atlases = [
    ["tech-atlas", "tech-icons.png", originalIconIds, bounds],
    ["tools-atlas", "tools-extra.png", additionalIconIds.slice(1), additionalBounds.slice(1)],
    ["codex-artwork", "codex.png", ["codex"], [[0, 0, 1254, 1254]]],
    ["cloud-atlas", "cloud-extra.png", cloudIconIds, cloudBounds],
    ["comfyui-artwork", "comfyui.png", ["comfyui"], [[218, 259, 1059, 1051]]],
    ["studio-trading-atlas", "studio-trading-extra.png", studioTradingIconIds,
      [[93, 74, 676, 661], [790, 76, 1386, 637], [1486, 233, 2131, 580]]],
    ["supabase-artwork", "supabase.png", ["supabase"], [[261, 191, 992, 1081]]],
  ].map(([atlasId, filename, ids, sourceBounds]) => {
    const png = readFileSync(new URL(`./matte/${filename}`, import.meta.url));
    const width = png.readUInt32BE(16);
    const height = png.readUInt32BE(20);
    // Viewports trim only the padding; preserve the generated PNG and alpha.
    const symbols = ids.map((id, index) => {
      const [left, top, right, bottom] = sourceBounds[index];
      const padding = 3;
      // A wide symbol's viewport can expose adjacent atlas rows when fitted
      // into a square. Clip in atlas coordinates, before aspect-ratio fitting.
      if (id === "cloudflare") {
        const clipId = `tech-icon-${id}-crop`;
        return `<clipPath id="${clipId}" clipPathUnits="userSpaceOnUse"><rect x="${left-padding}" y="${top-padding}" width="${right-left+padding*2}" height="${bottom-top+padding*2}"/></clipPath><symbol id="tech-icon-${id}" viewBox="${left-padding} ${top-padding} ${right-left+padding*2} ${bottom-top+padding*2}" overflow="hidden"><use href="#${atlasId}" clip-path="url(#${clipId})"/></symbol>`;
      }
      return `<symbol id="tech-icon-${id}" viewBox="${left-padding} ${top-padding} ${right-left+padding*2} ${bottom-top+padding*2}" overflow="hidden"><use href="#${atlasId}"/></symbol>`;
    }).join("");
    return `<image id="${atlasId}" width="${width}" height="${height}" href="data:image/png;base64,${png.toString("base64")}"/>${symbols}`;
  }).join("");
  return `<defs xmlns="http://www.w3.org/2000/svg">${atlases}</defs>`;
}
