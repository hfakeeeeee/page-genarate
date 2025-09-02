Create a STUNNING, ultra-modern Vue app for: {instructions}

DESIGN EXCELLENCE REQUIREMENTS:
- Framework: {framework} with {language}
- Build: 7-15 files with seamless Vue Router navigation
- Style: Advanced Tailwind CSS with CLEAN, MODERN aesthetics (NOT overly colorful)
- Color Philosophy: Minimal, sophisticated, professional design
- Animations: Subtle, smooth transitions and micro-interactions
- Typography: Clean, readable fonts (Inter, system fonts)

MODERN CLEAN COLOR PALETTE - MANDATORY:
- Primary: Choose ONE sophisticated color scheme from: Blue (slate/sky), Green (emerald/teal), Purple (violet/indigo), Orange (amber/orange), Red (rose/red), Gray (neutral/stone), or Warm (yellow/amber)
- Background: Clean whites, light grays, or subtle warm tones
- Dark mode: Deep colors not pure black (slate-900, gray-900, zinc-900, emerald-900, violet-900)
- Text: High contrast but not harsh (gray-900, slate-800, zinc-700)
- Accent: ONE complementary color that enhances the primary scheme
- AVOID: Multiple bright colors, rainbow gradients, neon colors, too many accent colors
- USE: Monochromatic schemes with subtle color variations and professional tone
- EXAMPLES: Emerald-based (emerald-600, emerald-50, emerald-900), Violet-based (violet-600, violet-50, violet-900), Amber-based (amber-600, amber-50, amber-900)

CLEAN LAYOUT STANDARDS - CRITICAL:
- Consistent spacing system (use p-4, p-6, p-8, p-12 systematically)
- Proper margins and padding on ALL elements
- Clean grid systems (grid-cols-1, grid-cols-2, grid-cols-3)
- Consistent component sizing across all pages
- Proper responsive breakpoints (sm:, md:, lg:, xl:)
- NO layout breaks on mobile, tablet, or desktop
- Uniform header/navigation height across pages
- Consistent card sizes and spacing
- Proper text alignment and hierarchy

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

MODERN DESIGN ELEMENTS:
- Subtle shadows (shadow-sm, shadow-md, shadow-lg - NOT shadow-2xl)
- Clean borders using chosen color scheme (border-gray-200, border-emerald-200, border-violet-200, etc.)
- Minimal use of gradients (only for subtle backgrounds using primary color)
- Glass morphism effects used sparingly with chosen color theme
- Clean button designs with proper padding and primary color scheme
- Consistent rounded corners (rounded-lg, rounded-xl)
- Proper whitespace and breathing room
- Color-coordinated hover states and interactive elements

TECHNICAL REQUIREMENTS - CRITICAL:
- Include ALL necessary dependencies in package.json
- Dependencies: vue, vue-router, @vitejs/plugin-vue
- DevDependencies: vite, tailwindcss, postcss, autoprefixer, @types/* (for TypeScript), vue-tsc (for TypeScript)
- Ensure vite.config includes Vue plugin import and usage
- All generated code must work without additional installation steps

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
- Desktop optimization
- Text scaling (text-sm, text-base, text-lg, text-xl)
- Image responsiveness with proper aspect ratios
- Navigation that works on all screen sizes

STRUCTURE:
- Vue 3+ with Composition API and modern patterns
- Vue Router 4 with smooth, consistent navigation
- Consistent component architecture across pages
- Proper error handling and loading states
- Clean code organization and naming
- Use `<script setup>` syntax for cleaner components

OUTPUT FORMAT:
Return ONLY valid JSON with properly escaped strings:
{{
  "project_name": "descriptive-name",
  "framework": "{framework}",
  "language": "{language}",
  "instructions": "Brief instruction of what you built",
  "files": {{
    "package.json": "Complete package.json with Vue 3, Vite, Tailwind, Vue Router, @vitejs/plugin-vue, autoprefixer - DON'T ADD type module to package.json, ensure must have scripts to start dev server",
    "index.html": "HTML with proper meta tags and clean structure - ALWAYS include script leading to src/main.{main_ext} in index.html",
    "vite.config.{file_ext}": "Vite config with Vue plugin and server: {{host: true, cors: true, allowedHosts: true}} - KEEP allowedHosts as boolean true - INCLUDE @vitejs/plugin-vue",
    "tailwind.config.js": "Clean Tailwind config with consistent design tokens using chosen color scheme - keep plugins empty for now",
    "postcss.config.js": "PostCSS config for Tailwind",{config_files}
    "src/main.{main_ext}": "Vue entry point with router setup and clean initialization",
    "src/App.vue": "Main App component with router-view and consistent layout",
    "src/style.css": "Global styles with Tailwind, clean base styles",
    "src/router/index.{main_ext}": "Vue Router configuration with all routes - USE LAZY LOADING: component: () => import('../pages/PageName.vue')",
    "src/components/Layout.vue": "Consistent layout component with header/footer - NO transitions, simple structure",
    "src/components/Navigation.vue": "Clean navigation component with router-link - NO complex animations",
    "src/pages/Home.vue": "Clean hero section with professional design",
    "CREATE PAGES BASED ON COMPLEXITY: Simple/Basic (3-5 pages) | Moderate (5-7 pages) | Full/Complete (8-12 pages) - MAINTAIN LAYOUT CONSISTENCY"
  }}
}}

VUE COMPONENT STRUCTURE:
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

CRITICAL RULES:
- BE ADAPTIVE - Match complexity to user's request (simple = fewer pages, full = more pages)
- ANALYZE the website purpose and create relevant, meaningful pages
- RESPECT user's complexity preference: simple/basic/minimal = 3-5 pages, full/complete = 8-12 pages
- CHOOSE ONE sophisticated color scheme and use it consistently throughout
- CLEAN and MODERN over colorful and flashy
- CONSISTENT layout and spacing across ALL pages
- ONE primary color scheme with maximum one accent color
- Proper responsive design that never breaks
- Professional, business-ready appearance
- Valid Vue 3 syntax with proper JSON escaping
- MANDATORY: All images must use placehold.co URLs
- Use `<script setup>` syntax for all components
- Implement proper Vue Router navigation
- Test layout on mobile, tablet, and desktop breakpoints
- CRITICAL: NO Vue transition components - use CSS transitions only
- Use router-link for all navigation
- Implement lazy loading for all route components
- Ensure all components are properly imported and registered