---
name: jawinsa-design
description: Use this skill to generate well-branded interfaces and assets for Jawinsa S.A.C. (Jawinsa Repara), a Peruvian multimarca automotive + industrial workshop. Premium-industrial Spanish-language brand. Use for production code or throwaway prototypes/mocks/slides.
user-invocable: true
---

Read the `README.md` file within this skill, and explore the other available files.

Quick map:
- `README.md` — company context, content fundamentals, visual foundations, iconography.
- `colors_and_type.css` — CSS variables (color, type, spacing, radii, shadows, motion). Always include this.
- `assets/` — logo (currently a placeholder wordmark — flag to the user if you use it).
- `ui_kits/landing/` — landing-page UI kit (Hero, Services, WhyUs, News, Contact, Footer) with `index.html` demo and JSX components.
- `preview/` — small specimen cards (not for production use; reference only).

When designing or coding:
- Tone is Spanish, formal-ish (`usted`), concrete, confident, no fluff. Specific numbers > vague claims. No emoji. Never marketing buzzwords like "soluciones 360°".
- Visual mood: Bosch confidence + Porsche-service premium. Neutral-heavy palette, signal-amber accent used sparingly.
- Sharp corners (2 px), tight shadows, no bouncy animations, no isometric illustrations.
- Iconography: Lucide. Cards: white, hairline border, top-edge amber accent on hover (never left-edge).
- Photography: warm, cinematic workshop scenes; never stock-vector illustrations.

If creating visual artifacts (slides, mocks, throwaway prototypes), copy assets out and produce static HTML files for the user to view. If working on production code, copy the relevant assets and follow the foundations document.

If the user invokes this skill with no other guidance, ask them what they want to build, then act as an expert designer outputting either HTML artifacts or production code.

**Open caveats (please confirm with user before shipping):**
- The Jawinsa logo file did not upload to the source project — `assets/logo-placeholder.svg` is a typographic stand-in. Replace before any production use.
- Fonts are Google Fonts approximations (Archivo, Manrope, JetBrains Mono). If Jawinsa licenses a brand typeface, swap in `colors_and_type.css`.
- Accent color (signal amber `#E8732C`) was chosen to match the requested industrial-premium mood — verify it harmonizes with the real logo once received.
