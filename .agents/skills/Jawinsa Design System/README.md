# Jawinsa Design System

A design system for **Jawinsa S.A.C.** — a Peruvian multi-service automotive and industrial workshop. The public-facing brand is **Jawinsa Repara**.

This system is built for premium, trustworthy, no-nonsense visual communication: confident like Bosch, refined like Porsche Service, accessible for users who are not tech-native.

---

## Company context

**Jawinsa S.A.C.** operates as an integral hub for automotive and industrial solutions. The strongest customer-facing arm is **Jawinsa Repara**.

### What they do

1. **Jawinsa Repara — Taller multimarca e industrial**
   - **Automotriz & Comercial:** reparación y mantenimiento de autos particulares, camionetas, camiones y volquetes.
   - **Industrial & Logística:** servicio técnico para montacargas y grupos electrógenos.
   - **Diagnóstico:** escáneres multimarca y herramientas de diagnóstico electrónico avanzado (motor, eléctrico, transmisión).

2. **Comercialización de repuestos y consumibles**
   - Repuestos mecánicos y eléctricos.
   - Aceites de motor/transmisión, filtros (aire, aceite, combustible) y consumibles de mantenimiento preventivo.

3. **Modelos de negocio**
   - **B2C:** dueños de vehículos particulares.
   - **B2B:** flotas comerciales, empresas de logística, operadores con grupos electrógenos.
   - **Licitaciones / Grandes corporativos / Estado:** contratos de gran envergadura.

### Audience priority
Equal weight to B2C and B2B, with clear paths into either flow from the landing.

### Visual direction (confirmed with user)
- **Mood:** Bosch confidence + Porsche-service industrial premium.
- **Color:** neutral-heavy palette (whites, greys, blacks) with logo color as accent.
- **Language:** Spanish only.
- **Animation:** moderate — parallax, hover micro-interactions, one signature hero animation.

---

## Sources provided

- `uploads/jawinsa-logo.jpg` — **the file was referenced but did not upload successfully**. The design system currently uses a clean text wordmark as placeholder. **Please re-upload the logo** so the real mark and palette can be wired in.
- No codebase, Figma file, or prior web/print materials were attached.

> ⚠️ Because no real brand assets reached the project, the accent color (warm signal amber) and the wordmark are educated placeholders chosen to match the requested mood. They are designed to swap cleanly once the logo arrives.

---

## Content fundamentals

Tone is **confident, plain-spoken, and competent** — the way a master mechanic talks to you about your truck: no jargon for show, no fluff, but never condescending. Premium feel comes from precision of language, not from adjectives.

### Voice rules

- **Spanish, neutral Latin American** — `usted` for B2B/formal landing copy, `tú` only in informal news posts or social. Default to `usted` in doubt.
- **Short sentences. Active verbs.** "Diagnosticamos. Reparamos. Devolvemos su unidad operativa."
- **No emoji** in the product UI. Permitted only sparingly in social/news. Use proper iconography (Lucide) instead.
- **Casing:** Sentence case for headings. ALL CAPS only for short eyebrow labels (e.g. `LÍNEA INDUSTRIAL`, `SOLICITAR COTIZACIÓN`) — never for full sentences.
- **Numbers carry weight.** Lead with concrete numbers when you have them: "+12 años", "+800 unidades atendidas/año", "24/7 emergencias". Avoid vague claims like "los mejores".
- **Technical specificity is a feature.** Say "escáner OBD-II multimarca" not "tecnología avanzada". Say "grupo electrógeno Cummins / Perkins" not "equipos modernos". Specificity = competence.
- **CTA verbs are direct:** `Solicitar cotización`, `Agendar servicio`, `Llamar ahora`, `Escribir por WhatsApp`. Never "Descubrir más", "Conoce nuestra propuesta", or other marketing fluff.
- **Avoid:** corporate buzzwords (sinergia, holístico, soluciones 360°), exclamation marks, all-caps sentences, generic stock phrases ("calidad garantizada"), more than one adjective per noun.

