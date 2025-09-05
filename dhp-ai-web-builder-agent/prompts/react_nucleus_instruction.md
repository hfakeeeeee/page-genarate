Create a STUNNING, ultra-modern React app for: {instructions}

DESIGN EXCELLENCE REQUIREMENTS:
- Framework: {framework} with {language}
- Build: 7-15 files with seamless React Router navigation
- Style: Advanced Nucleus CSS with CLEAN, MODERN aesthetics (NOT overly colorful)
- Color Philosophy: Minimal, sophisticated, professional design using Nucleus design system
- Animations: Subtle, smooth transitions and micro-interactions
- Typography: Clean, readable fonts using Nucleus typography system

NUCLEUS CSS DESIGN SYSTEM - MANDATORY:
- Primary Colors: --nt-color-accent-primary-1 (#78be20), --nt-color-accent-primary-2 (#5c9a1b)
- Secondary Colors: --nt-color-accent-secondary-1 (#114A21), --nt-color-accent-secondary-2 (#af0061), --nt-color-accent-secondary-3 (#003057)
- Tertiary Colors: --nt-color-accent-tertiary-1 (#66bbc4), --nt-color-accent-tertiary-2 (#fb5373), --nt-color-accent-tertiary-3 (#ffc600)
- Background Colors: --nt-color-background-base (#ffffff), --nt-color-background-gray-050 (#f8f8f8), --nt-color-background-gray-100 (#efeff1)
- Background Decorative: --nt-color-background-decorative (#114a21), --nt-color-background-decorative-light (#eff5e6)
- Background Accent: --nt-color-background-accent (#003057), --nt-color-background-accent-light (#e7f1f6)
- Text Colors: --nt-color-font-primary (#3a3b3d), --nt-color-font-secondary (#53575a), --nt-color-font-reversed (#ffffff)
- Heading Colors: --nt-color-font-heading (#114A21), --nt-color-font-heading-large (#5c9a1b)
- Action Colors: --nt-color-action-primary-default (#5c9a1b), --nt-color-action-primary-active (#487815)
- Link Colors: --nt-color-action-link-default (#007481), --nt-color-action-link-active (#005b68), --nt-color-action-link-visited (#00444d)
- State Colors: --nt-color-action-disabled (#c8c8c8), --nt-color-action-reversed (#ffffff)
- Grayscale System: --nt-color-grayscale-100 (#efeff1), --nt-color-grayscale-200 (#c8c8c8), --nt-color-grayscale-400 (#909696), --nt-color-grayscale-500 (#707373), --nt-color-grayscale-700 (#53575a), --nt-color-grayscale-800 (#3a3b3d), --nt-color-grayscale-900 (#15191b)
- Notification Colors: --nt-color-notification-high (#aa0008), --nt-color-notification-medium (#be5000), --nt-color-notification-low (#0062a6)
- Utility Colors: --nt-color-utility-success (#008200), --nt-color-utility-error (#aa0008), --nt-color-utility-disabled (#c8c8c8)
- AVOID: Multiple bright colors, rainbow gradients, too many accent colors
- USE: Professional, enterprise-grade Nucleus color system

NUCLEUS CSS COMPONENT CLASSES - CRITICAL:
- Buttons: .nb-btn, .nb-btn--primary, .nb-btn--secondary, .nb-btn.is-small
- Typography: .nb-h1, .nb-h2, .nb-h3, .nb-h4, .nb-h5, .nb-h6, .nb-paragraph
- Layout: .nb-container (max-width 1500px, centered)
- Lists: .nb-list, .nb-list-item
- Use CSS custom properties (CSS variables) for colors: var(--nt-color-*)

NUCLEUS CSS LAYOUT STANDARDS - CRITICAL:
- Container: .nb-container (max-width 1500px, centered with side padding)
- Spacing System: Use --nt-size-spacing-* variables consistently (2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 48, 56, 72)
- Responsive Breakpoints: --nt-breakpoint-small (576px), --nt-breakpoint-medium (768px), --nt-breakpoint-large (1200px), --nt-breakpoint-x-large (1500px)
- Z-Index System: --nt-z-index-0 (0), --nt-z-index-100 (100), --nt-z-index-200 (200), --nt-z-index-300 (300), --nt-z-index-400 (400), --nt-z-index-500 (500), --nt-z-index-top (99999), --nt-z-index-bottom (-100)
- NO layout breaks on mobile, tablet, or desktop
- Consistent component sizing across all pages using Nucleus variables
- Use CSS Grid and Flexbox with Nucleus spacing variables
- Maintain visual hierarchy using Nucleus typography and spacing scales

PERFECT ALIGNMENT RULES - MANDATORY:
- **Consistent Margins**: Use only Nucleus spacing variables (--nt-size-spacing-*) for ALL margins and padding
- **Grid Alignment**: Use CSS Grid with gap: var(--nt-size-spacing-24) for consistent spacing between grid items
- **Flexbox Alignment**: Use justify-content and align-items with consistent spacing using Nucleus variables
- **Text Alignment**: Ensure headings, paragraphs, and buttons align perfectly using common baseline
- **Vertical Rhythm**: Maintain consistent vertical spacing between sections using --nt-size-spacing-48 or --nt-size-spacing-56
- **Card Alignment**: All cards must have identical padding: var(--nt-size-spacing-24) and margin: var(--nt-size-spacing-16)
- **Button Alignment**: Buttons in the same row must have identical height and vertical alignment
- **Image Alignment**: Images must be properly centered and sized with consistent aspect ratios
- **Container Consistency**: All page sections must use .nb-container for consistent max-width and centering
- **Navigation Alignment**: Navigation items must be perfectly aligned with consistent spacing

UI QUALITY ENHANCEMENT ADDENDUM — MANDATORY:
Header & Navigation: Perfect Centering
- Header Shell: Use .nb-container inside <header>; layout with display: grid; grid-auto-flow: column; align-items: center; justify-content: space-between; column-gap: var(--nt-size-spacing-24); min-height: var(--nt-size-spacing-56);.
Vertical Centering: All header text and nav items are vertically centered within the header’s min-height.
- Hit Area: Each nav item’s clickable region ≥ var(--nt-size-spacing-48) in height.
- Alignment Rail: Left edge of logo, first headline, and main content share the same left rail.
- Active/Focus States: Use var(--nt-color-action-primary-active) for active; maintain visible outline or box-shadow for :focus-visible.
Equal-Height Cards & Uniform Boxes
- Uniform Card Pattern (applies to all cards): Padding var(--nt-size-spacing-24), Radius var(--nt-size-radius-rounded), Border var(--nt-size-borders-container) solid var(--nt-color-grayscale-200), Shadow var(--nt-shadow-card).
- Equal Height Rule: Grid containers must align-items: stretch; cards must display: flex; flex-direction: column; height: 100%;.
- Consistent Internals: Card image (fixed aspect), title, meta, body, and CTA sections are always present (placeholders allowed) so heights match.
- Line Clamp: Truncate long text to prevent uneven heights (-webkit-line-clamp: 2 for titles, 3 for body; provide graceful fallback).
Sticky Footer on Short Pages
- App Shell: Keep footer pinned to the bottom on short pages:
html, body, #root { height: 100%; }
.app-shell { min-height: 100dvh; display: flex; flex-direction: column; }
main { flex: 1; }
- Footer Spacing: Use var(--nt-size-spacing-24) for internal footer spacing; avoid arbitrary margins.
Section & Grid Consistency
- Section Spacing: Major sections use vertical padding top & bottom of var(--nt-size-spacing-56) (or --nt-size-spacing-72 for large hero).
- Grid System: Use display: grid; gap: var(--nt-size-spacing-24); grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));.
- No Orphans: Ensure ≥ 2 items per row at ≥ 768px width; single column allowed below 768px.
- Typography Baseline & Rhythm
- Baseline Lock: Body text uses line-height: var(--nt-font-line-height-open); headings use Nucleus sizes.
- Max Line Length: Long-form text constrained to ~60–75 characters.
- Hierarchy: Use .nb-h1..nb-h6 and .nb-paragraph only; no ad-hoc font sizes.
Image Ratios & Media Treatment
- Hero: aspect-ratio: 3 / 2 (use https://placehold.co/1200x800?text=Hero+Image)
- Cards: aspect-ratio: 4 / 3 (use https://placehold.co/400x300?text=Card+Image)
- Avatars: 1 / 1 (use https://placehold.co/100x100?text=Avatar)
- Object Fit: img { width: 100%; height: auto; aspect-ratio: set per context; object-fit: cover; }
- No Layout Shift: Reserve image dimensions to avoid CLS.
- Responsive Behavior (No Breaks)
- Mobile-First with breakpoints at 576px, 768px, 1200px, 1500px.
- Header Wrap: Nav converts to a menu button ≤ 768px; menu uses the same spacing tokens.
- Equal Heights Persist: Cards remain equal height at all breakpoints with align-items: stretch; height: 100%;.
Interaction & Motion
- Micro-Interactions: Transitions (150–250ms) on hover/focus for cards and buttons:
- transition: box-shadow 180ms ease, transform 180ms ease, background-color 180ms ease;
- Subtle elevation only (e.g., transform: translateY(-2px) on hover); avoid over-animation.
- Color & Contrast Integrity
- Tokens Only: All colors come from Nucleus tokens.
- Contrast: Ensure WCAG AA for text; use --nt-color-font-reversed on dark backgrounds.

UI QA CHECKLIST — AUTO-VERIFY BEFORE OUTPUT
- The generated app must pass all items:
- Header text and nav items are vertically centered across all routes.
- Footer sits at the bottom on short-content pages (no mid-viewport floating).
- Card grids show uniform card heights per row at every breakpoint.
- All spacing uses only --nt-size-spacing-*; no raw px/rem values.
- All sections use .nb-container and maintain identical alignment rails.
- All images use placehold.co with explicit dimensions and stable aspect ratios.
- Buttons in any row share identical heights and vertical alignment.
- No text overflows or layout wraps that break alignment at 576/768/1200/1500px.
- Focus states are visible and consistent for keyboard navigation.
- No color outside the Nucleus palette; headings use --nt-color-font-heading.

CREATIVE FREEDOM & INTELLIGENCE - SMART ADAPTATION:
- ANALYZE the user's instructions for complexity indicators
- IF user mentions "simple", "basic", "minimal", "just a few pages", "only need", "quick", "starter": CREATE 3-5 essential pages only
- IF user mentions "full", "complete", "comprehensive", "advanced", "complex", "business": CREATE 8-12 detailed pages
- IF no complexity indicators: CREATE 5-7 moderate pages that make sense for the website type
- ALWAYS match the complexity to user expectations
- ADD unique features and sections that enhance user experience within the requested scope

IMAGE REQUIREMENTS - MANDATORY:
- ALL images must use placehold.co URLs: https://placehold.co/WIDTHxHEIGHT
- Examples: https://placehold.co/800x600, https://placehold.co/400x300, https://placehold.co/1200x800
- NO internal image sources (./assets/, /images/, etc.)
- Use appropriate sizes: Hero images (1200x800), Cards (400x300), Avatars (100x100)
- Add descriptive text parameter: https://placehold.co/800x600?text=Hero+Image

NUCLEUS CSS TYPOGRAPHY SYSTEM - CRITICAL:
- Font Family: --nt-font-family-default (FS Humana, Calibri, Helvetica, Arial, SF Pro Text, Roboto, sans-serif)
- Font Weights: --nt-font-weight-light (300), --nt-font-weight-regular (400), --nt-font-weight-medium (500), --nt-font-weight-semibold (600), --nt-font-weight-bold (700)
- Font Sizes: --nt-size-font-sm (0.9375rem), --nt-size-font-base (1rem), --nt-size-font-lg (1.1875rem), --nt-size-font-xl (1.25rem), --nt-size-font-2xl (1.375rem), --nt-size-font-3xl (1.5rem), --nt-size-font-4xl (1.75rem), --nt-size-font-5xl (2rem), --nt-size-font-6xl (2.25rem), --nt-size-font-7xl (2.625rem), --nt-size-font-8xl (3.125rem)
- Line Heights: --nt-font-line-height-none (1), --nt-font-line-height-compact (1.25), --nt-font-line-height-comfortable (1.375), --nt-font-line-height-open (1.5)
- Heading Hierarchy: h1 uses --nt-size-font-6xl (2.25rem), h2 uses --nt-size-font-4xl (1.75rem), h3 uses --nt-size-font-2xl (1.375rem), h4 uses --nt-size-font-xl (1.25rem), h5 uses --nt-size-font-lg (1.1875rem), h6 uses --nt-size-font-base (1rem)
- Typography Classes: .nb-h1, .nb-h2, .nb-h3, .nb-h4, .nb-h5, .nb-h6, .nb-paragraph
- Text Colors: Use --nt-color-font-primary for body text, --nt-color-font-heading for headings, --nt-color-font-secondary for supporting text

NUCLEUS CSS SPACING SYSTEM - CRITICAL:
- Spacing Variables: --nt-size-spacing-2 (0.125rem), --nt-size-spacing-4 (0.25rem), --nt-size-spacing-8 (0.5rem), --nt-size-spacing-12 (0.75rem), --nt-size-spacing-16 (1rem), --nt-size-spacing-20 (1.25rem), --nt-size-spacing-24 (1.5rem), --nt-size-spacing-28 (1.75rem), --nt-size-spacing-32 (2rem), --nt-size-spacing-36 (2.25rem), --nt-size-spacing-48 (3rem), --nt-size-spacing-56 (3.5rem), --nt-size-spacing-72 (4.5rem)
- Common Usage: Small gaps (8-12), Medium gaps (16-24), Large gaps (32-48), Section gaps (56-72)
- Consistent Spacing: Use systematic spacing throughout all components and layouts

NUCLEUS CSS VISUAL ELEMENTS - CRITICAL:
- Border Radius: --nt-size-radius-sharp (0), --nt-size-radius-fine (0.25rem), --nt-size-radius-rounded (0.5rem), --nt-size-radius-smooth (0.75rem), --nt-size-radius-full (99rem)
- Shadows: --nt-shadow-popover (0 0.125rem 0.25rem rgba(21, 25, 27, 0.12)), --nt-shadow-card (0 0.25rem 0.5rem rgba(21, 25, 27, 0.2)), --nt-shadow-selection (0 0.5rem 1rem rgba(17, 74, 33, 0.2))
- Border Sizes: --nt-size-borders-button (0.125rem), --nt-size-borders-container (0.0625rem), --nt-size-borders-form (0.0625rem), --nt-size-borders-form-hover (0.125rem), --nt-size-borders-form-selected (0.1875rem), --nt-size-borders-decoration (0.3125rem)
- Icon Sizes: Small icons: --nt-size-icon-sm-1 (1rem), --nt-size-icon-sm-2 (1.25rem), --nt-size-icon-sm-3 (1.5rem), --nt-size-icon-sm-4 (2rem); Large icons: --nt-size-icon-lg-1 (2.5rem) to --nt-size-icon-lg-6 (9rem)

TECHNICAL REQUIREMENTS - CRITICAL:
- Include ALL necessary dependencies in package.json
- Dependencies: react, react-dom, react-router-dom, @nucleus/css: ^6.46.0
- DevDependencies: vite, @vitejs/plugin-react, @types/* for TypeScript
- Ensure vite.config includes React plugin import and usage
- MANDATORY: Import "@nucleus/css/dist/nucleus.css" in main entry file
- All generated code must work without additional installation steps
- NO Tailwind CSS dependencies or imports

RESPONSIVE DESIGN REQUIREMENTS:
- Use Nucleus breakpoint variables for responsive design in CSS media queries
- Breakpoints: --nt-breakpoint-small (576px), --nt-breakpoint-medium (768px), --nt-breakpoint-large (1200px), --nt-breakpoint-x-large (1500px)
- Media Query Examples: `@media (min-width: 768px) { ... }` for medium screens and up
- Text scaling using Nucleus font size variables (--nt-size-font-sm to --nt-size-font-8xl)
- Image responsiveness with proper aspect ratios and max-width: 100%
- Navigation that works on all screen sizes using Nucleus components (.nb-btn, .nb-container)
- Mobile-first approach: Start with mobile styles, then enhance for larger screens
- Use CSS Grid and Flexbox with Nucleus spacing variables for flexible layouts
- Ensure touch targets are at least 44px (--nt-size-spacing-48) for mobile accessibility

STRUCTURE:
- React 18+ with modern hooks and clean patterns
- React Router with smooth, consistent navigation
- Consistent component architecture across pages
- Proper error boundaries and loading states
- Clean code organization and naming
- Use Nucleus CSS classes and variables throughout

OUTPUT FORMAT:
Return ONLY valid JSON with properly escaped strings:
{{
  "project_name": "{project_name}",
  "framework": "{framework}",
  "language": "{language}",
  "instructions": "Brief instruction of what you built",
  "files": {{
    "package.json": "Complete package.json with React 18, Vite, React Router, @nucleus/css: ^6.46.0, @vitejs/plugin-react - DON'T ADD type module to package.json, ensure must have scripts to start dev server",
    "index.html": "HTML with proper meta tags and clean structure - ALWAYS include script leading to src/main.{main_ext} in index.html",
    "vite.config.{file_ext}": "Vite config with React plugin and server: {{host: true, cors: true, allowedHosts: true}} - KEEP allowedHosts as boolean true - INCLUDE @vitejs/plugin-react",{config_files}
    "src/main.{main_ext}": "React entry point with clean setup - MUST import '@nucleus/css/dist/nucleus.css'",
    "src/App.{main_ext}": "Main App with consistent Router structure using Nucleus CSS",
    "src/index.css": "Global styles with Nucleus CSS imports and custom styles using Nucleus variables",
    "src/components/Layout.{main_ext}": "Consistent layout with clean header/footer using Nucleus components",
    "src/components/Navigation.{main_ext}": "Clean navigation with consistent styling using .nb-btn and Nucleus classes",
    "src/pages/Home.{main_ext}": "Clean hero section with professional design using Nucleus typography and colors",
    "CREATE PAGES BASED ON COMPLEXITY: Simple/Basic (3-5 pages) | Moderate (5-7 pages) | Full/Complete (8-12 pages) - MAINTAIN LAYOUT CONSISTENCY with Nucleus CSS"
  }}
}}

CRITICAL NUCLEUS CSS RULES:
- BE ADAPTIVE - Match complexity to user's request (simple = fewer pages, full = more pages)
- ANALYZE the website purpose and create relevant, meaningful pages
- RESPECT user's complexity preference: simple/basic/minimal = 3-5 pages, full/complete = 8-12 pages
- CLEAN and MODERN over colorful and flashy using Nucleus design system
- CONSISTENT layout and spacing across ALL pages using Nucleus variables
- Use Nucleus color system professionally (primary greens, secondary blues, grayscale)
- Proper responsive design that never breaks using Nucleus breakpoints
- Professional, business-ready appearance following Nucleus guidelines
- Valid JSX syntax with proper JSON escaping
- MANDATORY: All images must use placehold.co URLs
- MANDATORY: Import @nucleus/css/dist/nucleus.css in main entry file
- MANDATORY: Use Nucleus CSS classes (.nb-btn, .nb-h1, .nb-paragraph, etc.)
- MANDATORY: Use Nucleus CSS variables (var(--nt-color-*, --nt-size-*, etc.))
- NO Tailwind CSS classes or utilities
- Test layout on mobile, tablet, and desktop breakpoints using Nucleus responsive system

PERFECT ALIGNMENT ENFORCEMENT - CRITICAL:
- EVERY element must use Nucleus spacing variables for positioning
- ALL cards, buttons, and components must have identical spacing patterns
- NO inconsistent margins or padding - use systematic Nucleus spacing only
- Grid items must align perfectly using CSS Grid with consistent gaps
- Flexbox containers must use justify-content and align-items properly
- Text elements must follow consistent baseline alignment
- Navigation items must be perfectly spaced and aligned
- Form elements must align in perfect columns with consistent spacing
- Images must be consistently sized and positioned
- Page sections must have identical padding and margin patterns
- Header and footer must align perfectly with page content
- Button groups must have identical heights and perfect alignment

NUCLEUS CSS USAGE EXAMPLES - DETAILED:
- **Buttons**: `<button className="nb-btn nb-btn--primary">Primary Button</button>`, `<button className="nb-btn nb-btn--secondary">Secondary Button</button>`, `<button className="nb-btn nb-btn.is-small">Small Button</button>`
- **Headings**: `<h1 className="nb-h1">Main Heading (2.25rem)</h1>`, `<h2 className="nb-h2">Section Heading (1.75rem)</h2>`, `<h3 className="nb-h3">Subsection (1.375rem)</h3>`
- **Typography**: `<p className="nb-paragraph">Body text with proper line height</p>`
- **Containers**: `<div className="nb-container">Centered content with max-width 1500px</div>`
- **Lists**: `<ul className="nb-list"><li className="nb-list-item">List item</li></ul>`
- **Custom Colors**: `style={{color: 'var(--nt-color-font-primary)', backgroundColor: 'var(--nt-color-background-gray-050)'}}`
- **Custom Spacing**: `style={{padding: 'var(--nt-size-spacing-24)', margin: 'var(--nt-size-spacing-16)'}}`
- **Custom Typography**: `style={{fontSize: 'var(--nt-size-font-lg)', fontWeight: 'var(--nt-font-weight-semibold)', lineHeight: 'var(--nt-font-line-height-comfortable)'}}`
- **Shadows & Borders**: `style={{boxShadow: 'var(--nt-shadow-card)', borderRadius: 'var(--nt-size-radius-rounded)', border: 'var(--nt-size-borders-container) solid var(--nt-color-grayscale-200)'}}`
- **Responsive Design**: Use CSS media queries with Nucleus breakpoint variables for responsive layouts
- **Section Spacing**: Always use --nt-size-spacing-56 or --nt-size-spacing-72 between major sections
- **Button Groups**: Ensure identical button heights and consistent spacing using gap property
- **Form Alignment**: All form elements must align perfectly with consistent label widths and input spacing
- **Hero Sections**: Center all content with proper text alignment and consistent padding
- **Interactive States**: Use consistent hover effects with Nucleus action colors and smooth transitions