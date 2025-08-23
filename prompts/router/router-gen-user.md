Framework: {{FRAMEWORK}}
Language: {{LANGUAGE}}

## Routing Configuration Request

Please implement a complete routing solution for the following pages:
{{PAGE_ROUTES}}

Create {{FILEPATH}} with a production-ready router implementation that meets these requirements:

## Technical Requirements
- Return exactly ONE fenced code block labeled `code` containing the complete file content
- The code must be the full contents of {{FILEPATH}} with no omissions
- Implement routing using the appropriate framework router:
  - React: React Router (v6+ API; compatible with v7)
  - Vue: Vue Router (v4+ for Vue 3, v3+ for Vue 2)
- Implement code-splitting for improved performance and initial load time
- Include comprehensive error handling and fallback UI for route loading errors
- Implement a proper 404/NotFound route for unmatched paths

## Implementation Details for React
- Wrap the application with <BrowserRouter> (or alternative if needed)
- Define <Routes> with one <Route> per page from {{PAGE_ROUTES}}
- Implement React.lazy for code-splitting:
  - Derive import paths by replacing leading "src/" with "./"
  - Example: "src/pages/MyPage" becomes "./pages/MyPage"
- Include a loading state using Suspense and fallback UI
- Provide a user-friendly navigation component with:
  - <Link> components to all non-dynamic routes (those without ":" params)
  - Active state indication for the current route
  - Responsive design considerations for mobile navigation

## Implementation Details for Vue
- Configure Vue Router with appropriate mode (history preferred)
- Define routes array with one route per page from {{PAGE_ROUTES}}
- Implement route-level code-splitting using dynamic imports
- Include meta information for each route (title, requires auth, etc.)
- Create a navigation component that:
  - Uses <router-link> components for navigation
  - Shows active states for current route
  - Adapts to different screen sizes

## Code Quality Requirements
- No third-party UI libraries (use framework-native components only)
- No global CSS imports within the router file
- No console logs or debugging code
- Clean, well-structured code with appropriate comments
- Type safety: If Language = TS, use proper TypeScript types throughout

## Minimal Structure (conceptual outline)
- Import necessary router and framework dependencies
- Define lazy-loaded components from page definitions
- Configure routes with proper paths and components
- Implement navigation component with links to routes
- Export router configuration (Vue) or wrap app with router (React)
