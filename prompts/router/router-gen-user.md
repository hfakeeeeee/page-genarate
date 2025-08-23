Framework: {{FRAMEWORK}}
Language: {{LANGUAGE}}

Add routing for following pages (JSON array of objects with name and route, filepath under /src):
{{PAGE_ROUTES}}

Create {{FILEPATH}} with working router:

## Requirements
- Return exactly ONE fenced code block labeled `code`. No prose before/after.
- The code must be the full contents of {{FILEPATH}}
- React app router using React Router (v6+ API; works with v7 too)
- Wrap the app UI with <BrowserRouter>
- Define <Routes> with one <Route> per page in {{PAGE_ROUTES}}
- Use React.lazy for pages:
    - Derive import path by replacing leading "src/" with "./".
    - Example: "src/pages/MyPage" becomes "./pages/MyPage".
- Provide a NotFound route for unmatched routes.
- Provide a simple <nav> with <Link> to all non-dynamic routes (those without ":" params).
- No third-party UI libs. No global CSS import here. No console logs.
- If Language = TS, file is .tsx and types are explicit (use React.FC where possible).

## Minimal structure to follow (sketch)
- Imports: React, { Suspense, lazy }, and { BrowserRouter, Routes, Route, Link } from 'react-router-dom'.
- Build an array from {{PAGE_ROUTES}} and map to lazy components and <Route> entry.
- Export default function App() { ... } that renders the nav + <Suspense><Routes/></Suspense>.
