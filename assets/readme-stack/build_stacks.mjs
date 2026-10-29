// Render locally with README Stack; no package install or network is needed.
import { renderStackSvg } from "./vendor/render.js";
import { techIconDefinitions, techIconOverrides } from "./tech-icons.mjs";

const groups = [
  ["n8n", "langchain", "autonomous-agents", "llm-orchestration", "comfyui"],
  ["python", "typescript", "javascript", "sql"],
  ["cloudflare", "docker", "serverless-computing", "rest-graphql", "google-cloud", "azure", "firebase", "supabase"],
  ["git", "linux", "figma", "postman", "codex", "claude", "antigravity", "affinity", "android-studio", "blender", "fl-studio", "roblox-studio", "metatrader-5", "tradingview"],
];
const result = { iconDefinitions: techIconDefinitions() };
for (const [variant, width] of [["desktop", 386], ["mobile", 344], ["desktop-static", 386], ["mobile-static", 344]]) {
  result[variant] = groups.map((ids, index) => {
    const params = new URLSearchParams({
      i: ids.join(","), s: "fast", d: index % 2 ? "right" : "left",
      t: "dark", g: "compact", z: "large", l: "on", m: variant.endsWith("-static") ? "static" : "infinite",
    });
    const rendered = renderStackSvg(`/v1/stack.svg?${params}`, {
      width, background: "#000000", iconOverrides: techIconOverrides,
    });
    if (rendered.status !== 200) throw new Error(`Unable to render ${ids.join(",")}`);
    return rendered.svg;
  });
}
process.stdout.write(JSON.stringify(result));
