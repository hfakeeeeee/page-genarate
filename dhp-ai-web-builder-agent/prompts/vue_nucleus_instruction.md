Create a modern, professional Vue app for: {instructions}

GOAL
- Generate a clean, business-ready app that strictly follows Nucleus CSS.
- Prefer clarity, alignment, and consistency over flashy visuals.

MUST-HAVES (STRICT)
- Framework: {framework} with {language}
- Vue 3 + Composition API using <script setup>
- Router: Vue Router 4 (lazy-load route components)
- Files: 7–15 total
- Images: placehold.co only (e.g., https://placehold.co/1200x800?text=Hero+Image)
- Nucleus CSS: Use tokens, classes, spacing, and breakpoints everywhere
- No Tailwind
- Import "@nucleus/css/dist/nucleus.css" in entry file

NUCLEUS DESIGN PRINCIPLES
- Minimal, enterprise palette; WCAG AA contrast
- Subtle micro-interactions (150–250ms) for hover/focus
- Typography via Nucleus classes only
- Consistent spacing using Nucleus spacing tokens only

TOKENS & CLASSES (ESSENTIAL)
- Colors (use tokens only):
  - Primary: --nt-color-accent-primary-1, --nt-color-accent-primary-2
  - Secondary: --nt-color-accent-secondary-1, -2, -3
  - Background: --nt-color-background-base, -gray-050, -gray-100
  - Text: --nt-color-font-primary, -secondary, -reversed
  - Action: --nt-color-action-primary-default, -active
- Typography:
  - Classes: .nb-h1.. .nb-h6, .nb-paragraph
  - Family/weights/sizes/line-heights: use Nucleus tokens only
- Layout & Lists:
  - .nb-container (max-width 1500px, centered)
  - .nb-list, .nb-list-item
- Buttons:
  - .nb-btn, .nb-btn--primary, .nb-btn--secondary, .nb-btn.is-small
- Visuals:
  - Shadows: --nt-shadow-card
  - Radius: --nt-size-radius-rounded
  - Borders: --nt-size-borders-container

SPACING & BREAKPOINTS
- Use ONLY: --nt-size-spacing-2/4/8/12/16/20/24/28/32/36/48/56/72
- Sections: vertical padding = 56 (or 72 for hero)
- Grid gaps: 24
- Breakpoints: 576px, 768px, 1200px, 1500px (mobile-first)

LAYOUT & ALIGNMENT RULES
- Every page uses .nb-container; identical left alignment rails
- Header: grid layout, items perfectly centered vertically, hit area ≥ spacing-48
- Cards: equal height across breakpoints; consistent internal structure
- Sticky footer on short pages (app shell with main flex: 1)
- Buttons in a row share identical heights and alignment
- Reserve image sizes to prevent CLS (hero 1200x800, cards 400x300, avatars 100x100)

INTERACTION
- Use CSS transitions only: box-shadow/background/transform 180ms ease
- Subtle lift: transform: translateY(-2px) on hover is OK

RESPONSIVE
- Mobile-first; ensure ≥2 items per row ≥768px when using grids
- No wrapping/overflow that breaks alignment at 576/768/1200/1500px

ROUTING & PAGES (COMPLEXITY)
- Analyze instructions:
  - Simple/basic/minimal/quick/starter → 3–5 pages
  - Full/complete/comprehensive/advanced/complex/business → 8–12 pages
  - Otherwise → 5–7 pages
- Always build relevant pages for the site type with consistent layout

TECH REQUIREMENTS
- Dependencies: vue, vue-router, @nucleus/css:^6.46.0
- DevDependencies: vite, @vitejs/plugin-vue, vue-tsc (for TS), @types/* (for TS)
- Vite config must include Vue plugin and server: { host: true, cors: true, allowedHosts: true }
- Entry must import "@nucleus/css/dist/nucleus.css"
- All code should run without extra steps
- Avoid Vue Transition components; prefer CSS transitions

OUTPUT FORMAT (RETURN ONLY VALID JSON)
{
  "project_name": "{project_name}",
  "framework": "{framework}",
  "language": "{language}",
  "instructions": "Brief instruction of what you built",
  "files": {
    "package.json": "Complete package.json with Vue 3, Vite, Vue Router, @nucleus/css:^6.46.0, @vitejs/plugin-vue; include scripts to start dev server; do not add type module",
    "index.html": "HTML with meta tags; includes script to src/main.{main_ext}",
    "vite.config.{file_ext}": "Vite with @vitejs/plugin-vue and server: {host:true, cors:true, allowedHosts:true}",
    "src/main.{main_ext}": "Vue entry with router; must import '@nucleus/css/dist/nucleus.css'",
    "src/App.vue": "App shell with <router-view/> and Nucleus layout",
    "src/style.css": "Global styles using only Nucleus tokens",
    "src/router/index.{main_ext}": "Router with lazy-loaded routes",
    "src/components/Layout.vue": "Header/footer with perfect alignment using Nucleus classes",
    "src/components/Navigation.vue": "router-link styled with .nb-btn and Nucleus tokens",
    "src/pages/Home.vue": "Hero using Nucleus typography/colors and placehold.co image",
    "CREATE PAGES BASED ON COMPLEXITY": "Simple (3–5) | Moderate (5–7) | Full (8–12); maintain consistent layout and tokens"
  }
}

QA CHECKLIST (AUTO-VERIFY BEFORE OUTPUT)
- Header/nav text vertically centered across routes
- Footer pinned bottom on short pages
- Card grids have equal-height cards at all breakpoints
- All spacing uses Nucleus spacing tokens only (no raw px/rem)
- All sections use .nb-container with aligned rails
- All images use placehold.co with explicit sizes and stable aspect ratios
- Buttons share identical heights and alignment in any row
- No overflow/wrap issues at 576/768/1200/1500px
- Focus states visible and consistent
- Colors strictly from Nucleus palette; headings use --nt-color-font-heading