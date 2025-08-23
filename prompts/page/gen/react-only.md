## React Development Best Practices
- Use functional components with hooks for modern React patterns
- If `language = typescript`, implement explicit prop types with TypeScript interfaces/types and narrow any inferred shapes as needed
- Prefer controlled components for form elements
- Use React.memo() for performance optimization where appropriate
- Only use `useEffect` when absolutely necessary for side effects
- Implement proper cleanup functions in useEffect hooks to prevent memory leaks
- Consider using React.lazy and Suspense for code-splitting when appropriate
- Implement error boundaries around complex or potentially unstable components

## React Component Architecture
- Export a **default** page component using the following pattern:
`export default function <PageName>Page() {...}`
- Structure components with a logical hierarchy (props down, events up)
- Extract reusable UI elements into small, focused subcomponents within the same file
- Keep component state as close as possible to where it's used
- Use custom hooks to extract and reuse stateful logicConventions
- Functional component with hooks only.
- If `language = typescript, add explicit prop types and narrow any inferred shapes as needed.
- Do not using `useEffect` unless strictly necessary.

## React File skeleton
- One file exporting **default** page component:
`export default function <Name>Page() {...}`
- Optional small local subcomponents within the same file.

## React Styling Best Practices (when custom CSS is insufficient)
- Add a `<style>` element **inside** your returned JSX using this pattern:
```jsx
<style>
{`
.page-local-section { 
  margin-block: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.page-local-grid {
  display: grid; 
  gap: 1rem; 
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}
/* Use descriptive class names with 'page-local-' prefix to avoid conflicts */
`}
</style>
```

## React Import Guidelines:
- ALWAYS include `import React from 'react';` at the top of every JSX/TSX file
- Import additional React features as needed: `import { useState, useEffect, useRef } from 'react';`
- For routing, import from react-router-dom: `import { Link, useParams, useNavigate } from 'react-router-dom';`
- Import component-specific CSS if needed: `import './ComponentName.css';`
- Import local components using relative paths: `import ComponentName from '../components/ComponentName';`
- Use modern React Router v6+ API (compatible with v7) for navigation:
  - `<Link to="/...">` instead of `<a href="/...">`
  - `<NavLink>` for navigation with active states
  - `<Outlet>` for nested routes where appropriate
  - Use `useNavigate()` hook for programmatic navigation
  - Use `useParams()` for accessing route parameters

## React Performance Considerations:
- Implement `React.memo()` for components that render often but with the same props
- Use the `useCallback` hook for functions passed as props to child components
- Use the `useMemo` hook for expensive calculations
- Consider implementing virtualization for long lists using libraries like react-window
- Avoid anonymous functions in render methods where possible

## IMPORTANT REQUIREMENTS:
1. ALWAYS include `import React from 'react';` at the top of every JSX/TSX file
2. Do NOT use BrowserRouter or Router components in page components
3. Make sure all component exports use `export default` syntax
4. Include all necessary imports for hooks and components you use