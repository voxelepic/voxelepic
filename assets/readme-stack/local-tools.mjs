// Additional profile entries, outside the unchanged upstream catalog snapshot.
import { techIconOverrides } from "./tech-icons.mjs";

export const localTools = [
  ["codex", "Codex", "EAE5D9", "https://openai.com/codex/"],
  ["claude", "Claude", "D97757", "https://claude.ai/"],
  ["antigravity", "Antigravity", "4285F4", "https://antigravity.google/press"],
  ["affinity", "Affinity", "AFF078", "https://www.affinity.studio/"],
  ["android-studio", "Android Studio", "3DDC84", "https://developer.android.com/studio"],
  ["blender", "Blender", "E87D0D", "https://www.blender.org/"],
  ["fl-studio", "FL Studio", "FF9900", "https://www.image-line.com/fl-studio/"],
  ["google-cloud", "Google Cloud", "4285F4", "https://cloud.google.com/", "Cloud & Infrastructure"],
  ["azure", "Azure", "0089D6", "https://azure.microsoft.com/", "Cloud & Infrastructure"],
  ["firebase", "Firebase", "FF9100", "https://firebase.google.com/", "Cloud & Infrastructure"],
  ["comfyui", "ComfyUI", "F3FF4F", "https://comfy.org/", "AI & Automation"],
  ["roblox-studio", "Roblox Studio", "00A2FF", "https://create.roblox.com/"],
  ["metatrader-5", "MetaTrader 5", "46A65A", "https://www.metatrader5.com/"],
  ["tradingview", "TradingView", "2962FF", "https://www.tradingview.com/"],
  ["supabase", "Supabase", "3ECF8E", "https://supabase.com/", "Cloud & Infrastructure"],
].map(([id, name, hex, source, category = "Tools & Ecosystem"]) => ({
  id, name, hex, source, category,
  ...techIconOverrides[id],
  provider: "Local image-generated matte 3D illustration",
  rights: {
    status: "illustration", license: "Generated profile artwork; no trademark rights granted",
    notice: "Stylized identifying illustration; not official product artwork or endorsement",
  },
}));