### Copy examples — yes / no

| ✅ Yes | ❌ No |
|---|---|
| "Reparamos lo que detiene su operación." | "¡Soluciones automotrices integrales para todas tus necesidades!" |
| "Diagnóstico electrónico multimarca en 45 minutos." | "Tecnología de punta para descubrir el problema." |
| "Cotice su servicio. Le respondemos en menos de 24 h." | "Contáctanos y un asesor se pondrá en contacto contigo a la brevedad." |
| "+12 años manteniendo flotas industriales en Lima." | "Empresa líder con amplia trayectoria." |
| "Línea industrial · Montacargas y grupos electrógenos" | "Servicios premium para empresas exigentes" |

---

## Visual foundations

The system is built around the tension between **heavy industrial materials** (steel, graphite, oil-warm amber) and **premium restraint** (generous whitespace, sharp 2 px lines, never-blurry type).

### Color
- **Neutral-heavy.** Backgrounds are paper-white (`#F6F4F0`, slight warm tint to avoid clinical feel) or graphite-black (`#0E1014`). Mid-tones are a calibrated steel scale.
- **Accent — `Signal Amber`** (`#E8732C`). Used sparingly: primary buttons, key data figures, hero headline emphasis, hover underlines. **Never** for body text. Never on amber backgrounds. The amber evokes sodium workshop lamps, welding sparks, Porsche/KTM heritage, and Liqui Moly tins — it is the right kind of "industrial warmth."
- **Semantic colors** (success, warning, danger, info) are desaturated and steel-shifted so they don't compete with the accent.
- Logo color is held in reserve to override `--accent` once provided.

### Typography
- **Display:** `Archivo` (variable; using weights 600–900). Slight condensed feel, mechanical sharpness, perfect for confident headlines.
- **Body / UI:** `Manrope` (variable; 400–700). Modern, neutral, generous x-height — readable on tablet/mobile where Jawinsa's non-tech users will be.
- **Mono / data:** `JetBrains Mono` — for VIN codes, license plates, diagnostic readouts, phone numbers, technical specs.
- **Substitution flag:** these are Google Fonts approximations. If Jawinsa has a brand typeface, swap by editing `colors_and_type.css`.

### Spacing & layout
- **8-point grid.** All spacing tokens are multiples of 4 px (`--space-1` = 4, `--space-2` = 8, `--space-3` = 12, ...).
- **Generous section padding:** 96–160 px vertical on desktop, 48–72 px on mobile. Premium = breathing room.
- **Max content width:** 1280 px (`--max-width`). Hero may go full-bleed.
- **12-column grid** on desktop, **6-column** on tablet, **4-column** on mobile.

### Borders & corners
- **Sharp by default.** Cards and primary surfaces use **2 px radius** (almost square) — industrial, mechanical. Only on-screen "soft" elements like tooltips and small chips use 999 px (pills).
- **Hairlines:** 1 px borders in `--steel-200` on light, `--steel-800` on dark. Sharp, not dotted, never colored.
- **Accent rule:** a 3 px solid amber underline on key headings ("steel-stamped" effect) is a signature.

### Shadows & elevation
- **Restrained.** Shadows are tight and warm — never the puffy "Material" drop shadow.
- Three elevation levels:
  - `--shadow-1`: `0 1px 2px rgb(14 16 20 / 0.06), 0 1px 1px rgb(14 16 20 / 0.04)` — cards at rest.
  - `--shadow-2`: `0 6px 16px -4px rgb(14 16 20 / 0.10), 0 2px 4px rgb(14 16 20 / 0.06)` — hover, dropdowns.
  - `--shadow-3`: `0 24px 48px -12px rgb(14 16 20 / 0.18), 0 8px 16px rgb(14 16 20 / 0.08)` — modals, popovers.

