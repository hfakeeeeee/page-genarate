Create a STUNNING, ultra-modern React app for: {instructions}

DESIGN EXCELLENCE REQUIREMENTS:
- Framework: {framework} with {language}
- Build: 7-15 files with seamless React Router navigation
- Style: Advanced Tailwind CSS with CLEAN, MODERN aesthetics (NOT overly colorful)
- Color Philosophy: Minimal, sophisticated, professional design
- Animations: Subtle, smooth transitions and micro-interactions
- Typography: Clean, readable fonts (Inter, system fonts)

MODERN CLEAN COLOR PALETTE - MANDATORY:
- Primary: Neutral color with ONE subtle accent color
- Background: Clean color
- Dark mode: Deep color not black (slate-900, gray-900, zinc-900)
- Text: High contrast but not harsh 
- AVOID: Multiple bright colors, rainbow gradients, too many accent colors
- USE: Monochromatic schemes with subtle color variations

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

CREATIVE FREEDOM & INTELLIGENCE:
- ANALYZE the website type and CREATE relevant pages intelligently
- CREATE 8-12 meaningful pages that make sense for the specific website type
- ADD unique features and sections that enhance user experience
- THINK beyond basic pages - add creative, relevant functionality

IMAGE REQUIREMENTS - MANDATORY:
- ALL images must use placehold.co URLs: https://placehold.co/WIDTHxHEIGHT
- Examples: https://placehold.co/800x600, https://placehold.co/400x300, https://placehold.co/1200x800
- NO internal image sources (./assets/, /images/, etc.)
- Use appropriate sizes: Hero images (1200x800), Cards (400x300), Avatars (100x100)
- Add descriptive text parameter: https://placehold.co/800x600?text=Hero+Image

MODERN DESIGN ELEMENTS:
- Subtle shadows (shadow-sm, shadow-md, shadow-lg - NOT shadow-2xl)
- Clean borders (border-gray-200, border-slate-300)
- Minimal use of gradients (only for subtle backgrounds)
- Glass morphism effects used sparingly
- Clean button designs with proper padding
- Consistent rounded corners (rounded-lg, rounded-xl)
- Proper whitespace and breathing room

TECHNICAL REQUIREMENTS - CRITICAL:
- Include ALL necessary dependencies in package.json
- Dependencies: react, react-dom, react-router-dom, @vitejs/plugin-react
- DevDependencies: vite, tailwindcss, postcss, autoprefixer, @types/* for TypeScript
- Ensure vite.config includes React plugin import and usage
- All generated code must work without additional installation steps

RESPONSIVE DESIGN REQUIREMENTS:
- Desktop optimization
- Text scaling (text-sm, text-base, text-lg, text-xl)
- Image responsiveness with proper aspect ratios
- Navigation that works on all screen sizes

STRUCTURE:
- React 18+ with modern hooks and clean patterns
- React Router with smooth, consistent navigation
- Consistent component architecture across pages
- Proper error boundaries and loading states
- Clean code organization and naming

OUTPUT FORMAT:
Return ONLY valid JSON with properly escaped strings:
{{
  "project_name": "descriptive-name",
  "framework": "{framework}",
  "language": "{language}",
  "instructions": "Brief instruction of what you built",
  "files": {{
    "package.json": "Complete package.json with React 18, Vite, Tailwind, React Router, @vitejs/plugin-react, autoprefixer", DON'T ADD type module to package.json, ensure must have scripts to start dev server,
    "index.html": "HTML with proper meta tags and clean structure", ALWAYS include script leading to src/App.{main_ext} in index.html",
    "vite.config.{file_ext}": "Vite config with React plugin and server: {{host: true, cors: true, allowedHosts: true}} - KEEP allowedHosts as boolean true - INCLUDE @vitejs/plugin-react",
    "tailwind.config.js": "Clean Tailwind config with consistent design tokens", keep plugins empty for now,
    "postcss.config.js": "PostCSS config for Tailwind",{config_files}
    "src/main.{main_ext}": "React entry point with clean setup",
    "src/App.{main_ext}": "Main App with consistent Router structure",
    "src/index.css": "Global styles with Tailwind, clean base styles",
    "src/components/Layout.{main_ext}": "Consistent layout with clean header/footer",
    "src/components/Navigation.{main_ext}": "Clean navigation with consistent styling",
    "src/pages/Home.{main_ext}": "Clean hero section with professional design",
    "CREATE 8-12 MORE RELEVANT PAGES based on website type - MAINTAIN LAYOUT CONSISTENCY"
  }}
}}

CRITICAL RULES:
- BE CREATIVE - Don't just create basic pages, think about what users really need
- ANALYZE the website purpose and create relevant, meaningful pages
- CLEAN and MODERN over colorful and flashy
- CONSISTENT layout and spacing across ALL pages
- ONE accent color maximum, rest neutral
- Proper responsive design that never breaks
- Professional, business-ready appearance
- Valid JSX syntax with proper JSON escaping
- MANDATORY: All images must use placehold.co URLs
- Test layout on mobile, tablet, and desktop breakpoints"""