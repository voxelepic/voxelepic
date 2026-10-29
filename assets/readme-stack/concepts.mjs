// Original neutral symbols for capabilities, rather than product logos.
const glyph = (id, name, body) => ({
  id, name, hex: "BFFB4F", viewBox: "0 0 24 24",
  body: `<g fill="none" stroke="#bffb4f" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">${body}</g>`,
  source: "Local capability symbol; not a product logo",
  provider: "README profile artwork",
  rights: { status: "neutral", license: "Original neutral glyph", notice: "Capability illustration" },
});

export const conceptTools = [
  glyph("autonomous-agents", "Autonomous Agents",
    '<rect x="7" y="7" width="10" height="10" rx="3"/><path d="M12 3v4M12 17v4M3 12h4M17 12h4"/><path d="M10 11v2m4-2v2"/><circle cx="12" cy="2.5" r="1"/><circle cx="12" cy="21.5" r="1"/><circle cx="2.5" cy="12" r="1"/><circle cx="21.5" cy="12" r="1"/>'),
  glyph("llm-orchestration", "LLM Orchestration",
    '<path d="M5 3h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-8l-5 4v-4H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Z"/><path d="m7 10 2-2-2-2m5 6h4"/>'),
  glyph("serverless-computing", "Serverless",
    '<path d="M7 17H6a4 4 0 0 1-.6-8A6.5 6.5 0 0 1 18 7.5 4.8 4.8 0 0 1 19 17h-2"/><path d="m13 10-4 6h4l-2 6 6-8h-5l1-4Z"/>'),
  glyph("rest-graphql", "REST / GraphQL",
    '<path d="m7 7-5 5 5 5m10-10 5 5-5 5m-4-12-2 14"/>'),
];
