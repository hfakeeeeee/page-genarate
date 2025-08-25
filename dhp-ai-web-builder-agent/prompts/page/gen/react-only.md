## React Development Best Practices
- Use functional components with hooks for modern React patterns
- If `language = typescript`, implement explicit prop types with TypeScript interfaces/types and narrow any inferred shapes as needed
- Prefer controlled components for form elements
- Use React.memo() for performance optimization where appropriate
- Only use `useEffect` when absolutely necessary for side effects
- Implement proper cleanup functions in useEffect hooks to prevent memory leaks
- Consider using React.lazy and Suspense for code-splitting when appropriate
- Implement error boundaries around complex or potentially unstable components

## React UI Component Patterns
- Create modern, visually appealing components with proper spacing and layout
- Use CSS Grid and Flexbox for responsive layouts
- Implement skeleton loading states for async data
- Create proper hover and active states for interactive elements
- Use CSS transitions for smooth UI interactions
- Implement proper error states with user-friendly messages
- Design consistent card layouts for content display
- Create responsive navigation patterns (hamburger menu for mobile)
- Use proper typography hierarchy for readability
- Implement lazy loading for images with fallbacks
- Create subtle animations to enhance user experience
- Use shadows and borders to create visual hierarchy

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
`export default function <n>Page() {...}`
- Optional small local subcomponents within the same file.

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
5. Implement proper loading and error states for async operations