### Backgrounds & imagery
- **Cinematic workshop photography**, warm temperature (3200–4500 K), shallow depth of field. Subjects: hands at work, tool close-ups, vehicles partway dismantled, certification stamps, fleet rows.
- **Full-bleed hero**, half-bleed section breaks. Never tile or repeat.
- **No gradients on text or as primary backgrounds.** A single full-bleed black-to-graphite vertical gradient is permitted behind hero photography as a protection layer for white type.
- **No illustrations.** No isometric vector art, no friendly cartoons, no hand-drawn icons. This is a workshop, not a SaaS startup.
- **No patterns or repeating textures** beyond an optional very subtle 1% noise overlay on dark hero panels to kill banding.

### Animation
- **Easing:** custom `cubic-bezier(0.2, 0.8, 0.2, 1)` for entrances, `cubic-bezier(0.4, 0, 0.6, 1)` for exits.
- **Durations:** 150 ms for hover/state changes, 300–400 ms for entrances, 600–800 ms for hero reveal.
- **Hero signature:** a slow, controlled parallax photograph + a staggered headline reveal (line-by-line, mask-clip) + an amber underline that draws on after the headline lands.
- **No bounce, no elastic.** Heavy materials don't bounce.
- **Hover state:** lighten dark surfaces by ~6%, darken light surfaces by ~3%, no transform jumps. CTAs gain an amber outer ring on focus (`outline: 2px solid var(--accent); outline-offset: 2px`).
- **Press state:** scale 0.98, faster than 100 ms, snap back at 200 ms.

### Transparency & blur
- Sticky header uses a 12 px backdrop blur with 80% paper-white background — *only on scroll*, never at top of page.
- No frosted glass elsewhere.

### Card pattern
- White paper bg, 2 px radius, 1 px `--steel-200` border, `--shadow-1` at rest, `--shadow-2` on hover, no transform, 150 ms ease.
- A 3 px amber accent bar appears on the **top edge** on hover for clickable cards (not the left edge — left-edge accent is the AI-slop tell to avoid).

### Layout rules
- Fixed top header, ~72 px tall, paper bg with backdrop-blur on scroll, hairline bottom border.
- Sticky-bottom-right floating WhatsApp pill on mobile, hidden ≥1024 px (the contact section handles it on desktop).
- Footer is graphite-black, full-bleed, with a 1 px `--steel-700` hairline above the legal row.

---

## Iconography

- **Library:** [Lucide Icons](https://lucide.dev/) (CDN). Stroke-based, 1.5–2 px stroke, geometric, technical feel — matches the system.
- **Sizes:** 16 / 20 / 24 / 32 px. Icons inherit `currentColor`.
- **No emoji** in the product UI. Never.
- **No unicode-as-icon** (e.g. `→`, `★`). Use Lucide equivalents.
- **No custom illustrations** unless they are real photographs.
- Logo and brand mark are SVG (or PNG @2x as fallback) — held in `assets/`. The current placeholder is a CSS wordmark; replace when the real file arrives.

---

## Index — what's in this project

```
README.md                  ← you are here
SKILL.md                   ← Claude Code skill entrypoint
colors_and_type.css        ← CSS variables: colors, type, spacing, shadows
assets/
  logo-placeholder.svg     ← placeholder wordmark (replace with real logo)
fonts/                     ← (Google Fonts loaded via <link>; flag to user to self-host)
preview/                   ← small specimen cards rendered in the Design System tab
ui_kits/
  landing/                 ← Landing page UI kit (hero, services, why, news, contact, footer)
    index.html             ← full landing assembled
    *.jsx                  ← individual components
```

## Caveats & open items

- **Logo not received.** Wordmark + accent color are placeholders. Re-upload to lock in the brand.
- **Fonts are Google Fonts approximations** (`Archivo`, `Manrope`, `JetBrains Mono`). If Jawinsa has a licensed brand typeface, swap in `colors_and_type.css` and drop the files in `fonts/`.
- **Images are placeholders** (solid neutral fills with labels). Replace with real workshop photography to unlock the system's full premium feel.
- **Contact info is fictional** (Lima, Perú placeholders). Wire in real phone, WhatsApp, address, email, hours.
