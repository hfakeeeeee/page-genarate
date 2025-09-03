Create a STUNNING, ultra-modern Vue app for: {instructions}

DESIGN EXCELLENCE REQUIREMENTS:
- Framework: {framework} with {language}
- Build: 7-15 files with seamless Vue Router navigation
- Style: Advanced Nucleus CSS with CLEAN, MODERN aesthetics (NOT overly colorful)
- Color Philosophy: Minimal, sophisticated, professional design using Nucleus design system
- Animations: Subtle, smooth transitions and micro-interactions
- Typography: Clean, readable fonts using Nucleus typography system

NUCLEUS CSS DESIGN SYSTEM - MANDATORY:
- Primary Colors: Use Nucleus color variables (--nt-color-accent-primary-1: #78be20, --nt-color-accent-primary-2: #5c9a1b)
- Background Colors: --nt-color-background-base (#ffffff), --nt-color-background-gray-050 (#f8f8f8), --nt-color-background-gray-100 (#efeff1)
- Text Colors: --nt-color-font-primary (#3a3b3d), --nt-color-font-secondary (#53575a), --nt-color-font-heading (#114A21)
- Action Colors: --nt-color-action-primary-default (#5c9a1b), --nt-color-action-link-default (#007481)
- AVOID: Multiple bright colors, rainbow gradients, too many accent colors
- USE: Nucleus color system with professional color palette

NUCLEUS CSS COMPONENT CLASSES - CRITICAL:
- Buttons: .nb-btn, .nb-btn--primary, .nb-btn--secondary, .nb-btn.is-small
- Typography: .nb-h1, .nb-h2, .nb-h3, .nb-h4, .nb-h5, .nb-h6, .nb-paragraph
- Layout: .nb-container (max-width 1500px, centered)
- Lists: .nb-list, .nb-list-item
- Use CSS custom properties (CSS variables) for colors: var(--nt-color-*)

NUCLEUS CSS LAYOUT STANDARDS - CRITICAL:
- Use Nucleus spacing variables: --nt-size-spacing-* (2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 48, 56, 72)
- Spacing Examples: padding: var(--nt-size-spacing-16), margin: var(--nt-size-spacing-24)
- Border Radius: var(--nt-size-radius-fine) (0.25rem), var(--nt-size-radius-rounded) (0.5rem), var(--nt-size-radius-smooth) (0.75rem)
- Shadows: var(--nt-shadow-card), var(--nt-shadow-popover), var(--nt-shadow-selection)
- NO layout breaks on mobile, tablet, or desktop
- Consistent component sizing across all pages using Nucleus variables
- Proper responsive breakpoints using Nucleus breakpoint variables

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

NUCLEUS CSS STYLING ELEMENTS:
- Use Nucleus font sizes: var(--nt-size-font-sm), var(--nt-size-font-base), var(--nt-size-font-lg), var(--nt-size-font-xl), etc.
- Font weights: var(--nt-font-weight-regular), var(--nt-font-weight-medium), var(--nt-font-weight-semibold), var(--nt-font-weight-bold)
- Line heights: var(--nt-font-line-height-compact), var(--nt-font-line-height-comfortable), var(--nt-font-line-height-open)
- Use Nucleus CSS classes for consistent styling (.nb-btn, .nb-h1, .nb-paragraph, etc.)
- Custom CSS should use Nucleus variables and follow the design system

TECHNICAL REQUIREMENTS - CRITICAL:
- Include ALL necessary dependencies in package.json
- Dependencies: vue, vue-router, @nucleus/css: ^6.46.0
- DevDependencies: vite, @vitejs/plugin-vue, @types/* (for TypeScript), vue-tsc (for TypeScript)
- Ensure vite.config includes Vue plugin import and usage
- MANDATORY: Import "@nucleus/css/dist/nucleus.css" in main entry file
- All generated code must work without additional installation steps
- NO Tailwind CSS dependencies or imports

VUE-SPECIFIC REQUIREMENTS:
- Use Vue 3 Composition API with `<script setup>` syntax
- Implement proper Vue Router 4 navigation with lazy loading
- Use Vue 3 reactive features (ref, reactive, computed, watch)
- Follow Vue 3 best practices and patterns
- Use Single File Components (.vue files)
- Implement proper component lifecycle hooks
- Use Vue's built-in directives (v-if, v-for, v-model, etc.)
- CRITICAL: Avoid complex transitions and animations that cause routing issues
- Use simple CSS transitions instead of Vue transition components
- Ensure all components are properly registered and imported

RESPONSIVE DESIGN REQUIREMENTS:
- Use Nucleus breakpoint variables for responsive design
- Breakpoints: --nt-breakpoint-small (576px), --nt-breakpoint-medium (768px), --nt-breakpoint-large (1200px), --nt-breakpoint-x-large (1500px)
- Text scaling using Nucleus font size variables
- Image responsiveness with proper aspect ratios
- Navigation that works on all screen sizes using Nucleus components

STRUCTURE:
- Vue 3+ with Composition API and modern patterns
- Vue Router 4 with smooth, consistent navigation
- Consistent component architecture across pages
- Proper error handling and loading states
- Clean code organization and naming
- Use `<script setup>` syntax for cleaner components
- Use Nucleus CSS classes and variables throughout

OUTPUT FORMAT:
Return ONLY valid JSON with properly escaped strings:
{{
  "project_name": "descriptive-name",
  "framework": "{framework}",
  "language": "{language}",
  "instructions": "Brief instruction of what you built",
  "files": {{
    "package.json": "Complete package.json with Vue 3, Vite, Vue Router, @nucleus/css: ^6.46.0, @vitejs/plugin-vue - DON'T ADD type module to package.json, ensure must have scripts to start dev server",
    "index.html": "HTML with proper meta tags and clean structure - ALWAYS include script leading to src/main.{main_ext} in index.html",
    "vite.config.{file_ext}": "Vite config with Vue plugin and server: {{host: true, cors: true, allowedHosts: true}} - KEEP allowedHosts as boolean true - INCLUDE @vitejs/plugin-vue",{config_files}
    "src/main.{main_ext}": "Vue entry point with router setup and clean initialization - MUST import '@nucleus/css/dist/nucleus.css'",
    "src/App.vue": "Main App component with router-view and consistent layout using Nucleus CSS",
    "src/style.css": "Global styles with Nucleus CSS imports and custom styles using Nucleus variables",
    "src/router/index.{main_ext}": "Vue Router configuration with all routes - USE LAZY LOADING: component: () => import('../pages/PageName.vue')",
    "src/components/Layout.vue": "Consistent layout component with header/footer using Nucleus components - NO transitions, simple structure",
    "src/components/Navigation.vue": "Clean navigation component with router-link using .nb-btn and Nucleus classes - NO complex animations",
    "src/pages/Home.vue": "Clean hero section with professional design using Nucleus typography and colors",
    "CREATE PAGES BASED ON COMPLEXITY: Simple/Basic (3-5 pages) | Moderate (5-7 pages) | Full/Complete (8-12 pages) - MAINTAIN LAYOUT CONSISTENCY with Nucleus CSS"
  }}
}}

VUE COMPONENT STRUCTURE WITH NUCLEUS CSS:
- Use `<template>`, `<script setup>`, `<style scoped>` structure
- Implement proper props and emits
- Use Vue 3 Composition API patterns
- Follow Vue naming conventions (PascalCase for components)
- Use proper Vue directives and syntax
- CRITICAL: Avoid Vue transition components (Transition, TransitionGroup)
- Use CSS transitions and transforms instead of Vue transitions
- Ensure proper component imports and registration
- Use router-link for navigation, not manual route changes
- Implement proper error boundaries and loading states
- Use Nucleus CSS classes in templates: `<button class="nb-btn nb-btn--primary">`

CRITICAL NUCLEUS CSS RULES:
- BE ADAPTIVE - Match complexity to user's request (simple = fewer pages, full = more pages)
- ANALYZE the website purpose and create relevant, meaningful pages
- RESPECT user's complexity preference: simple/basic/minimal = 3-5 pages, full/complete = 8-12 pages
- CLEAN and MODERN over colorful and flashy using Nucleus design system
- CONSISTENT layout and spacing across ALL pages using Nucleus variables
- Use Nucleus color system professionally (primary greens, secondary blues, grayscale)
- Proper responsive design that never breaks using Nucleus breakpoints
- Professional, business-ready appearance following Nucleus guidelines
- Valid Vue 3 syntax with proper JSON escaping
- MANDATORY: All images must use placehold.co URLs
- MANDATORY: Import @nucleus/css/dist/nucleus.css in main entry file
- MANDATORY: Use Nucleus CSS classes (.nb-btn, .nb-h1, .nb-paragraph, etc.)
- MANDATORY: Use Nucleus CSS variables (var(--nt-color-*, --nt-size-*, etc.))
- Use `<script setup>` syntax for all components
- Implement proper Vue Router navigation
- Test layout on mobile, tablet, and desktop breakpoints using Nucleus responsive system
- CRITICAL: NO Vue transition components - use CSS transitions only
- Use router-link for all navigation
- Implement lazy loading for all route components
- Ensure all components are properly imported and registered
- NO Tailwind CSS classes or utilities

NUCLEUS CSS USAGE EXAMPLES FOR VUE:
- Buttons: `<button class="nb-btn nb-btn--primary">Primary Button</button>`
- Headings: `<h1 class="nb-h1">Main Heading</h1>`
- Paragraphs: `<p class="nb-paragraph">Text content</p>`
- Containers: `<div class="nb-container">Centered content</div>`
- Custom styles: `:style="{color: 'var(--nt-color-font-primary)', padding: 'var(--nt-size-spacing-16)'}"`
- Background colors: `:style="{backgroundColor: 'var(--nt-color-background-gray-050)'}"`
